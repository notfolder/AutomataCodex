"""
ConfigurableAgentの単体テスト

AgentNodeConfig・WorkflowContext・ProgressReporterをモックして
ConfigurableAgentのhandle()・store_result()・invoke_mcp_tool()を検証する。
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from agents.configurable_agent import ConfigurableAgent, WorkflowContext
from shared.models.agent_definition import AgentNodeConfig


# ========================================
# テスト用フィクスチャ
# ========================================


def _make_agent_node_config(
    role: str = "planning",
    input_keys: list[str] | None = None,
    output_keys: list[str] | None = None,
    mcp_servers: list[str] | None = None,
) -> AgentNodeConfig:
    """テスト用AgentNodeConfigを生成する"""
    return AgentNodeConfig(
        id="test-agent-node",
        role=role,
        input_keys=input_keys or ["task_description"],
        output_keys=output_keys or ["planning_result"],
        mcp_servers=mcp_servers or ["text_editor"],
        prompt_id="test-prompt",
    )


class _ConcreteWorkflowContext(WorkflowContext):
    """テスト用WorkflowContextの具象クラス"""

    def __init__(self) -> None:
        self._state: dict = {}

    async def get_state(self, key: str):
        return self._state.get(key)

    async def set_state(self, key: str, value) -> None:
        self._state[key] = value


@pytest.fixture
def agent_config() -> AgentNodeConfig:
    """テスト用AgentNodeConfigを返す"""
    return _make_agent_node_config()


@pytest.fixture
def mock_ctx() -> _ConcreteWorkflowContext:
    """テスト用WorkflowContextを返す"""
    ctx = _ConcreteWorkflowContext()
    ctx._state = {
        "task_mr_iid": 42,
        "task_description": "テストタスクの説明",
    }
    return ctx


@pytest.fixture
def mock_agent() -> MagicMock:
    """モックエージェント（LLMエージェント）を返す"""
    agent = MagicMock()
    agent.run = AsyncMock(return_value="LLMの応答テキスト")
    return agent


@pytest.fixture
def mock_progress_reporter() -> MagicMock:
    """モック進捗レポーターを返す"""
    reporter = MagicMock()
    reporter.report_progress = AsyncMock()
    return reporter


@pytest.fixture
def configurable_agent(
    agent_config: AgentNodeConfig,
    mock_agent: MagicMock,
    mock_progress_reporter: MagicMock,
) -> ConfigurableAgent:
    """テスト用ConfigurableAgentを返す"""
    return ConfigurableAgent(
        config=agent_config,
        agent=mock_agent,
        prompt_content="タスク: {task_description}",
        progress_reporter=mock_progress_reporter,
    )


# ========================================
# TestConfigurableAgentHandle
# ========================================


class TestConfigurableAgentHandle:
    """ConfigurableAgent.handle()のテスト"""

    @pytest.mark.asyncio
    async def test_handleが入力データを取得してプロンプトを生成する(
        self,
        configurable_agent: ConfigurableAgent,
        mock_ctx: _ConcreteWorkflowContext,
        mock_agent: MagicMock,
    ) -> None:
        """handle()を実行し、入力データが正しく取得されてagent.run()が呼ばれることを確認する"""
        result = await configurable_agent.handle(msg={}, ctx=mock_ctx)

        # agent.run()が呼ばれていることを確認する
        mock_agent.run.assert_called_once()
        # 出力データが返されることを確認する
        assert isinstance(result, dict)
        assert "planning_result" in result

    @pytest.mark.asyncio
    @pytest.mark.parametrize("role", ["planning", "execution", "reflection", "review"])
    async def test_handleがroleに応じた後処理を実行する(
        self,
        role: str,
        mock_agent: MagicMock,
        mock_progress_reporter: MagicMock,
        mock_ctx: _ConcreteWorkflowContext,
    ) -> None:
        """roleが各値の場合にエラーなくhandle()が実行されることを確認する"""
        config = _make_agent_node_config(role=role)
        agent = ConfigurableAgent(
            config=config,
            agent=mock_agent,
            prompt_content="タスク: {task_description}",
            progress_reporter=mock_progress_reporter,
        )

        # 例外が発生しないことを確認する
        result = await agent.handle(msg={}, ctx=mock_ctx)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_進捗報告がstart_llm_response_completeの順に呼び出される(
        self,
        configurable_agent: ConfigurableAgent,
        mock_ctx: _ConcreteWorkflowContext,
        mock_progress_reporter: MagicMock,
    ) -> None:
        """progress_reporter.report_progressが3回呼び出されることを確認する"""
        await configurable_agent.handle(msg={}, ctx=mock_ctx)

        # start・llm_response・completeの3回呼ばれることを確認する
        assert mock_progress_reporter.report_progress.call_count == 3

        # 呼び出し順序を確認する
        calls = mock_progress_reporter.report_progress.call_args_list
        events = [c.kwargs.get("event") or c.args[1] if c.args else c.kwargs.get("event") for c in calls]
        # call_argsはkeyword-onlyなので kwargs で確認する
        event_values = [c.kwargs["event"] for c in calls]
        assert event_values[0] == "start"
        assert event_values[1] == "llm_response"
        assert event_values[2] == "complete"

    @pytest.mark.asyncio
    async def test_エラー発生時にevent_errorで進捗報告する(
        self,
        agent_config: AgentNodeConfig,
        mock_progress_reporter: MagicMock,
        mock_ctx: _ConcreteWorkflowContext,
    ) -> None:
        """handle()内でエラーが発生した場合にevent='error'で報告されることを確認する"""
        # agent.run()が例外をスローするモックを作成する
        error_agent = MagicMock()
        error_agent.run = AsyncMock(side_effect=RuntimeError("テストエラー"))

        agent = ConfigurableAgent(
            config=agent_config,
            agent=error_agent,
            prompt_content="テスト",
            progress_reporter=mock_progress_reporter,
        )

        with pytest.raises(RuntimeError, match="テストエラー"):
            await agent.handle(msg={}, ctx=mock_ctx)

        # エラー進捗報告が呼ばれていることを確認する
        error_calls = [
            c for c in mock_progress_reporter.report_progress.call_args_list
            if c.kwargs.get("event") == "error"
        ]
        assert len(error_calls) == 1


# ========================================
# TestConfigurableAgentMethods
# ========================================


class TestConfigurableAgentMethods:
    """ConfigurableAgentのユーティリティメソッドのテスト"""

    @pytest.mark.asyncio
    async def test_invoke_mcp_toolで未登録ツールはValueErrorが発生する(
        self,
        configurable_agent: ConfigurableAgent,
    ) -> None:
        """config.mcp_serversに含まれないツール名でValueErrorが発生することを確認する"""
        with pytest.raises(ValueError, match="登録されていません"):
            await configurable_agent.invoke_mcp_tool(
                tool_name="unregistered_tool",
                params={"key": "value"},
            )

    @pytest.mark.asyncio
    async def test_store_resultがcontextにoutput_keysを保存する(
        self,
        configurable_agent: ConfigurableAgent,
        mock_ctx: _ConcreteWorkflowContext,
    ) -> None:
        """store_result()がctx.set_state()を正しく呼び出すことを確認する"""
        output_keys = ["planning_result"]
        result_data = {"planning_result": "生成されたプラン"}

        await configurable_agent.store_result(
            output_keys=output_keys,
            result=result_data,
            ctx=mock_ctx,
        )

        # contextに保存されていることを確認する
        saved_value = await mock_ctx.get_state("planning_result")
        assert saved_value == "生成されたプラン"
