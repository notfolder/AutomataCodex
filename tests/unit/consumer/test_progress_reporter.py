"""
ProgressReporter 関連クラス群の単体テスト

MermaidGraphRenderer・ProgressCommentManager・ProgressReporter の
各メソッドを検証する。
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from agents.configurable_agent import WorkflowContext
from tools.mermaid_graph_renderer import MermaidGraphRenderer
from tools.progress_comment_manager import ProgressCommentManager
from tools.progress_reporter import ProgressReporter


# ========================================
# テスト用ヘルパークラス
# ========================================


class _ConcreteWorkflowContext(WorkflowContext):
    """テスト用WorkflowContextの具象クラス"""

    def __init__(self) -> None:
        self._state: dict = {}

    async def get_state(self, key: str):
        """指定キーの状態値を返す"""
        return self._state.get(key)

    async def set_state(self, key: str, value) -> None:
        """指定キーに値を保存する"""
        self._state[key] = value


# ========================================
# フィクスチャ
# ========================================


@pytest.fixture
def mock_ctx() -> _ConcreteWorkflowContext:
    """テスト用WorkflowContextを返す"""
    ctx = _ConcreteWorkflowContext()
    ctx._state = {
        "project_id": 10,
        "task_mr_iid": 5,
    }
    return ctx


@pytest.fixture
def simple_graph_def() -> dict:
    """テスト用の単純なグラフ定義を返す"""
    return {
        "nodes": [
            {"id": "node_a", "label": "ノードA", "type": "agent"},
            {"id": "node_b", "label": "ノードB", "type": "executor"},
        ],
        "edges": [
            {"from": "node_a", "to": "node_b"},
        ],
    }


@pytest.fixture
def mock_gitlab_client() -> MagicMock:
    """テスト用GitlabClientモックを返す"""
    client = MagicMock()
    # create_merge_request_noteはnote_idを返す
    client.create_merge_request_note.return_value = 123
    return client


@pytest.fixture
def mermaid_renderer(simple_graph_def: dict) -> MermaidGraphRenderer:
    """テスト用MermaidGraphRendererを返す"""
    return MermaidGraphRenderer(graph_def=simple_graph_def)


@pytest.fixture
def mock_mermaid_renderer() -> MagicMock:
    """モックMermaidGraphRendererを返す"""
    renderer = MagicMock(spec=MermaidGraphRenderer)
    renderer.render.return_value = "flowchart TD\n  node_a --> node_b"
    return renderer


# ========================================
# TestMermaidGraphRenderer
# ========================================


class TestMermaidGraphRenderer:
    """MermaidGraphRenderer.render() のテスト"""

    def test_mermaid_renderer_basic(
        self,
        simple_graph_def: dict,
    ) -> None:
        """単純なグラフ定義でrenderを呼び出し、flowchart TDと各ノードのIDが含まれることを確認する"""
        renderer = MermaidGraphRenderer(graph_def=simple_graph_def)
        node_states = {"node_a": "pending", "node_b": "pending"}

        result = renderer.render(node_states)

        # flowchart TD が先頭に含まれることを確認する
        assert result.startswith("flowchart TD")
        # 各ノードIDが含まれることを確認する
        assert "node_a" in result
        assert "node_b" in result
        # エッジの矢印が含まれることを確認する
        assert "-->" in result

    def test_mermaid_renderer_node_states(
        self,
        simple_graph_def: dict,
    ) -> None:
        """異なるnode_states（running/done/error等）でclassDefが出力されることを確認する"""
        renderer = MermaidGraphRenderer(graph_def=simple_graph_def)
        node_states = {"node_a": "running", "node_b": "done"}

        result = renderer.render(node_states)

        # 使用されている状態のクラスが出力されることを確認する
        assert "classDef" in result
        # running と done に対応する classDef が含まれることを確認する
        assert "running" in result
        assert "done" in result
        # ノード定義に状態クラスが付いていることを確認する（:::state 記法）
        assert ":::running" in result
        assert ":::done" in result


# ========================================
# TestProgressCommentManager
# ========================================


class TestProgressCommentManager:
    """ProgressCommentManager のテスト"""

    async def test_progress_comment_manager_create(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        mock_gitlab_client: MagicMock,
        mock_mermaid_renderer: MagicMock,
    ) -> None:
        """create_progress_commentがgitlab_clientを呼びnote_idを返すことを確認する"""
        manager = ProgressCommentManager(
            gitlab_client=mock_gitlab_client,
            mermaid_renderer=mock_mermaid_renderer,
        )
        node_states = {"node_a": "pending", "node_b": "pending"}

        note_id = await manager.create_progress_comment(
            context=mock_ctx,
            mr_iid=5,
            node_states=node_states,
        )

        # create_merge_request_noteが呼ばれることを確認する
        mock_gitlab_client.create_merge_request_note.assert_called_once()
        # note_idが返されることを確認する
        assert note_id == 123
        # コンテキストにprogress_comment_idが保存されることを確認する
        assert mock_ctx._state["progress_comment_id"] == 123

    async def test_progress_comment_manager_update(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        mock_gitlab_client: MagicMock,
        mock_mermaid_renderer: MagicMock,
    ) -> None:
        """update_progress_commentがgitlab_client.update_merge_request_noteを呼ぶことを確認する"""
        manager = ProgressCommentManager(
            gitlab_client=mock_gitlab_client,
            mermaid_renderer=mock_mermaid_renderer,
        )
        # コンテキストにnote_idを設定する
        mock_ctx._state["progress_comment_id"] = 123
        # スロットリングを回避するために最終更新時刻を0に設定する
        manager.last_update_time = 0.0

        node_states = {"node_a": "running", "node_b": "pending"}

        await manager.update_progress_comment(
            context=mock_ctx,
            mr_iid=5,
            node_states=node_states,
            event_summary="⏳ ノードA 処理を開始します",
            llm_response="",
            error_detail=None,
        )

        # update_merge_request_noteが呼ばれることを確認する
        mock_gitlab_client.update_merge_request_note.assert_called_once()
        call_args = mock_gitlab_client.update_merge_request_note.call_args
        # project_id, mr_iid, note_id が正しいことを確認する
        assert call_args.args[0] == 10  # project_id
        assert call_args.args[1] == 5   # mr_iid
        assert call_args.args[2] == 123  # note_id


# ========================================
# TestProgressReporter
# ========================================


class TestProgressReporter:
    """ProgressReporter のテスト"""

    @pytest.fixture
    def mock_comment_manager(self) -> MagicMock:
        """テスト用ProgressCommentManagerモックを返す"""
        manager = MagicMock()
        manager.create_progress_comment = AsyncMock(return_value=99)
        manager.update_progress_comment = AsyncMock()
        return manager

    @pytest.fixture
    def progress_reporter(
        self,
        simple_graph_def: dict,
        mock_mermaid_renderer: MagicMock,
        mock_comment_manager: MagicMock,
    ) -> ProgressReporter:
        """テスト用ProgressReporterを返す"""
        return ProgressReporter(
            graph_def=simple_graph_def,
            mermaid_renderer=mock_mermaid_renderer,
            comment_manager=mock_comment_manager,
        )

    async def test_progress_reporter_initialize(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        progress_reporter: ProgressReporter,
        mock_comment_manager: MagicMock,
    ) -> None:
        """initializeがcreate_progress_commentを呼び、全ノードがpendingになることを確認する"""
        await progress_reporter.initialize(context=mock_ctx, mr_iid=5)

        # 全ノードがpendingで初期化されることを確認する
        assert progress_reporter.node_states["node_a"] == "pending"
        assert progress_reporter.node_states["node_b"] == "pending"
        # create_progress_commentが呼ばれることを確認する
        mock_comment_manager.create_progress_comment.assert_called_once()

    async def test_progress_reporter_report_start_event(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        progress_reporter: ProgressReporter,
        mock_comment_manager: MagicMock,
    ) -> None:
        """start eventでノード状態がrunningになることを確認する"""
        # 事前に全ノードをpendingで初期化する
        progress_reporter.node_states = {"node_a": "pending", "node_b": "pending"}

        await progress_reporter.report_progress(
            context=mock_ctx,
            event="start",
            node_id="node_a",
            details={},
        )

        # node_aがrunning状態になることを確認する
        assert progress_reporter.node_states["node_a"] == "running"
        # コメント更新が呼ばれることを確認する
        mock_comment_manager.update_progress_comment.assert_called_once()

    async def test_progress_reporter_report_complete_event(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        progress_reporter: ProgressReporter,
        mock_comment_manager: MagicMock,
    ) -> None:
        """complete eventでノード状態がdoneになることを確認する"""
        progress_reporter.node_states = {"node_a": "running", "node_b": "pending"}

        await progress_reporter.report_progress(
            context=mock_ctx,
            event="complete",
            node_id="node_a",
            details={"elapsed": 3.5},
        )

        # node_aがdone状態になることを確認する
        assert progress_reporter.node_states["node_a"] == "done"
        mock_comment_manager.update_progress_comment.assert_called_once()

    async def test_progress_reporter_finalize(
        self,
        mock_ctx: _ConcreteWorkflowContext,
        progress_reporter: ProgressReporter,
        mock_comment_manager: MagicMock,
    ) -> None:
        """finalizeで残りのノードがdoneになることを確認する"""
        # node_aはdone、node_bはpendingの状態にする
        progress_reporter.node_states = {"node_a": "done", "node_b": "pending"}

        await progress_reporter.finalize(
            context=mock_ctx,
            mr_iid=5,
            summary="全タスク完了",
        )

        # pendingのnode_bもdoneになることを確認する
        assert progress_reporter.node_states["node_a"] == "done"
        assert progress_reporter.node_states["node_b"] == "done"
        # 最終コメント更新が呼ばれることを確認する
        mock_comment_manager.update_progress_comment.assert_called_once()
        # event_summaryに完了文字列が含まれることを確認する
        assert "全タスク完了" in progress_reporter.latest_event_summary
