"""
各カスタムProviderの単体テスト

PostgreSqlChatHistoryProvider・PlanningContextProvider・
ToolResultContextProvider・ContextCompressionService・
TaskInheritanceContextProvider・ContextStorageManagerの
DB操作・ファイル操作をモックして動作を検証する。
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from providers.chat_history_provider import PostgreSqlChatHistoryProvider
from providers.planning_context_provider import PlanningContextProvider
from providers.tool_result_context_provider import ToolResultContextProvider
from providers.context_compression_service import ContextCompressionService
from providers.task_inheritance_context_provider import TaskInheritanceContextProvider
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


# ========================================
# TestTaskInheritanceContextProvider
# ========================================


class TestTaskInheritanceContextProvider:
    """TaskInheritanceContextProviderのテスト"""

    @pytest.mark.asyncio
    async def test_before_runがdisable_inheritanceの場合はNoneを返す(self) -> None:
        """disable_inheritance=Trueの場合にNoneを返すことを確認する"""
        metadata = json.dumps({"disable_inheritance": True})
        task_row = MagicMock()
        task_row.__getitem__ = lambda self, key: {"metadata": metadata}[key]
        pool = _make_mock_pool()
        mock_conn = pool.acquire.return_value.__aenter__.return_value
        mock_conn.fetchrow = AsyncMock(return_value=task_row)

        provider = TaskInheritanceContextProvider(db_pool=pool)
        result = await provider.before_run(task_uuid="test-uuid")

        assert result is None

    @pytest.mark.asyncio
    async def test_before_runがタスク未発見の場合はNoneを返す(self) -> None:
        """tasksテーブルにtask_uuidが存在しない場合にNoneを返すことを確認する"""
        pool = _make_mock_pool()
        mock_conn = pool.acquire.return_value.__aenter__.return_value
        mock_conn.fetchrow = AsyncMock(return_value=None)

        provider = TaskInheritanceContextProvider(db_pool=pool)
        result = await provider.before_run(task_uuid="nonexistent-uuid")

        assert result is None

    @pytest.mark.asyncio
    async def test_before_runが過去タスクない場合はNoneを返す(self) -> None:
        """過去の成功タスクが存在しない場合にNoneを返すことを確認する"""
        metadata = json.dumps({
            "task_identifier": "issue-123",
            "repository": "owner/repo",
        })
        task_row = MagicMock()
        task_row.__getitem__ = lambda self, key: {"metadata": metadata}[key]
        pool = _make_mock_pool(fetch_return=[])
        mock_conn = pool.acquire.return_value.__aenter__.return_value
        mock_conn.fetchrow = AsyncMock(return_value=task_row)

        provider = TaskInheritanceContextProvider(db_pool=pool)
        result = await provider.before_run(task_uuid="test-uuid")

        assert result is None

    @pytest.mark.asyncio
    async def test_before_runが過去タスクのMarkdownを返す(self) -> None:
        """過去タスクが存在する場合にMarkdown形式の継承データを返すことを確認する"""
        from unittest.mock import patch as mock_patch

        metadata = json.dumps({
            "task_identifier": "issue-123",
            "repository": "owner/repo",
        })
        past_metadata_str = json.dumps({
            "inheritance_data": {
                "final_summary": "実装完了",
                "planning_history": [],
                "implementation_patterns": [],
                "key_decisions": ["pytestを使用"],
            }
        })
        task_row = MagicMock()
        task_row.__getitem__ = lambda self, key: {"metadata": metadata}[key]

        pool = _make_mock_pool()
        mock_conn = pool.acquire.return_value.__aenter__.return_value
        mock_conn.fetchrow = AsyncMock(return_value=task_row)

        # _get_past_tasks_asyncをパッチして期待する辞書を返す
        past_task_dict = {
            "task_uuid": "past-uuid",
            "metadata": past_metadata_str,
            "completed_at": "2024-01-01",
        }

        provider = TaskInheritanceContextProvider(db_pool=pool)
        with mock_patch.object(
            provider, "_get_past_tasks_async", AsyncMock(return_value=past_task_dict)
        ):
            result = await provider.before_run(task_uuid="test-uuid")

        assert result is not None
        assert "Previous Task Context" in result
        assert "pytestを使用" in result

    def test_format_inheritance_dataがMarkdownを生成する(self) -> None:
        """_format_inheritance_data()が期待するMarkdown形式を返すことを確認する"""
        provider = TaskInheritanceContextProvider(db_pool=MagicMock())
        inheritance_data = {
            "final_summary": "テスト完了",
            "planning_history": [
                {"phase": "planning", "node_id": "node1", "plan": "計画", "created_at": "2024-01-01"}
            ],
            "implementation_patterns": [
                {"pattern_type": "test", "description": "pytestを使用"}
            ],
            "key_decisions": ["決定1", "決定2"],
        }

        result = provider._format_inheritance_data(inheritance_data)

        assert "Previous Task Context" in result
        assert "テスト完了" in result
        assert "Planning History" in result
        assert "pytestを使用" in result
        assert "決定1" in result

    @pytest.mark.asyncio
    async def test_after_runが何もしない(self) -> None:
        """after_run()が例外なく完了することを確認する（本Providerは何もしない）"""
        pool = _make_mock_pool()
        provider = TaskInheritanceContextProvider(db_pool=pool)
        # 例外が発生しないことを確認する
        result = await provider.after_run(task_uuid="test-uuid")
        assert result is None


# ========================================
# TestContextCompressionServiceMethods
# ========================================


class TestContextCompressionServiceMethods:
    """ContextCompressionServiceの詳細メソッドのテスト"""

    @pytest.mark.asyncio
    async def test_compress_messages_asyncが要約テキストを返す(self) -> None:
        """compress_messages_async()がLLMを呼び出し(summary, token_count)タプルを返すことを確認する"""
        mock_row = MagicMock()
        mock_row.__getitem__ = lambda self, key: {"role": "user", "content": "テストコンテンツ"}[key]
        pool = _make_mock_pool(fetch_return=[mock_row])

        mock_llm = MagicMock()
        mock_llm.generate = AsyncMock(return_value="要約テキスト")
        mock_config = MagicMock()

        service = ContextCompressionService(
            db_pool=pool,
            llm_client=mock_llm,
            config=mock_config,
        )

        summary, token_count = await service.compress_messages_async(
            task_uuid="test-uuid", start_seq=0, end_seq=5
        )

        assert summary == "要約テキスト"
        assert isinstance(token_count, int)
        assert token_count > 0
        mock_llm.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_replace_with_summary_asyncがトランザクションを実行する(self) -> None:
        """replace_with_summary_async()がDELETE・INSERT・UPDATE・INSERTをトランザクション内で実行することを確認する"""
        pool = MagicMock()
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        # conn.transaction()は同期メソッドとして非同期コンテキストマネージャを返す
        mock_txn_cm = MagicMock()
        mock_txn_cm.__aenter__ = AsyncMock(return_value=None)
        mock_txn_cm.__aexit__ = AsyncMock(return_value=False)
        mock_conn.transaction = MagicMock(return_value=mock_txn_cm)
        pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        pool.acquire.return_value.__aexit__ = AsyncMock(return_value=False)

        mock_config = MagicMock()
        service = ContextCompressionService(
            db_pool=pool,
            llm_client=MagicMock(),
            config=mock_config,
        )

        await service.replace_with_summary_async(
            task_uuid="test-uuid",
            summary="要約テキスト",
            start_seq=0,
            end_seq=5,
            original_tokens=100,
            compressed_tokens=30,
        )

        # execute が複数回呼ばれていることを確認する（DELETE・INSERT・UPDATE・INSERT）
        assert mock_conn.execute.call_count >= 4
        call_args_str = str(mock_conn.execute.call_args_list)
        assert "DELETE" in call_args_str
        assert "INSERT" in call_args_str
        assert "UPDATE" in call_args_str


# ========================================
# TestContextStorageManagerSaveError
# ========================================


class TestContextStorageManagerSaveError:
    """ContextStorageManager.save_error()のテスト"""

    @pytest.mark.asyncio
    async def test_save_errorがtask_repositoryを呼び出す(self) -> None:
        """save_error()がtask_repository.update_task_status()を呼び出すことを確認する"""
        mock_task_repo = AsyncMock()
        mock_task_repo.update_task_status = AsyncMock()

        manager = ContextStorageManager(
            chat_history_provider=MagicMock(),
            token_usage_repository=MagicMock(),
            context_repository=MagicMock(),
            task_repository=mock_task_repo,
        )

        await manager.save_error(
            task_uuid="test-uuid",
            node_id="node1",
            error_category="transient",
            error_message="テストエラー",
            stack_trace="Traceback ...",
        )

        mock_task_repo.update_task_status.assert_called_once_with(
            "test-uuid",
            "failed",
            error_message="テストエラー",
        )

    @pytest.mark.asyncio
    async def test_save_errorがtask_repositoryなしでも例外を出さない(self) -> None:
        """task_repositoryにupdate_task_statusがない場合でも例外なく完了することを確認する"""
        mock_task_repo = MagicMock(spec=[])  # specに空リストを渡してメソッドなしにする

        manager = ContextStorageManager(
            chat_history_provider=MagicMock(),
            token_usage_repository=MagicMock(),
            context_repository=MagicMock(),
            task_repository=mock_task_repo,
        )

        # 例外が発生しないことを確認する
        await manager.save_error(
            task_uuid="test-uuid",
            node_id="node1",
            error_category="implementation",
            error_message="テストエラー",
            stack_trace="",
        )
