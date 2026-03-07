# エージェント定義ファイル 詳細設計書

## 1. 概要

エージェント定義ファイルはグラフ内の各エージェントノードの設定（ロール・ステップ間データキー・利用ツール・実行環境要否）をJSON形式で定義する。`workflow_definitions`テーブルの`agent_definition`カラム（JSONB型）に保存され、グラフ定義・プロンプト定義と1セットで管理される。

`AgentFactory`がこのJSONをパースし、各ノードの`ConfigurableAgent`インスタンス生成時に`AgentNodeConfig`として渡す。

## 2. DBへの保存形式

`workflow_definitions`テーブルの`agent_definition`カラムにJSONBとして保存する。

| カラム | 型 | 説明 |
|-------|------|------|
| agent_definition | JSONB NOT NULL | エージェント定義JSON（本仕様で定義する形式） |

グラフ定義・エージェント定義・プロンプト定義は同一テーブルの同一レコードに格納し、常に1セットで取得・更新する。

## 3. JSON形式の仕様

### 3.1 トップレベル構造

エージェント定義は以下のトップレベルフィールドを持つJSONオブジェクトである。

| フィールド | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `version` | 文字列 | 必須 | 定義フォーマットバージョン（例: "1.0"） |
| `agents` | オブジェクト配列 | 必須 | 各エージェントノードの定義配列（後述） |

### 3.2 エージェントノード定義（agents）

`agents`は各エージェントノードを定義するオブジェクトの配列である。

| フィールド | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `id` | 文字列 | 必須 | エージェントの一意識別子（グラフ定義の`agent_definition_id`と一致させる） |
| `role` | 文字列 | 必須 | エージェント役割（"planning" / "reflection" / "execution" / "review"） |
| `input_keys` | 文字列配列 | 必須 | ワークフローコンテキストから受け取るキー一覧 |
| `output_keys` | 文字列配列 | 必須 | ワークフローコンテキストへ書き込むキー一覧 |
| `tools` | 文字列配列 | 必須 | 利用するツール名一覧 |
| `prompt_id` | 文字列 | 必須 | プロンプト定義ファイル内の対応するプロンプトID |
| `max_iterations` | 整数 | 任意 | LLMとのターン数上限（デフォルト: 20） |
| `timeout_seconds` | 整数 | 任意 | タイムアウト秒数（デフォルト: 600） |
| `description` | 文字列 | 任意 | エージェントの説明文 |

**roleの値と処理内容**:

| role | 処理内容 |
|------|---------|
| `planning` | コンテキスト取得→LLM呼び出し（プランニング）→Todoリスト作成→GitLab投稿→コンテキスト保存 |
| `reflection` | プラン取得→LLM呼び出し（検証）→改善判定→GitLab投稿→コンテキスト保存 |
| `execution` | プラン取得→LLM呼び出し（実装/生成）→ファイル操作（MCPツール）→git操作→コンテキスト保存 |
| `review` | MR差分取得→LLM呼び出し（レビュー）→コメント生成→GitLab投稿→コンテキスト保存 |

**toolsに指定可能な値**:

| ツール名 | 説明 |
|---------|------|
| `text_editor` | ファイル読み書き操作（text-editor MCPサーバー） |
| `command_executor` | コマンド実行（command-executor MCPサーバー） |
| `create_todo_list` | Todoリスト作成（Agent Frameworkネイティブツール） |
| `get_todo_list` | Todoリスト取得（Agent Frameworkネイティブツール） |
| `update_todo_status` | Todo状態更新（Agent Frameworkネイティブツール） |
| `sync_to_gitlab` | GitLabへTodoリスト同期（Agent Frameworkネイティブツール） |

## 4. システムプリセット

### 4.1 標準MR処理エージェント定義（standard_mr_processing）

```json
{
  "version": "1.0",
  "agents": [
    {
      "id": "task_classifier",
      "role": "planning",
      "input_keys": ["task_context"],
      "output_keys": ["classification_result"],
      "tools": ["text_editor"],
      "prompt_id": "task_classifier",
      "max_iterations": 5,
      "timeout_seconds": 120,
      "description": "Issue/MRの内容を分析してタスク種別を判定する"
    },
    {
      "id": "code_generation_planning",
      "role": "planning",
      "input_keys": ["task_context", "classification_result"],
      "output_keys": ["plan_result", "todo_list"],
      "tools": ["text_editor", "create_todo_list", "sync_to_gitlab"],
      "prompt_id": "code_generation_planning",
      "max_iterations": 15,
      "timeout_seconds": 300,
      "description": "コード生成タスクの実行計画を生成する"
    },
    {
      "id": "bug_fix_planning",
      "role": "planning",
      "input_keys": ["task_context", "classification_result"],
      "output_keys": ["plan_result", "todo_list"],
      "tools": ["text_editor", "create_todo_list", "sync_to_gitlab"],
      "prompt_id": "bug_fix_planning",
      "max_iterations": 15,
      "timeout_seconds": 300,
      "description": "バグ修正タスクの実行計画を生成する"
    },
    {
      "id": "test_creation_planning",
      "role": "planning",
      "input_keys": ["task_context", "classification_result"],
      "output_keys": ["plan_result", "todo_list"],
      "tools": ["text_editor", "create_todo_list", "sync_to_gitlab"],
      "prompt_id": "test_creation_planning",
      "max_iterations": 15,
      "timeout_seconds": 300,
      "description": "テスト作成タスクの実行計画を生成する"
    },
    {
      "id": "documentation_planning",
      "role": "planning",
      "input_keys": ["task_context", "classification_result"],
      "output_keys": ["plan_result", "todo_list"],
      "tools": ["text_editor", "create_todo_list", "sync_to_gitlab"],
      "prompt_id": "documentation_planning",
      "max_iterations": 15,
      "timeout_seconds": 300,
      "description": "ドキュメント生成タスクの実行計画を生成する"
    },
    {
      "id": "plan_reflection",
      "role": "reflection",
      "input_keys": ["plan_result", "todo_list", "task_context"],
      "output_keys": ["reflection_result"],
      "tools": ["text_editor", "get_todo_list", "sync_to_gitlab"],
      "prompt_id": "plan_reflection",
      "max_iterations": 10,
      "timeout_seconds": 180,
      "description": "プランを検証し、問題点と改善案を提示する"
    },
    {
      "id": "code_generation",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "code_generation",
      "max_iterations": 40,
      "timeout_seconds": 1800,
      "description": "新規コードを生成する"
    },
    {
      "id": "bug_fix",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "bug_fix",
      "max_iterations": 40,
      "timeout_seconds": 1800,
      "description": "バグ修正を実装する"
    },
    {
      "id": "test_creation",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "test_creation",
      "max_iterations": 30,
      "timeout_seconds": 1200,
      "description": "テストコードを作成する"
    },
    {
      "id": "documentation",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result"],
      "tools": ["text_editor", "update_todo_status", "sync_to_gitlab"],
      "prompt_id": "documentation",
      "max_iterations": 30,
      "timeout_seconds": 900,
      "description": "ドキュメントを作成する"
    },
    {
      "id": "code_review",
      "role": "review",
      "input_keys": ["execution_result", "task_context"],
      "output_keys": ["review_result"],
      "tools": ["text_editor", "sync_to_gitlab"],
      "prompt_id": "code_review",
      "max_iterations": 10,
      "timeout_seconds": 300,
      "description": "コードレビューを実施する"
    },
    {
      "id": "documentation_review",
      "role": "review",
      "input_keys": ["execution_result", "task_context"],
      "output_keys": ["review_result"],
      "tools": ["text_editor", "sync_to_gitlab"],
      "prompt_id": "documentation_review",
      "max_iterations": 10,
      "timeout_seconds": 300,
      "description": "ドキュメントレビューを実施する"
    },
    {
      "id": "test_execution_evaluation",
      "role": "review",
      "input_keys": ["execution_result", "task_context"],
      "output_keys": ["review_result"],
      "tools": ["command_executor", "sync_to_gitlab"],
      "prompt_id": "test_execution_evaluation",
      "max_iterations": 15,
      "timeout_seconds": 600,
      "description": "テストを実行し結果を評価する"
    }
  ]
}
```

### 4.2 複数コード生成並列エージェント定義（multi_codegen_mr_processing）

コーディングエージェントを3種類の設定で並列実行する場合のエージェント定義。task_classifierからtest_execution_evaluationまで標準と共通の定義を継承し、以下を追加する。

```json
{
  "version": "1.0",
  "agents": [
    {
      "id": "code_generation_fast",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result_fast"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "code_generation_fast",
      "max_iterations": 30,
      "timeout_seconds": 900,
      "description": "高速モデルでコードを生成する"
    },
    {
      "id": "code_generation_standard",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result_standard"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "code_generation_standard",
      "max_iterations": 40,
      "timeout_seconds": 1800,
      "description": "標準モデルでコードを生成する"
    },
    {
      "id": "code_generation_creative",
      "role": "execution",
      "input_keys": ["plan_result", "task_context"],
      "output_keys": ["execution_result_creative"],
      "tools": [
        "text_editor",
        "command_executor",
        "update_todo_status",
        "sync_to_gitlab"
      ],
      "prompt_id": "code_generation_creative",
      "max_iterations": 40,
      "timeout_seconds": 1800,
      "description": "高温度設定で創造的なコードを生成する"
    },
    {
      "id": "code_review",
      "role": "review",
      "input_keys": [
        "execution_result_fast",
        "execution_result_standard",
        "execution_result_creative",
        "task_context"
      ],
      "output_keys": ["review_result"],
      "tools": ["text_editor", "sync_to_gitlab"],
      "prompt_id": "code_review_multi",
      "max_iterations": 15,
      "timeout_seconds": 600,
      "description": "3種類のコード生成結果を比較レビューする"
    },
    {
      "id": "plan_reflection",
      "role": "reflection",
      "input_keys": ["review_result", "task_context"],
      "output_keys": ["reflection_result"],
      "tools": ["text_editor", "sync_to_gitlab"],
      "prompt_id": "plan_reflection",
      "max_iterations": 10,
      "timeout_seconds": 180,
      "description": "レビュー結果を評価し再計画の要否を判断する"
    }
  ]
}
```

## 5. コンテキストキー一覧

ステップ間でワークフローコンテキストを通じてやり取りするキーの定義。

| キー名 | 型 | 説明 | 設定エージェント定義ID |
|-------|------|------|------|
| `task_context` | TaskContext | タスク共通情報（UUID・MR情報・ユーザー情報） | UserResolverExecutor |
| `classification_result` | ClassificationResult | タスク種別・関連ファイル・仕様書情報 | task_classifier |
| `plan_result` | PlanResult | 実行計画・仕様書有無フラグ | *_planning |
| `todo_list` | TodoList | Todoリスト | *_planning |
| `execution_result` | ExecutionResult | 実装・ドキュメント作成結果 | code_generation / bug_fix / test_creation / documentation |
| `execution_result_fast` | ExecutionResult | 高速モデルによる実装結果 | code_generation_fast |
| `execution_result_standard` | ExecutionResult | 標準モデルによる実装結果 | code_generation_standard |
| `execution_result_creative` | ExecutionResult | 高温度モデルによる実装結果 | code_generation_creative |
| `reflection_result` | ReflectionResult | プラン検証結果・再計画判断 | plan_reflection |
| `review_result` | ReviewResult | レビュー結果・指摘事項 | code_review / documentation_review / test_execution_evaluation |

**複数エージェントが並列出力する場合のキー命名規則**:

並列実行ノードが同じコンテキストキー名に出力すると上書きが発生するため、並列ノードの`output_keys`には必ずサフィックスを付与して区別する。命名規則は`{基本キー名}_{エージェントID末尾部分}`とする。例: `code_generation_fast`エージェントの出力は`execution_result_fast`とする。後続の集約ノード（レビュー等）の`input_keys`にはすべての並列ノードの出力キーを列挙する。

## 6. バリデーション仕様

`DefinitionLoader.validate_agent_definition(agent_def, graph_def)`が以下のチェックを実施する。

| チェック項目 | 説明 |
|-----------|------|
| 必須フィールドの存在 | `version`・`agents`の存在確認 |
| 各エージェントの必須フィールド | `id`・`role`・`input_keys`・`output_keys`・`tools`・`prompt_id`の存在確認 |
| グラフ定義との整合性 | グラフ定義で参照される`agent_definition_id`すべてについて対応するエージェント定義が存在するか |
| roleの有効値 | "planning" / "reflection" / "execution" / "review"のいずれかであるか |
| toolsの有効値 | 登録可能なツール名一覧に含まれるかどうか |
