"""
各カスタムProviderの単体テスト

PostgreSqlChatHistoryProvider・PlanningContextProvider・
ToolResultContextProvider・ContextCompressionService・
ContextStorageManagerのDB操作・ファイル操作をモックして動作を検証する。
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from providers.chat_history_provider import PostgreSqlChatHistoryProvider
from providers.planning_context_provider import PlanningContextProvider
from providers.tool_result_context_provider import ToolResultContextProvider
from providers.context_compression_service import ContextCompressionService
from providers.context_storage_manager import ContextStorageManager


# ========================================
# テスト用ヘルパー
# ========================================


def _make_mock_pool(fetch_return=None, fetchval_return=None) -> MagicMock:
    """
    asyncpg接続プールのモックを生成する。

    Args:
        fetch_return: conn.fetch()の戻り値
        fetchval_return: conn.fetchval()の戻り値

    Returns:
        モックasyncpg接続プール
    """
    pool = MagicMock()
    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=fetch_return or [])
    mock_conn.fetchval = AsyncMock(return_value=fetchval_return or 0)
    mock_conn.fetchrow = AsyncMock(return_value=None)
    mock_conn.execute = AsyncMock()
    pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    pool.acquire.return_value.__aexit__ = AsyncMock(return_value=False)
    return pool


# ========================================
# TestPostgreSqlChatHistoryProvider
# ========================================


class TestPostgreSqlChatHistoryProvider:
    """PostgreSqlChatHistoryProviderのテスト"""

    @pytest.mark.asyncio
    async def test_get_messagesがメッセージ一覧を返す(self) -> None:
        """asyncpgプールをモックしてget_messages()がメッセージリストを返すことを確認する"""
        # fetchが返すRowのモックを生成する
        mock_row = MagicMock()
        mock_row.__getitem__ = lambda self, key: {
            "role": "user",
            "content": "テストメッセージ",
            "tokens": 10,
        }[key]
        pool = _make_mock_pool(fetch_return=[mock_row])

        provider = PostgreSqlChatHistoryProvider(db_pool=pool)
        result = await provider.get_messages("test-uuid")

        assert len(result) == 1
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "テストメッセージ"

    @pytest.mark.asyncio
    async def test_save_messagesが新規メッセージのみINSERTする(self) -> None:
        """既存メッセージ数を考慮して差分のみINSERTすることを確認する"""
        # 既存メッセージが1件ある状態をモックする
        pool = _make_mock_pool(fetchval_return=1)
        mock_conn = pool.acquire.return_value.__aenter__.return_value

        provider = PostgreSqlChatHistoryProvider(db_pool=pool)
        messages = [
            {"role": "user", "content": "既存メッセージ"},
            {"role": "assistant", "content": "新規メッセージ"},
        ]
        await provider.save_messages("test-uuid", messages)

        # INSERTが実行されていることを確認する（新規1件分）
        assert mock_conn.execute.call_count >= 1
        call_args_str = str(mock_conn.execute.call_args_list)
        assert "INSERT" in call_args_str


# ========================================
# TestPlanningContextProvider
# ========================================


class TestPlanningContextProvider:
    """PlanningContextProviderのテスト"""

    @pytest.mark.asyncio
    async def test_before_runがプランニング履歴をMarkdown形式で返す(self) -> None:
        """asyncpgをモックしてMarkdown形式のテキストが返ることを確認する"""
        mock_row = MagicMock()
        mock_row.__getitem__ = lambda self, key: {
            "phase": "planning",
            "node_id": "node1",
            "plan": "テスト計画",
            "action_id": "act-001",
            "result": "成功",
        }[key]
        pool = _make_mock_pool(fetch_return=[mock_row])

        provider = PlanningContextProvider(db_pool=pool)
        result = await provider.before_run(task_uuid="test-uuid")

        assert result is not None
        assert "## プランニング履歴" in result
        assert "planning" in result
        assert "node1" in result

    @pytest.mark.asyncio
    async def test_before_runでデータがない場合はNoneを返す(self) -> None:
        """データがない場合はNoneを返すことを確認する"""
        pool = _make_mock_pool(fetch_return=[])

        provider = PlanningContextProvider(db_pool=pool)
        result = await provider.before_run(task_uuid="test-uuid")

        assert result is None

    @pytest.mark.asyncio
    async def test_after_runがDBにプランニング履歴を保存する(self) -> None:
        """after_run()がINSERTを実行することを確認する"""
        pool = _make_mock_pool()
        mock_conn = pool.acquire.return_value.__aenter__.return_value

        provider = PlanningContextProvider(db_pool=pool)
        await provider.after_run(
            task_uuid="test-uuid",
            phase="planning",
            node_id="node1",
            plan={"key": "value"},
            action_id="act-001",
            result="成功",
        )

        assert mock_conn.execute.call_count == 1
        call_args_str = str(mock_conn.execute.call_args_list)
        assert "INSERT" in call_args_str


# ========================================
# TestToolResultContextProvider
# ========================================


class TestToolResultContextProvider:
    """ToolResultContextProviderのテスト"""

    @pytest.mark.asyncio
    async def test_before_runがツール実行結果のサマリを返す(self) -> None:
        """asyncpgとファイルシステムをモックして結果を確認する"""
        mock_row = MagicMock()
        mock_row.__getitem__ = lambda self, key: {
            "tool_name": "execute_command",
            "tool_command": "ls -la",
            "file_path": "/tmp/result.json",
            "created_at": "2024-01-01",
        }[key]
        pool = _make_mock_pool(fetch_return=[mock_row])

        provider = ToolResultContextProvider(db_pool=pool)
        # ファイル読み込みをモックする
        with patch("pathlib.Path.exists", return_value=False):
            result = await provider.before_run(task_uuid="test-uuid")

        # ファイルが存在しない場合でもNoneにはならない（メタデータは存在するため）
        assert result is not None

    @pytest.mark.asyncio
    async def test_after_runがメタデータをDBに保存する(self) -> None:
        """after_run()がファイル保存とDB保存を行うことを確認する"""
        pool = _make_mock_pool()
        mock_conn = pool.acquire.return_value.__aenter__.return_value

        provider = ToolResultContextProvider(db_pool=pool, file_storage_base_dir="/tmp/test")
        tool_result = {"output": "コマンド実行結果", "exit_code": 0}

        # ファイルシステム操作をモックする
        with patch("pathlib.Path.mkdir"), \
             patch("pathlib.Path.write_text"), \
             patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 100
            await provider.after_run(
                task_uuid="test-uuid",
                tool_name="execute_command",
                tool_command="ls -la",
                arguments={"command": "ls -la"},
                result=tool_result,
            )

        # DBへのINSERTが呼ばれていることを確認する
        assert mock_conn.execute.call_count >= 1


# ========================================
# TestContextCompressionService
# ========================================


class TestContextCompressionService:
    """ContextCompressionServiceのテスト"""

    @pytest.mark.asyncio
    async def test_圧縮無効の場合はFalseを返す(self) -> None:
        """context_compression_enabled=Falseの場合にFalseを返すことを確認する"""
        # ユーザー設定でcontext_compression_enabled=Falseを返すモックを作成する
        user_config_row = MagicMock()
        user_config_row.__getitem__ = lambda self, key: {
            "context_compression_enabled": False,
            "token_threshold": 10000,
            "keep_recent_messages": 5,
            "min_to_compress": 3,
            "min_compression_ratio": 0.5,
            "model_name": "gpt-4o",
        }[key]
        pool = MagicMock()
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=user_config_row)
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_config = MagicMock()
        mock_config.default_token_threshold = 10000
        mock_config.model_recommendations = {}

        service = ContextCompressionService(
            db_pool=pool,
            llm_client=MagicMock(),
            config=mock_config,
        )
        result = await service.check_and_compress_async(
            task_uuid="test-uuid", user_email="test@example.com"
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_トークン数が閾値以下の場合は圧縮しない(self) -> None:
        """total_tokens <= token_thresholdの場合にFalseを返すことを確認する"""
        # 圧縮有効だがトークン数が少ない状態を作成する
        user_config_row = MagicMock()
        user_config_row.__getitem__ = lambda self, key: {
            "context_compression_enabled": True,
            "token_threshold": 100000,
            "keep_recent_messages": 5,
            "min_to_compress": 3,
            "min_compression_ratio": 0.5,
            "model_name": "gpt-4o",
        }[key]
        # 合計トークン数が少ない状態を返す
        token_row = MagicMock()
        token_row.__getitem__ = lambda self, key: {"total_tokens": 100}[key]

        pool = MagicMock()
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(side_effect=[user_config_row, token_row])
        mock_conn.fetch = AsyncMock(return_value=[])
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_config = MagicMock()
        mock_config.default_token_threshold = 100000
        mock_config.model_recommendations = {}

        service = ContextCompressionService(
            db_pool=pool,
            llm_client=MagicMock(),
            config=mock_config,
        )
        result = await service.check_and_compress_async(
            task_uuid="test-uuid", user_email="test@example.com"
        )

        # トークン数が閾値以下なので圧縮しない
        assert result is False


# ========================================
# TestContextStorageManager
# ========================================


class TestContextStorageManager:
    """ContextStorageManagerのテスト"""

    @pytest.mark.asyncio
    async def test_save_token_usageがリポジトリを呼び出す(self) -> None:
        """save_token_usage()がtoken_usage_repository.record_token_usage()を呼び出すことを確認する"""
        mock_token_repo = AsyncMock()
        mock_token_repo.record_token_usage = AsyncMock()

        manager = ContextStorageManager(
            chat_history_provider=MagicMock(),
            token_usage_repository=mock_token_repo,
            context_repository=MagicMock(),
            task_repository=MagicMock(),
        )

        await manager.save_token_usage(
            user_email="test@example.com",
            task_uuid="test-uuid",
            node_id="node1",
            model="gpt-4o",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
        )

        # record_token_usageが呼ばれていることを確認する
        mock_token_repo.record_token_usage.assert_called_once()
