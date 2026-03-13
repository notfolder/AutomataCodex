"""
TodoManagementTool モジュール

PostgreSQL を使った Todo リスト管理ツールクラスを定義する。
LLM エージェントが FunctionTool として呼び出せるインターフェースを提供し、
PostgreSQL への直接操作を担う。

CLASS_IMPLEMENTATION_SPEC.md § 10.1（TodoManagementTool）に準拠する。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from shared.gitlab_client.gitlab_client import GitlabClient

logger = logging.getLogger(__name__)

# Todo ステータス定数
_STATUS_COMPLETED = "completed"

# Markdown チェックボックスの文字列
_CHECK_DONE = "[x]"
_CHECK_TODO = "[ ]"


def _todo_to_checkbox(status: str) -> str:
    """
    Todo のステータスを Markdown チェックボックス文字列に変換する。

    Args:
        status: Todo のステータス文字列

    Returns:
        "[x]"（completed）または "[ ]"（その他）
    """
    return _CHECK_DONE if status == _STATUS_COMPLETED else _CHECK_TODO


class TodoManagementTool:
    """
    PostgreSQL Todo リスト管理ツール。

    LLM エージェントの FunctionTool として機能し、
    PostgreSQL の todos テーブルへの直接操作と
    GitLab MR へのコメント同期を担う。

    CLASS_IMPLEMENTATION_SPEC.md § 10.1 に準拠する。

    Attributes:
        db_connection: asyncpg の Connection または Pool
        gitlab_client: GitLab API クライアント
        task_uuid: 現在のタスクを識別する UUID 文字列
    """

    def __init__(
        self,
        db_connection: Any,
        gitlab_client: "GitlabClient",
        task_uuid: str,
    ) -> None:
        """
        初期化。

        Args:
            db_connection: asyncpg.Connection または asyncpg.Pool
            gitlab_client: GitLab API クライアント
            task_uuid: 現在のタスク UUID（各タスク実行コンテキストで一意）
        """
        self.db_connection = db_connection
        self.gitlab_client = gitlab_client
        self.task_uuid = task_uuid

    async def create_todo_list(
        self,
        project_id: int,
        mr_iid: int,
        todos: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Todo リストを PostgreSQL に一括登録する。

        todos の各要素を todos テーブルに INSERT し、
        生成された todo_id のリストを返す。

        Args:
            project_id: GitLab プロジェクト ID（将来の拡張用）
            mr_iid: MergeRequest IID（将来の拡張用）
            todos: 登録する Todo 情報のリスト
                各要素: {"title": str, "description": str (optional),
                          "status": str (optional), "parent_todo_id": int (optional)}

        Returns:
            {"status": "success", "todo_ids": [id1, id2, ...]}
        """
        todo_ids: list[int] = []

        for order_index, todo in enumerate(todos):
            title: str = todo.get("title", "")
            description: str = todo.get("description", "")
            status: str = todo.get("status", "not-started")

            # todos テーブルに INSERT して生成された ID を取得する
            row = await self.db_connection.fetchrow(
                """
                INSERT INTO todos
                    (task_uuid, title, description, status, order_index)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
                """,
                self.task_uuid,
                title,
                description,
                status,
                order_index,
            )
            todo_id: int = row["id"]
            todo_ids.append(todo_id)
            logger.debug(
                "Todo登録: task_uuid=%s, todo_id=%d, title=%s",
                self.task_uuid,
                todo_id,
                title,
            )

        logger.info(
            "Todoリスト登録完了: task_uuid=%s, 件数=%d",
            self.task_uuid,
            len(todo_ids),
        )
        return {"status": "success", "todo_ids": todo_ids}

    async def sync_to_gitlab(
        self,
        project_id: int,
        mr_iid: int,
        task_uuid: str | None = None,
    ) -> dict[str, Any]:
        """
        PostgreSQL の Todo リストを Markdown 形式に変換して GitLab MR にコメント投稿する。

        親子関係を考慮した階層構造の Markdown チェックリストを生成する。

        Args:
            project_id: GitLab プロジェクト ID
            mr_iid: MergeRequest IID
            task_uuid: 取得対象のタスク UUID（省略時は self.task_uuid を使用）

        Returns:
            {"status": "success"}
        """
        target_uuid = task_uuid if task_uuid is not None else self.task_uuid

        # ① PostgreSQL から Todo 一覧を取得する
        rows = await self.db_connection.fetch(
            """
            SELECT id, title, status, parent_todo_id
            FROM todos
            WHERE task_uuid = $1
            ORDER BY order_index
            """,
            target_uuid,
        )

        # ② 親子関係を考慮して Markdown 形式に変換する
        # まず全 todo を id でインデックス化する
        todo_by_id: dict[int, dict[str, Any]] = {
            row["id"]: dict(row) for row in rows
        }

        # 親ノードごとに子ノードをまとめる
        children_map: dict[int | None, list[dict[str, Any]]] = {}
        for todo in todo_by_id.values():
            parent_id: int | None = todo.get("parent_todo_id")
            children_map.setdefault(parent_id, []).append(todo)

        lines: list[str] = ["## 📋 Todo リスト", ""]

        def _render_todos(
            parent_id: int | None,
            indent_level: int,
        ) -> None:
            """再帰的に Todo を Markdown 形式で出力する。"""
            for todo in children_map.get(parent_id, []):
                checkbox = _todo_to_checkbox(todo["status"])
                indent = "  " * indent_level
                lines.append(f"{indent}- {checkbox} {todo['title']}")
                # 子 Todo を再帰的に処理する
                _render_todos(todo["id"], indent_level + 1)

        _render_todos(None, 0)

        markdown_content = "\n".join(lines)

        # ③ GitLab MR にコメントとして投稿する
        self.gitlab_client.create_merge_request_note(
            project_id, mr_iid, markdown_content
        )
        logger.info(
            "TodoリストをGitLabに同期: project_id=%d, mr_iid=%d, task_uuid=%s",
            project_id,
            mr_iid,
            target_uuid,
        )

        return {"status": "success"}
