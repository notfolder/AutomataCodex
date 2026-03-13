"""
connection.py の単体テスト

データベース接続プール管理・マイグレーション実行・暗号化キー取得を検証する。
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ========================================
# get_encryption_key のテスト
# ========================================


class TestGetEncryptionKey:
    """get_encryption_key のテスト"""

    def test_returns_32_byte_key(self):
        """32バイトのキーが正しく返ることを検証する"""
        from database.connection import get_encryption_key

        with patch.dict(os.environ, {"ENCRYPTION_KEY": "a" * 32}):
            key = get_encryption_key()
        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_raises_when_key_not_set(self):
        """ENCRYPTION_KEYが未設定の場合にValueErrorが発生することを検証する"""
        from database.connection import get_encryption_key

        env = os.environ.copy()
        env.pop("ENCRYPTION_KEY", None)
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ValueError, match="ENCRYPTION_KEY"):
                get_encryption_key()

    def test_raises_when_key_not_32_bytes(self):
        """32バイト以外のキーを指定した場合にValueErrorが発生することを検証する"""
        from database.connection import get_encryption_key

        with patch.dict(os.environ, {"ENCRYPTION_KEY": "short"}):
            with pytest.raises(ValueError, match="32バイト"):
                get_encryption_key()


# ========================================
# _build_dsn のテスト
# ========================================


class TestBuildDsn:
    """_build_dsn のテスト"""

    def test_uses_database_url_when_set(self):
        """DATABASE_URLが設定されている場合はそれを使用することを検証する"""
        from database.connection import _build_dsn

        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://custom/db"}):
            dsn = _build_dsn()
        assert dsn == "postgresql://custom/db"

    def test_builds_dsn_from_components(self):
        """個別の環境変数からDSNを組み立てることを検証する"""
        from database.connection import _build_dsn

        env = {
            "POSTGRES_HOST": "myhost",
            "POSTGRES_PORT": "5433",
            "POSTGRES_DB": "mydb",
            "POSTGRES_USER": "myuser",
            "POSTGRES_PASSWORD": "mypassword",
        }
        env.pop("DATABASE_URL", None)
        with patch.dict(os.environ, env, clear=True):
            dsn = _build_dsn()
        assert dsn == "postgresql://myuser:mypassword@myhost:5433/mydb"

    def test_uses_defaults(self):
        """環境変数未設定時にデフォルト値を使用することを検証する"""
        from database.connection import _build_dsn

        env = {"POSTGRES_PASSWORD": "pw"}
        with patch.dict(os.environ, env, clear=False):
            # DATABASE_URLを取り除いた上でデフォルト確認する
            env_without_url = {k: v for k, v in os.environ.items() if k != "DATABASE_URL"}
            env_without_url.pop("POSTGRES_HOST", None)
            env_without_url.pop("POSTGRES_PORT", None)
            env_without_url.pop("POSTGRES_DB", None)
            env_without_url.pop("POSTGRES_USER", None)
            env_without_url["POSTGRES_PASSWORD"] = "pw"
            with patch.dict(os.environ, env_without_url, clear=True):
                dsn = _build_dsn()
        assert "postgres:5432" in dsn
        assert "coding_agent" in dsn


# ========================================
# run_migration のテスト
# ========================================


class TestRunMigration:
    """run_migration のテスト"""

    async def test_skips_if_already_applied(self, tmp_path: Path):
        """適用済みのマイグレーションはスキップされることを検証する"""
        from database import connection as conn_mod

        migration_file = tmp_path / "1.0.0_test.sql"
        migration_file.write_text("SELECT 1;")

        pool = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        # schema_versionsテーブル作成はNone（成功）
        conn.execute = AsyncMock(return_value=None)
        # 適用済みとしてバージョンを返す
        conn.fetchval = AsyncMock(return_value="1.0.0")

        await conn_mod.run_migration(migration_file, pool=pool)

        # SQL実行が呼ばれていないこと（schema_versions作成の1回だけ）を確認する
        assert conn.execute.await_count == 1

    async def test_applies_migration_when_not_applied(self, tmp_path: Path):
        """未適用のマイグレーションが正しく実行されることを検証する"""
        from database import connection as conn_mod

        migration_file = tmp_path / "1.0.0_init.sql"
        migration_file.write_text("CREATE TABLE test (id SERIAL PRIMARY KEY);")

        pool = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        conn.execute = AsyncMock(return_value=None)
        # 未適用としてNoneを返す
        conn.fetchval = AsyncMock(return_value=None)

        # transaction() はコンテキストマネージャを直接返すため MagicMock を使用する
        tx_ctx = MagicMock()
        tx_ctx.__aenter__ = AsyncMock(return_value=None)
        tx_ctx.__aexit__ = AsyncMock(return_value=None)
        conn.transaction = MagicMock(return_value=tx_ctx)

        await conn_mod.run_migration(migration_file, pool=pool)

        # SQLが実行されたこと（schema_versions作成 + migration SQL + schema_versions INSERT）を確認する
        assert conn.execute.await_count >= 2

    async def test_raises_if_file_not_found(self, tmp_path: Path):
        """マイグレーションファイルが存在しない場合にFileNotFoundErrorが発生することを検証する"""
        from database import connection as conn_mod

        non_existent = tmp_path / "9.9.9_missing.sql"
        pool = MagicMock()

        with pytest.raises(FileNotFoundError):
            await conn_mod.run_migration(non_existent, pool=pool)

    async def test_version_is_inserted_to_schema_versions(self, tmp_path: Path):
        """マイグレーション適用後にschema_versionsへバージョンが記録されることを検証する"""
        from database import connection as conn_mod

        migration_file = tmp_path / "2.0.0_add_table.sql"
        migration_file.write_text("SELECT 1;")

        pool = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        conn.fetchval = AsyncMock(return_value=None)

        # transaction() はコンテキストマネージャを直接返すため MagicMock を使用する
        tx_ctx = MagicMock()
        tx_ctx.__aenter__ = AsyncMock(return_value=None)
        tx_ctx.__aexit__ = AsyncMock(return_value=None)
        conn.transaction = MagicMock(return_value=tx_ctx)

        # execute 呼び出しを記録する
        executed_sqls: list[str] = []

        async def capture_execute(sql: str, *_: object) -> None:
            executed_sqls.append(sql.strip())

        conn.execute = AsyncMock(side_effect=capture_execute)

        await conn_mod.run_migration(migration_file, pool=pool)

        # schema_versions への INSERT が呼ばれていることを確認する
        assert any("INSERT INTO schema_versions" in sql for sql in executed_sqls)
        # '2.0.0' がバージョンとして渡されていることを確認する
        all_args = [
            call.args for call in conn.execute.await_args_list
        ]
        version_inserted = any("2.0.0" in str(a) for a in all_args)
        assert version_inserted


# ========================================
# run_all_migrations のテスト
# ========================================


class TestRunAllMigrations:
    """run_all_migrations のテスト"""

    async def test_applies_all_files_in_order(self, tmp_path: Path):
        """migrationsディレクトリのSQLファイルをバージョン順に適用することを検証する"""
        from database import connection as conn_mod

        # 複数のマイグレーションファイルを作成する
        (tmp_path / "1.0.0_first.sql").write_text("SELECT 1;")
        (tmp_path / "1.1.0_second.sql").write_text("SELECT 2;")

        pool = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        # すべて未適用とする
        conn.fetchval = AsyncMock(return_value=None)
        conn.execute = AsyncMock(return_value=None)

        # transaction() はコンテキストマネージャを直接返すため MagicMock を使用する
        tx_ctx = MagicMock()
        tx_ctx.__aenter__ = AsyncMock(return_value=None)
        tx_ctx.__aexit__ = AsyncMock(return_value=None)
        conn.transaction = MagicMock(return_value=tx_ctx)

        await conn_mod.run_all_migrations(migrations_dir=tmp_path, pool=pool)

        # execute が複数回呼ばれていることを確認する（各ファイルで複数回）
        assert conn.execute.await_count > 2

    async def test_returns_early_if_no_sql_files(self, tmp_path: Path):
        """SQLファイルが存在しない場合は何も実行しないことを検証する"""
        from database import connection as conn_mod

        pool = MagicMock()
        conn = AsyncMock()

        # SQLファイルが存在しない空ディレクトリ
        await conn_mod.run_all_migrations(migrations_dir=tmp_path, pool=pool)

        # acquireが呼ばれていないことを確認する
        pool.acquire.assert_not_called()

    async def test_returns_early_if_dir_not_exists(self, tmp_path: Path):
        """migrationsディレクトリが存在しない場合は何も実行しないことを検証する"""
        from database import connection as conn_mod

        pool = MagicMock()
        non_existent_dir = tmp_path / "nonexistent"

        await conn_mod.run_all_migrations(migrations_dir=non_existent_dir, pool=pool)

        pool.acquire.assert_not_called()
