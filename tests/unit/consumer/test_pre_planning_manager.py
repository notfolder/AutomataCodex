"""
PrePlanningManagerの単体テスト

LLMクライアントとMCPクライアントをモックして計画前情報収集フェーズの
タスク理解・環境情報収集・実行環境選択を検証する。
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from planning.pre_planning_manager import PrePlanningManager


# ========================================
# テスト用フィクスチャ
# ========================================


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """モックLLMクライアントを返す"""
    client = MagicMock()
    # generateメソッドをasyncで動作させる（デフォルトはpythonを選択）
    response = json.dumps(
        {"selected_environment": "python", "reasoning": "requirements.txtが存在するため"}
    )
    client.generate = AsyncMock(return_value=response)
    return client


@pytest.fixture
def mock_mcp_clients() -> dict[str, MagicMock]:
    """モックMCPクライアント辞書を返す"""
    text_editor = MagicMock()
    text_editor.call_tool.return_value = {"files": ["requirements.txt", "README.md"]}
    return {"text_editor": text_editor}


@pytest.fixture
def pre_planning_manager(
    mock_llm_client: MagicMock,
    mock_mcp_clients: dict[str, MagicMock],
) -> PrePlanningManager:
    """テスト用PrePlanningManagerを返す"""
    return PrePlanningManager(
        config={},
        llm_client=mock_llm_client,
        mcp_clients=mock_mcp_clients,
    )


# ========================================
# TestPrePlanningManagerExecute
# ========================================


class TestPrePlanningManagerExecute:
    """PrePlanningManager.execute()のテスト"""

    @pytest.mark.asyncio
    async def test_executeが全処理を実行して結果を返す(
        self,
        pre_planning_manager: PrePlanningManager,
    ) -> None:
        """モックされたllm_clientでexecute()が期待するキーを持つ辞書を返すことを確認する"""
        result = await pre_planning_manager.execute(
            task_uuid="test-uuid",
            task_description="Pythonでアプリを実装してください",
            plan_environment_id="plan-env-001",
        )

        # 期待するキーが全て含まれていることを確認する
        assert "understanding_result" in result
        assert "environment_info" in result
        assert "selected_environment" in result
        assert "selection_details" in result

    @pytest.mark.asyncio
    async def test_selected_environmentが有効な環境名を返す(
        self,
        pre_planning_manager: PrePlanningManager,
    ) -> None:
        """select_execution_environment()が有効な環境名を返すことを確認する"""
        valid_environments = {"python", "miniforge", "node", "default"}

        result = await pre_planning_manager.execute(
            task_uuid="test-uuid",
            task_description="環境選択テスト",
            plan_environment_id="plan-env-001",
        )

        assert result["selected_environment"] in valid_environments

    @pytest.mark.asyncio
    async def test_llm応答が無効な環境名の場合はdefaultを使用する(
        self,
        mock_mcp_clients: dict[str, MagicMock],
    ) -> None:
        """無効な環境名(例:"ruby")をLLMが返した場合に"default"が使用されることを確認する"""
        # LLMが無効な環境名を返すクライアントを作成する
        invalid_llm_client = MagicMock()
        # タスク理解用の呼び出しと環境選択用の呼び出しを分ける
        invalid_env_response = json.dumps(
            {"selected_environment": "ruby", "reasoning": "Rubyのプロジェクトのため"}
        )
        # generateが複数回呼ばれる場合、1回目はタスク理解、2回目は環境選択
        invalid_llm_client.generate = AsyncMock(
            side_effect=["タスク理解完了", invalid_env_response]
        )

        manager = PrePlanningManager(
            config={},
            llm_client=invalid_llm_client,
            mcp_clients=mock_mcp_clients,
        )

        result = await manager.execute(
            task_uuid="test-uuid",
            task_description="Rubyアプリを実装してください",
            plan_environment_id="plan-env-001",
        )

        # 無効な環境名が返された場合は"default"が使用されることを確認する
        assert result["selected_environment"] == "default"
