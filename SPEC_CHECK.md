# 仕様書チェックレポート (SPEC_CHECK.md)

本ドキュメントは以下16ファイルを対象に3つの観点でチェックを実施した結果を報告する。

## 対象ファイル

| # | ファイル | 行数 |
|---|---------|------|
| 1 | AUTOMATA_CODEX_SPEC.md | 4068 |
| 2 | CLASS_IMPLEMENTATION_SPEC.md | 2060 |
| 3 | USER_MANAGEMENT_SPEC.md | 1239 |
| 4 | PROMPTS.md | 914 |
| 5 | PROMPT_DEFINITION_SPEC.md | 280 |
| 6 | STANDARD_MR_PROCESSING_FLOW.md | 862 |
| 7 | DATABASE_SCHEMA_SPEC.md | 1080 |
| 8 | AGENT_DEFINITION_SPEC.md | 933 |
| 9 | GRAPH_DEFINITION_SPEC.md | 834 |
| 10 | MULTI_MR_PROCESSING_FLOW.md | 413 |
| 11 | definitions/standard_mr_processing_agents.json | 268 |
| 12 | definitions/standard_mr_processing_graph.json | 484 |
| 13 | definitions/standard_mr_processing_prompts.json | 154 |
| 14 | definitions/multi_codegen_mr_processing_agents.json | 290 |
| 15 | definitions/multi_codegen_mr_processing_graph.json | 526 |
| 16 | definitions/multi_codegen_mr_processing_prompts.json | 174 |

---

## チェック観点1：ドキュメント間の矛盾チェック

各章ごとに関連するドキュメント/章をリストし、矛盾の有無を報告する。

### AUTOMATA_CODEX_SPEC.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 目的と範囲 | STANDARD_MR_PROCESSING_FLOW.md §1, MULTI_MR_PROCESSING_FLOW.md §1 | 問題なし |
| §2 システムアーキテクチャ | CLASS_IMPLEMENTATION_SPEC.md §2, DATABASE_SCHEMA_SPEC.md §1, STANDARD_MR_PROCESSING_FLOW.md §3 | 問題なし |
| §3 ユーザー管理システム | USER_MANAGEMENT_SPEC.md, DATABASE_SCHEMA_SPEC.md §2 | 問題なし |
| §4.1 Factory設計（WorkflowFactory）| CLASS_IMPLEMENTATION_SPEC.md §2.1 | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §4.4.2 で WorkflowFactory の主要メソッドとして `_inject_learning_node()` が明記されているが、CLASS_IMPLEMENTATION_SPEC.md §2.1 WorkflowFactory の主要メソッド一覧に `_inject_learning_node()` が記載されていない |
| §4.2 ExecutorFactory | CLASS_IMPLEMENTATION_SPEC.md §2.2 | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §4.4.2 で ExecutorFactory の主要メソッドとして `create_branch_merge(context)` が明記されているが、CLASS_IMPLEMENTATION_SPEC.md §2.2 の主要メソッド一覧に `create_branch_merge()` が記載されていない |
| §4.3.1 ConfigurableAgent 共通設計 | CLASS_IMPLEMENTATION_SPEC.md §1, AGENT_DEFINITION_SPEC.md §3 | 問題なし |
| §4.3.2 エージェントノード一覧 | AGENT_DEFINITION_SPEC.md §6, STANDARD_MR_PROCESSING_FLOW.md §2 | 問題なし |
| §4.4 定義ファイル管理（DefinitionLoader）| GRAPH_DEFINITION_SPEC.md, AGENT_DEFINITION_SPEC.md, PROMPT_DEFINITION_SPEC.md | 問題なし |
| §4.5 ブランチ管理 | MULTI_MR_PROCESSING_FLOW.md §4.3, §4.6 | 問題なし |
| §5.0 Issue→MR変換フロー | CLASS_IMPLEMENTATION_SPEC.md §3.3（ContentTransferExecutor） | 問題なし |
| §5.1 オブジェクト構造設計 | CLASS_IMPLEMENTATION_SPEC.md §4（Custom Provider群） | 問題なし |
| §6 進捗報告機能（ProgressReporter）| CLASS_IMPLEMENTATION_SPEC.md | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §6 では ProgressReporter クラスが詳述されているが、CLASS_IMPLEMENTATION_SPEC.md には ProgressReporter の独立した設計章が存在しない（§8のその他主要クラスに含まれる可能性あり） |
| §7 GitLab API 操作設計（GitLabClient）| CLASS_IMPLEMENTATION_SPEC.md | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §7.2 で GitLabClient クラスの責務と主要メソッドグループが記載されているが、CLASS_IMPLEMENTATION_SPEC.md に GitLabClient の独立した詳細設計章が存在しない |
| §8.3 Agent Framework標準Providerのカスタム実装 | CLASS_IMPLEMENTATION_SPEC.md §4 | 問題なし |
| §8.5 コンテキスト圧縮 | CLASS_IMPLEMENTATION_SPEC.md §4.4（ContextCompressionService）, DATABASE_SCHEMA_SPEC.md §2.2（user_configsテーブル） | 問題なし |
| §8.6 コンテキスト継承 | CLASS_IMPLEMENTATION_SPEC.md §8（その他主要クラス: TaskInheritanceContextProvider） | 問題なし |
| §8.7 ワークフロー状態管理 | CLASS_IMPLEMENTATION_SPEC.md §2.1（WorkflowFactory停止・再開関連）, DATABASE_SCHEMA_SPEC.md §5（workflow_execution_statesテーブル） | 問題なし |
| §8.8 実行環境管理（ExecutionEnvironmentManager）| CLASS_IMPLEMENTATION_SPEC.md §6 | 問題なし |
| §8.9 Middleware機構 | CLASS_IMPLEMENTATION_SPEC.md §5 | 問題なし |
| §9 Tool管理設計 (MCP) | CLASS_IMPLEMENTATION_SPEC.md §9（MCPClient関連）, AGENT_DEFINITION_SPEC.md §3.2（mcp_serversフィールド） | 問題なし |
| §10 エラー処理設計 | STANDARD_MR_PROCESSING_FLOW.md §4.3（リトライポリシー）, CLASS_IMPLEMENTATION_SPEC.md §5.4（ErrorHandlingMiddleware） | 問題なし |
| §11 学習機能（GuidelineLearningAgent）| CLASS_IMPLEMENTATION_SPEC.md §10, DATABASE_SCHEMA_SPEC.md §2.2（user_configsテーブルlearning_*カラム） | 問題なし |
| §12 セキュリティ設計 | USER_MANAGEMENT_SPEC.md, DATABASE_SCHEMA_SPEC.md | 問題なし |
| §13 運用設計 | DATABASE_SCHEMA_SPEC.md §5（workflow_execution_states）, CLASS_IMPLEMENTATION_SPEC.md §2.1（resume_workflow） | 問題なし |
| §14 設定ファイル定義（config.yaml）| CLASS_IMPLEMENTATION_SPEC.md全体 | 問題なし |

### CLASS_IMPLEMENTATION_SPEC.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 ConfigurableAgent | AUTOMATA_CODEX_SPEC.md §4.3.1, AGENT_DEFINITION_SPEC.md §3 | 問題なし |
| §1.4 handle() メソッド | AUTOMATA_CODEX_SPEC.md §4.3.1 | 問題なし |
| §2.1 WorkflowFactory | AUTOMATA_CODEX_SPEC.md §4.4.2 | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §4.4.2 に記載の `_inject_learning_node()` メソッドが CLASS_IMPLEMENTATION_SPEC.md §2.1 の主要メソッド一覧に存在しない |
| §2.2 ExecutorFactory | AUTOMATA_CODEX_SPEC.md §4.4.2 | **矛盾あり**: AUTOMATA_CODEX_SPEC.md §4.4.2 に記載の `create_branch_merge()` が CLASS_IMPLEMENTATION_SPEC.md §2.2 に存在しない |
| §2.3 AgentFactory | AUTOMATA_CODEX_SPEC.md §4.4.3, AGENT_DEFINITION_SPEC.md | 問題なし |
| §2.4 MCPClientFactory | AUTOMATA_CODEX_SPEC.md §4.4.4 | 問題なし |
| §2.5 TaskStrategyFactory | AUTOMATA_CODEX_SPEC.md §5.0 | 問題なし |
| §3 Executor群 | AUTOMATA_CODEX_SPEC.md §4.3.2, GRAPH_DEFINITION_SPEC.md §3.2 | 問題なし |
| §3.4 PlanEnvSetupExecutor | AUTOMATA_CODEX_SPEC.md §4.3.2, STANDARD_MR_PROCESSING_FLOW.md §3 | 問題なし |
| §3.5 ExecEnvSetupExecutor | AUTOMATA_CODEX_SPEC.md §4.3.2, GRAPH_DEFINITION_SPEC.md §3.2（env_count）| 問題なし |
| §4 Custom Provider群 | AUTOMATA_CODEX_SPEC.md §8.3, DATABASE_SCHEMA_SPEC.md | 問題なし |
| §4.4 ContextCompressionService | AUTOMATA_CODEX_SPEC.md §8.5, DATABASE_SCHEMA_SPEC.md §2.2（user_configsテーブル）| 問題なし |
| §5 Middleware実装 | AUTOMATA_CODEX_SPEC.md §8.9, GRAPH_DEFINITION_SPEC.md §3.2（metadata.check_comments_before）| 問題なし |
| §6 ExecutionEnvironmentManager | AUTOMATA_CODEX_SPEC.md §8.8, STANDARD_MR_PROCESSING_FLOW.md §3 | 問題なし |
| §7 EnvironmentAnalyzer | AUTOMATA_CODEX_SPEC.md §2.3.3, STANDARD_MR_PROCESSING_FLOW.md §4.1 | 問題なし |
| §8 PrePlanningManager | AUTOMATA_CODEX_SPEC.md §2.3.3, STANDARD_MR_PROCESSING_FLOW.md §4.1 | 問題なし |
| §8（重複）その他の主要クラス | AUTOMATA_CODEX_SPEC.md §6（ProgressReporter）, §8.6（TaskInheritanceContextProvider）| **矛盾あり**: CLASS_IMPLEMENTATION_SPEC.md のセクション番号「§8」が二重に存在する（§8: ExecutionEnvironmentManager以降のPrePlanningManagerと§8: その他の主要クラス）。ドキュメント構造の誤り |
| §9 MCPClient関連 | AUTOMATA_CODEX_SPEC.md §9, CLASS_IMPLEMENTATION_SPEC.md §2.4（MCPClientFactory） | 問題なし |
| §10 GuidelineLearningAgent | AUTOMATA_CODEX_SPEC.md §11 | 問題なし |

### USER_MANAGEMENT_SPEC.md

> **注意**: 前バージョンのチェックでは §1〜§7 の章名が実際のドキュメントと全て異なる誤記があった。以下は実際の章構造に基づき修正済み。

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §2 ユーザー登録フロー | DATABASE_SCHEMA_SPEC.md §2.1（usersテーブル）, §2.2（user_configsテーブル）| 問題なし |
| §3 データベース設計 | DATABASE_SCHEMA_SPEC.md §2 | 問題なし（テーブル詳細はDATABASE_SCHEMA_SPEC.mdに委譲と明記） |
| §3.1 ユーザーロール | DATABASE_SCHEMA_SPEC.md §2.1（roleカラム）| 問題なし |
| §3.2 パスワード管理 | AUTOMATA_CODEX_SPEC.md §12.2（暗号化）| 問題なし |
| §4 APIキー暗号化 | AUTOMATA_CODEX_SPEC.md §12.2, DATABASE_SCHEMA_SPEC.md §2.2（api_key_encrypted）| 問題なし |
| §5 初期管理者作成ツール | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §5.1 CLIコマンド | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §5.2 実行方法 | — | 問題なし |
| §5.3 処理フロー | DATABASE_SCHEMA_SPEC.md §2.1（usersテーブル）| 問題なし |
| §5.4 バリデーション | — | 問題なし |
| §5.5 デフォルト設定 | DATABASE_SCHEMA_SPEC.md §2.2（user_configsテーブル）| 問題なし |
| §5.6 エラーハンドリング | — | 問題なし |
| §5.7 セキュリティ考慮事項 | AUTOMATA_CODEX_SPEC.md §12 | 問題なし |
| §6 User Config API | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §6.1 ユーザー管理エンドポイント | DATABASE_SCHEMA_SPEC.md §2.2（user_configsテーブルの各カラム）| 問題なし |
| §6.2 ワークフロー定義管理エンドポイント | DATABASE_SCHEMA_SPEC.md §3.1（workflow_definitionsテーブル）, GRAPH_DEFINITION_SPEC.md, AGENT_DEFINITION_SPEC.md, PROMPT_DEFINITION_SPEC.md | 問題なし |
| §6.4 ユーザー別ワークフロー設定エンドポイント | DATABASE_SCHEMA_SPEC.md §2.3（user_workflow_settingsテーブル）| **注意**: §6.3が欠番（§6.1→§6.2→§6.4）であるが、ドキュメント内のみの問題であり他ドキュメントとの矛盾ではない |
| §7 Web管理画面 | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §8 ユーザー別トークン統計処理 | DATABASE_SCHEMA_SPEC.md §7.1（token_usageテーブル）, CLASS_IMPLEMENTATION_SPEC.md §5.3（TokenUsageMiddleware）| 問題なし |
| §8.1 実装モジュール | CLASS_IMPLEMENTATION_SPEC.md §5.3（TokenUsageMiddleware）| 問題なし |
| §8.2 Web管理画面での表示 | — | 問題なし |
| §9 Web管理画面の詳細設計 | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §9.1 技術スタック | — | 問題なし |
| §9.2 画面一覧（SC-01〜SC-14） | AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §9.3 画面遷移図 | — | 問題なし |
| §9.4 ワイヤーフレーム（SC-01〜SC-14詳細）| — | 問題なし |
| §9.5 画面共通仕様（§9.5.1〜§9.5.5）| — | 問題なし |

### PROMPTS.md

> **注意**: 前バージョンのチェックでは §11〜§16 の章タイトルが実際のドキュメントと異なる順序で誤記されていた。また §17〜§20（multi_codegen専用プロンプト）が完全に欠落していた。以下は実際の章構造に基づき修正済み。

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 Task Classifier Agent | AGENT_DEFINITION_SPEC.md §6.1, standard_mr_processing_prompts.json | 問題なし |
| §2 コード生成 Planning Agent | AGENT_DEFINITION_SPEC.md §6.2.1, standard_mr_processing_prompts.json | **矛盾あり（軽微）**: プロンプト本文（ステップ1）に「仕様書ファイルを徒底読み」（誤字: 「徹底的に読み」の誤り）が含まれる |
| §3 バグ修正 Planning Agent | AGENT_DEFINITION_SPEC.md §6.2.2, standard_mr_processing_prompts.json | 問題なし |
| §4 テスト生成 Planning Agent | AGENT_DEFINITION_SPEC.md §6.2.3, standard_mr_processing_prompts.json | 問題なし |
| §5 ドキュメント生成 Planning Agent | AGENT_DEFINITION_SPEC.md §6.2.4, standard_mr_processing_prompts.json | 問題なし |
| §6 Plan Reflection Agent | AGENT_DEFINITION_SPEC.md §6.3, standard_mr_processing_prompts.json | 問題なし |
| §7 Code Generation Agent | AGENT_DEFINITION_SPEC.md §6.4.1, standard_mr_processing_prompts.json | 問題なし |
| §8 Bug Fix Agent | AGENT_DEFINITION_SPEC.md §6.4.2, standard_mr_processing_prompts.json | 問題なし |
| §9 Documentation Agent | AGENT_DEFINITION_SPEC.md §6.4.3, standard_mr_processing_prompts.json | 問題なし |
| §10 Test Creation Agent | AGENT_DEFINITION_SPEC.md §6.4.4, standard_mr_processing_prompts.json | 問題なし |
| §11 Test Execution & Evaluation Agent | AGENT_DEFINITION_SPEC.md §6.5, standard_mr_processing_prompts.json | 問題なし |
| §12 Code Review Agent | AGENT_DEFINITION_SPEC.md §6.6.1, standard_mr_processing_prompts.json | 問題なし |
| §13 Documentation Review Agent | AGENT_DEFINITION_SPEC.md §6.6.2, standard_mr_processing_prompts.json | 問題なし |
| §14 Code Generation Reflection Agent（標準フロー専用） | AGENT_DEFINITION_SPEC.md §6.7.1, standard_mr_processing_prompts.json | 問題なし |
| §15 Test Creation Reflection Agent（標準フロー専用） | AGENT_DEFINITION_SPEC.md §6.7.2, standard_mr_processing_prompts.json | 問題なし |
| §16 Documentation Reflection Agent（標準フロー専用） | AGENT_DEFINITION_SPEC.md §6.7.3, standard_mr_processing_prompts.json | 問題なし |
| §17 Code Generation Agent（高速モード）- multi_codegen専用 | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_prompts.json | 問題なし |
| §18 Code Generation Agent（標準モード）- multi_codegen専用 | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_prompts.json | 問題なし |
| §19 Code Generation Agent（創造的モード）- multi_codegen専用 | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_prompts.json | 問題なし |
| §20 Code Review Agent（複数実装比較）- multi_codegen専用 | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_prompts.json | 問題なし |

### PROMPT_DEFINITION_SPEC.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §4.4, DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |
| §2 DBへの保存形式 | DATABASE_SCHEMA_SPEC.md §3.1（workflow_definitions.prompt_definition） | 問題なし |
| §3.1 トップレベル構造 | standard_mr_processing_prompts.json, multi_codegen_mr_processing_prompts.json | 問題なし |
| §3.2 デフォルトLLMパラメータ（default_llm_params）| standard_mr_processing_prompts.json, USER_MANAGEMENT_SPEC.md §3.2（user_configs）| 問題なし |
| §3.3 プロンプト定義（prompts配列）| AGENT_DEFINITION_SPEC.md §3.2（prompt_idフィールド）, PROMPTS.md | 問題なし |
| §4.1 標準MR処理プロンプト定義（インラインJSON例）| standard_mr_processing_prompts.json | 問題なし（インライン例は説明用の抜粋であり実JSONと同一内容を示す） |
| §4.2 複数コード生成並列プロンプト定義（multi_codegen）| multi_codegen_mr_processing_prompts.json, PROMPTS.md §17〜§20 | 問題なし |
| §5 バリデーション仕様 | — | 問題なし |
| §6 プロンプト適用優先順位 | USER_MANAGEMENT_SPEC.md §6.2（ユーザーカスタムプロンプト設定）, DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |

### STANDARD_MR_PROCESSING_FLOW.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §1 | 問題なし |
| §1.1 本ドキュメントの目的 | — | 問題なし |
| §1.2 説明範囲 | — | 問題なし |
| §1.3 関連ドキュメント | — | 問題なし |
| §2 エージェント構成（表） | AGENT_DEFINITION_SPEC.md §4.1, standard_mr_processing_agents.json | **矛盾あり（重大）**: 以下5点の不一致がある |
| | | ①`code_generation`, `bug_fix`, `test_creation`, `documentation`の出力コンテキストキーを「`execution_results`」（複数）と記載しているが、standard_mr_processing_agents.jsonでは「`execution_result`」（単数）となっている |
| | | ②`code_review`の入力コンテキストキーを「`execution_results`, `task_context`」と記載しているが、standard_mr_processing_agents.jsonでは「`execution_result`, `task_context`」（単数）となっている |
| | | ③`test_execution_evaluation`の入力コンテキストキーを「`execution_results`, `task_context`」と記載しているが、standard_mr_processing_agents.jsonでは「`execution_result`, `task_context`」（単数）となっている |
| | | ④`plan_reflection`の入力コンテキストキーを「`plan_result, todo_list, task_context`」と記載しているが、AGENT_DEFINITION_SPEC.md §4.1では4キー、standard_mr_processing_agents.jsonでは6キーとなっている |
| | | ⑤`documentation_review`の入力コンテキストキーを「`execution_results`, `task_context`」と記載しているが、standard_mr_processing_agents.jsonでは「`execution_result`, `task_context`」（単数）となっている |
| §2.1 共通実装ルール | AGENT_DEFINITION_SPEC.md §3（JSON形式の仕様）| 問題なし |
| §3 MR処理の全体フロー（mermaidフロー図）| standard_mr_processing_graph.json | **矛盾あり（重大）**: 以下2点の不一致がある |
| | | ①フロー図では `code_generation_reflectionのproceed分岐 → code_review` と示されているが、standard_mr_processing_graph.jsonでは `code_gen_reflection_branch のproceed → execution_type_branch → test_execution_evaluation or code_review` と経由ノードが存在する |
| | | ②フロー図では `code_review → test_execution_evaluation → plan_reflection` と示されているが、standard_mr_processing_graph.jsonでは `execution_type_branch → test_execution_evaluation → code_review → plan_reflection`（テスト実行評価がコードレビューの前）となっている |
| §3.1 主要ノード構成（表） | standard_mr_processing_graph.json, AGENT_DEFINITION_SPEC.md §4.1 | 問題なし |
| §3.2 重要なフロー特性 | standard_mr_processing_graph.json | 問題なし |
| §4.1 計画前情報収集フェーズ | AGENT_DEFINITION_SPEC.md §6.1, AUTOMATA_CODEX_SPEC.md §4.3.1 | 問題なし |
| §4.2 計画フェーズ | AGENT_DEFINITION_SPEC.md §6.2, standard_mr_processing_agents.json | 問題なし |
| §4.3 実行フェーズ | AGENT_DEFINITION_SPEC.md §6.4 | 問題なし |
| §4.4 実行リフレクションフェーズ | standard_mr_processing_agents.json（code_generation_reflection等）| 問題なし |
| §4.5 レビューフェーズ | AGENT_DEFINITION_SPEC.md §6.6.1, §6.6.2 | 問題なし |
| §4.6 テスト実行・評価フェーズ（コード生成・バグ修正・テスト作成）| AGENT_DEFINITION_SPEC.md §6.5, standard_mr_processing_graph.json（execution_type_branch）| 問題なし |
| §4.7 リフレクションフェーズ | AGENT_DEFINITION_SPEC.md §6.3, standard_mr_processing_graph.json（replan_branch）| 問題なし |
| §4.8 差分計画パターン（ユーザーコメント対応）| CLASS_IMPLEMENTATION_SPEC.md §5.2（CommentCheckMiddleware）| 問題なし |
| §4.8.1 Middleware実装の特徴 | CLASS_IMPLEMENTATION_SPEC.md §5.2 | 問題なし |
| §4.8.2 コンテキストキーの拡張 | AGENT_DEFINITION_SPEC.md §5（コンテキストキー一覧）| 問題なし |
| §4.8.3 処理フロー | CLASS_IMPLEMENTATION_SPEC.md §5.2 | 問題なし |
| §4.8.4 reflection_result出力形式の拡張 | AGENT_DEFINITION_SPEC.md §4.1（plan_reflection output_keys）| 問題なし |
| §4.8.5 グラフ定義での実装 | GRAPH_DEFINITION_SPEC.md §3.2（metadataフィールド）| 問題なし |
| §4.8.6 エージェント定義での実装 | AGENT_DEFINITION_SPEC.md §4.1 | 問題なし |
| §4.8.7 プロンプト定義での実装 | PROMPT_DEFINITION_SPEC.md | 問題なし |
| §4.8.8 利点 | — | 問題なし |
| §5 タスク種別別詳細フロー | standard_mr_processing_graph.json | 問題なし |
| §5.1 コード生成フロー | AGENT_DEFINITION_SPEC.md §6.4.1, standard_mr_processing_graph.json | 問題なし |
| §5.2 バグ修正フロー | AGENT_DEFINITION_SPEC.md §6.4.2, standard_mr_processing_graph.json | 問題なし |
| §5.3 ドキュメント生成フロー | AGENT_DEFINITION_SPEC.md §6.4.3, standard_mr_processing_graph.json | 問題なし |
| §5.4 テスト作成フロー | AGENT_DEFINITION_SPEC.md §6.4.4, standard_mr_processing_graph.json | 問題なし |
| §6 仕様ファイル管理 | AUTOMATA_CODEX_SPEC.md §4.3.2 | 問題なし |
| §6.1 仕様ファイル命名規則 | — | 問題なし |
| §6.2 仕様ファイル作成テンプレート | — | 問題なし |
| §6.3 自動レビュープロセス | AGENT_DEFINITION_SPEC.md §6.6 | 問題なし |
| §7 まとめ | — | 問題なし |
| §7.1 主要な特徴 | — | 問題なし |
| §7.2 重要なポイント | — | 問題なし |
| §7.3 関連ドキュメント | — | 問題なし |

### DATABASE_SCHEMA_SPEC.md

> **注意**: 前バージョンのチェックでは DATABASE_SCHEMA_SPEC.md の章番号が実際のドキュメントと全て異なる誤記があった（§4〜§13が全てずれていた）。また §8〜§13 が完全に欠落していた。以下は実際の章構造に基づき修正済み。

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §8, USER_MANAGEMENT_SPEC.md | 問題なし |
| §1.1 データベース構成 | AUTOMATA_CODEX_SPEC.md §2.3.4（Runtime Layer）| 問題なし |
| §1.2 ER図 | 全テーブル | 問題なし |
| §2.1 usersテーブル | USER_MANAGEMENT_SPEC.md §2, §3 | 問題なし |
| §2.2 user_configsテーブル | USER_MANAGEMENT_SPEC.md §6.1, AUTOMATA_CODEX_SPEC.md §3, §11 | 問題なし |
| §2.3 user_workflow_settingsテーブル | USER_MANAGEMENT_SPEC.md §6.4, AUTOMATA_CODEX_SPEC.md §3 | 問題なし |
| §3.1 workflow_definitionsテーブル（JSONB構造例）| GRAPH_DEFINITION_SPEC.md, AGENT_DEFINITION_SPEC.md, PROMPT_DEFINITION_SPEC.md | **矛盾あり（重大）**: JSONB構造の例示が他ドキュメントの仕様と一致しない |
| | | ①`graph_definition`例で `executor_type` フィールドを使用しているが、GRAPH_DEFINITION_SPEC.md §3.2では `executor_class` フィールドを使用する |
| | | ②`agent_definition`例で `tools` フィールドを使用しているが、AGENT_DEFINITION_SPEC.md §3.2では `mcp_servers` フィールドを使用する |
| | | ③`agent_definition`例で input_keys が `["mr_description", "mr_comments"]` となっているが、実際の仕様は `["task_context"]` 等である |
| | | ④`prompt_definition`例で `prompt_id` フィールドが使われているが、PROMPT_DEFINITION_SPEC.md §3.3では `id` フィールドを使用する |
| §4.1 tasksテーブル | AUTOMATA_CODEX_SPEC.md §8, CLASS_IMPLEMENTATION_SPEC.md §2.1（save_workflow_state）| 問題なし |
| §4.5 ワークフロー実行管理テーブル群 | CLASS_IMPLEMENTATION_SPEC.md §2.1（WorkflowFactory停止・再開関連）| 問題なし |
| §4.5.1 workflow_execution_statesテーブル | CLASS_IMPLEMENTATION_SPEC.md §2.1（save_workflow_state, load_workflow_state）| 問題なし |
| §4.5.2 docker_environment_mappingsテーブル | CLASS_IMPLEMENTATION_SPEC.md §6（ExecutionEnvironmentManager）| 問題なし |
| §5.1 context_messagesテーブル | CLASS_IMPLEMENTATION_SPEC.md §4.1（PostgreSqlChatHistoryProvider）| 問題なし |
| §5.2 message_compressionsテーブル | CLASS_IMPLEMENTATION_SPEC.md §4.4（ContextCompressionService）| 問題なし |
| §5.3 context_planning_historyテーブル | CLASS_IMPLEMENTATION_SPEC.md §4.2（PlanningContextProvider）| 問題なし |
| §5.4 context_metadataテーブル | CLASS_IMPLEMENTATION_SPEC.md §4.1（PostgreSqlChatHistoryProvider）| 問題なし |
| §5.5 context_tool_results_metadataテーブル | CLASS_IMPLEMENTATION_SPEC.md §4.3（ToolResultContextProvider）| 問題なし |
| §6.1 todosテーブル | AGENT_DEFINITION_SPEC.md §3.2（todo_list仮想MCPサーバー）| 問題なし |
| §7.1 token_usageテーブル | AUTOMATA_CODEX_SPEC.md §3, CLASS_IMPLEMENTATION_SPEC.md §5.3（TokenUsageMiddleware）| 問題なし |
| §8 データ保持期限とクリーンアップ | — | 問題なし |
| §8.1 自動クリーンアップ対象テーブル | §5〜§7の各テーブル | 問題なし |
| §8.2 クリーンアップ実行方法 | AUTOMATA_CODEX_SPEC.md §13.3（監視・ログ）| 問題なし |
| §9 データベース初期化SQL | §2〜§7の各テーブル定義 | 問題なし |
| §10 データベース設定 | AUTOMATA_CODEX_SPEC.md §13.1（デプロイ構成）| 問題なし |
| §10.1 接続設定 | AUTOMATA_CODEX_SPEC.md §14.1（config.yaml）| 問題なし |
| §10.2 パフォーマンスチューニング | — | 問題なし |
| §10.3 バックアップ設定 | AUTOMATA_CODEX_SPEC.md §13.3 | 問題なし |
| §11 セキュリティ設定 | AUTOMATA_CODEX_SPEC.md §12, USER_MANAGEMENT_SPEC.md §4 | 問題なし |
| §11.1 暗号化 | USER_MANAGEMENT_SPEC.md §4（APIキー暗号化）| 問題なし |
| §11.2 アクセス制御 | AUTOMATA_CODEX_SPEC.md §12.1 | 問題なし |
| §12 マイグレーション管理 | — | 問題なし |
| §12.1 スキーマバージョン管理 | — | 問題なし |
| §12.2 マイグレーションファイル命名規則 | — | 問題なし |
| §13 まとめ | — | 問題なし |

### AGENT_DEFINITION_SPEC.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §4.4, DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |
| §2 DBへの保存形式 | DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |
| §3 JSON形式の仕様（mcp_serversフィールド等） | CLASS_IMPLEMENTATION_SPEC.md §2.3（AgentFactory）, §2.4（MCPClientFactory）| 問題なし |
| §3.1 トップレベル構造 | — | 問題なし |
| §3.2 エージェントノード定義（agents）| CLASS_IMPLEMENTATION_SPEC.md §2.3（AgentFactory.create_agent）| 問題なし |
| §4.1 標準MR処理エージェント定義（インライン定義）| standard_mr_processing_agents.json | **矛盾あり（重大）**: 以下7点の不一致がある |
| | | ①`task_classifier`の`output_keys`: ドキュメントは`["classification_result", "selected_environment"]`、JSONは`["classification_result"]`のみ |
| | | ②`code_generation_planning`等の計画エージェントの`input_keys`: ドキュメントは2キー、JSONは6キー（再計画用キー`previous_plan_result`, `replan_reason`, `user_new_comments`, `delta_requirements`を追加） |
| | | ③`code_generation_planning`等の計画エージェントの`output_keys`: ドキュメントは2キー、JSONは3キー（`plan_metadata`を追加） |
| | | ④`plan_reflection`の`input_keys`: ドキュメントは4キー、JSONは6キー（`user_new_comments`, `execution_result`を追加） |
| | | ⑤`plan_reflection`の`output_keys`: ドキュメントは1キー（`reflection_result`）、JSONは8キー（`replan_mode`, `replan_reason`, `delta_requirements`, `affected_todos`, `new_requirements`, `conflicts`, `comment_response`を追加） |
| | | ⑥実行エージェント（`code_generation`, `bug_fix`, `test_creation`, `documentation`）の`output_keys`: ドキュメントは`"execution_results"`（複数）、JSONは`"execution_result"`（単数） |
| | | ⑦`code_review`, `documentation_review`, `test_execution_evaluation`の`input_keys`: ドキュメントは`"execution_results"`（複数）、JSONは`"execution_result"`（単数） |
| §4.2 複数コード生成並列エージェント定義（インライン定義）| multi_codegen_mr_processing_agents.json | **矛盾あり（重大）**: 以下3点の不一致がある |
| | | ①ドキュメントのplan_reflectionの`input_keys`: `["review_result", "task_context"]`（2キー）、JSONは6キー |
| | | ②ドキュメントのplan_reflectionの`output_keys`: `["reflection_result"]`（1キー）、JSONは8キー |
| | | ③ドキュメントのplan_reflectionの`mcp_servers`: `["text_editor"]`（1サーバー）、JSONは`["text_editor", "todo_list"]`（2サーバー） |
| §5 コンテキストキー一覧 | CLASS_IMPLEMENTATION_SPEC.md全体, AUTOMATA_CODEX_SPEC.md §8.2 | 問題なし |
| §6.1 Task Classifier Agent | STANDARD_MR_PROCESSING_FLOW.md §4.1, PROMPTS.md §1 | 問題なし |
| §6.2 Planning Agent群 | STANDARD_MR_PROCESSING_FLOW.md §4.2, PROMPTS.md §2〜§5 | 問題なし |
| §6.2.1 コード生成 Planning Agent ノード | PROMPTS.md §2 | 問題なし |
| §6.2.2 バグ修正 Planning Agent ノード | PROMPTS.md §3 | 問題なし |
| §6.2.3 テスト生成 Planning Agent ノード | PROMPTS.md §4 | 問題なし |
| §6.2.4 ドキュメント生成 Planning Agent ノード | PROMPTS.md §5 | 問題なし |
| §6.3 Plan Reflection Agent | AUTOMATA_CODEX_SPEC.md §4.4.2（reflectionロールはenv_ref省略のみ許容）| **矛盾あり**: §6.3 のplan_reflectionエージェント定義主要設定に `env_ref: "plan"` と記載されているが、AUTOMATA_CODEX_SPEC.md §4.4.2では「reflectionロールはenv_ref省略のみ許容（Docker環境を必要としない）」と明記されており矛盾する。また、standard_mr_processing_graph.jsonの実装でもplan_reflectionにenv_refは設定されていない |
| §6.4 Execution Agent群 | STANDARD_MR_PROCESSING_FLOW.md §4.3, PROMPTS.md §7〜§10 | 問題なし |
| §6.4.1 Code Generation Agent ノード | PROMPTS.md §7 | 問題なし |
| §6.4.2 Bug Fix Agent ノード | PROMPTS.md §8 | 問題なし |
| §6.4.3 Documentation Agent ノード | PROMPTS.md §9 | 問題なし |
| §6.4.4 Test Creation Agent ノード | PROMPTS.md §10 | 問題なし |
| §6.5 Test Execution & Evaluation Agent ノード | STANDARD_MR_PROCESSING_FLOW.md §4.6, PROMPTS.md §11 | 問題なし |
| §6.6 Review Agent群 | STANDARD_MR_PROCESSING_FLOW.md §4.5 | 問題なし |
| §6.6.1 Code Review Agent ノード | PROMPTS.md §12 | 問題なし |
| §6.6.2 Documentation Review Agent ノード | PROMPTS.md §13 | 問題なし |
| §6.7 Execution Reflection Agent群 | STANDARD_MR_PROCESSING_FLOW.md §4.4 | 問題なし |
| §6.7.1 Code Generation Reflection Agent ノード | PROMPTS.md §14 | 問題なし |
| §6.7.2 Test Creation Reflection Agent ノード | PROMPTS.md §15 | 問題なし |
| §6.7.3 Documentation Reflection Agent ノード | PROMPTS.md §16 | 問題なし |

### GRAPH_DEFINITION_SPEC.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §4.4, DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |
| §2 DBへの保存形式 | DATABASE_SCHEMA_SPEC.md §3.1 | 問題なし |
| §3 JSON形式の仕様（ノード・エッジ定義）| CLASS_IMPLEMENTATION_SPEC.md §3.5（ExecEnvSetupExecutor）, AUTOMATA_CODEX_SPEC.md §4.3.2 | 問題なし |
| §3.1 トップレベル構造 | — | 問題なし |
| §3.2 ノード定義（nodes）（metadataフィールド含む）| CLASS_IMPLEMENTATION_SPEC.md §5.2（CommentCheckMiddleware）| 問題なし |
| §3.3 エッジ定義（edges）| — | 問題なし |
| §4.1 標準MR処理グラフ（インラインJSON）| standard_mr_processing_graph.json | **矛盾あり（重大）**: インラインJSONに以下のノードが欠落している |
| | | ①`code_generation_reflection`, `code_gen_reflection_branch`ノードが存在しない |
| | | ②`test_creation_reflection`, `test_reflection_branch`ノードが存在しない |
| | | ③`documentation_reflection`, `doc_reflection_branch`ノードが存在しない |
| | | ④エッジが `code_generation → execution_type_branch` と記載されているが、実JSONでは `code_generation → code_generation_reflection → code_gen_reflection_branch → execution_type_branch`（リフレクション経由） |
| §4.2 複数コード生成並列グラフ（インラインJSON）| multi_codegen_mr_processing_graph.json | **矛盾あり（重大）**: インラインJSONはコード生成の並列分岐に関する一部ノードのみ示されており、bug_fix, test_creation, documentation, replan_branch等の多数のノードとエッジが省略されている。ドキュメントが実JSONを不完全にしか表現していない |
| §4.2.1 multi_codegen_mr_processingの詳細説明 | multi_codegen_mr_processing_graph.json, MULTI_MR_PROCESSING_FLOW.md | 問題なし |
| §5 バリデーション仕様 | CLASS_IMPLEMENTATION_SPEC.md §2.1（WorkflowFactory）| 問題なし |
| §6 定義の取得・更新フロー | USER_MANAGEMENT_SPEC.md §6.2（ワークフロー定義管理エンドポイント）| 問題なし |

### MULTI_MR_PROCESSING_FLOW.md

| 章 | 関連ドキュメント/章 | 問題 |
|----|-------------------|------|
| §1 概要 | AUTOMATA_CODEX_SPEC.md §4.5, STANDARD_MR_PROCESSING_FLOW.md §1 | 問題なし |
| §1.1 本ドキュメントの目的 | — | 問題なし |
| §1.2 標準フローとの主な違い | STANDARD_MR_PROCESSING_FLOW.md | 問題なし |
| §1.3 説明範囲 | — | 問題なし |
| §1.4 関連ドキュメント | — | 問題なし |
| §2 エージェント構成（表） | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_agents.json | **矛盾あり**: `code_review`の入力コンテキストキーを「`execution_result, execution_results, branch_envs, task_context`」と記載しているが、multi_codegen_mr_processing_agents.jsonでは `input_keys: ["branch_envs", "execution_results", "task_context"]`（`execution_result`単数形が含まれない） |
| §2.1 並列コード生成エージェントの設定比較 | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_agents.json | 問題なし |
| §2.2 共通実装ルール | AGENT_DEFINITION_SPEC.md §3（JSON形式の仕様）| 問題なし |
| §3 MR処理の全体フロー（mermaidフロー図）| multi_codegen_mr_processing_graph.json | 問題なし（概ね一致） |
| §3.1 主要ノード構成（表）| multi_codegen_mr_processing_graph.json | 問題なし |
| §3.2 重要なフロー特性 | multi_codegen_mr_processing_graph.json | 問題なし |
| §4.1 計画前情報収集フェーズ | STANDARD_MR_PROCESSING_FLOW.md §4.1 | 問題なし（「標準フローと同一」と参照） |
| §4.2 計画フェーズ | STANDARD_MR_PROCESSING_FLOW.md §4.2 | 問題なし |
| §4.3 並列実行環境セットアップフェーズ | CLASS_IMPLEMENTATION_SPEC.md §3.5（ExecEnvSetupExecutor）, GRAPH_DEFINITION_SPEC.md §3.2（env_count）| 問題なし |
| §4.4 並列コード生成フェーズ | multi_codegen_mr_processing_agents.json | 問題なし |
| §4.5 比較レビュー・自動選択フェーズ | multi_codegen_mr_processing_agents.json（code_reviewエージェント）| 問題なし |
| §4.6 ブランチマージフェーズ（BranchMergeExecutor）| AUTOMATA_CODEX_SPEC.md §4.4.2（ExecutorFactory.create_branch_merge）| 問題なし |
| §4.7 リフレクション・再計画フェーズ | multi_codegen_mr_processing_agents.json（plan_reflection）| 問題なし |
| §4.8 バグ修正・テスト作成・ドキュメント生成タスク | STANDARD_MR_PROCESSING_FLOW.md §5.2〜§5.4, multi_codegen_mr_processing_graph.json | 問題なし |
| §5 コード生成タスクの詳細フロー | multi_codegen_mr_processing_graph.json | 問題なし |
| §6 ブランチ管理 | AUTOMATA_CODEX_SPEC.md §4.5 | 問題なし |
| §6.1 ブランチ命名規則 | AUTOMATA_CODEX_SPEC.md §4.5.1 | 問題なし |
| §6.2 ブランチのライフサイクル | AUTOMATA_CODEX_SPEC.md §4.5.2, §4.5.3 | 問題なし |
| §6.3 ブランチ保持ポリシー | AUTOMATA_CODEX_SPEC.md §4.5.4 | 問題なし |
| §7 まとめ | — | 問題なし |

---

## チェック観点2：JSONファイルとドキュメントの矛盾チェック

各JSONファイルごとに記述のあるドキュメント/章をリストし、矛盾の有無を報告する。

### standard_mr_processing_agents.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| `task_classifier.output_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["classification_result"]`のみ。AGENT_DEFINITION_SPEC.md §4.1は`["classification_result", "selected_environment"]` |
| `code_generation_planning.input_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは6キー（再計画用キー含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `code_generation_planning.output_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは3キー（`plan_metadata`含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `bug_fix_planning.input_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは6キー（再計画用キー含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `bug_fix_planning.output_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは3キー（`plan_metadata`含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `test_creation_planning.input_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは6キー（再計画用キー含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `test_creation_planning.output_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは3キー（`plan_metadata`含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `documentation_planning.input_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは6キー（再計画用キー含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `documentation_planning.output_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは3キー（`plan_metadata`含む）、AGENT_DEFINITION_SPEC.md §4.1は2キーのみ |
| `plan_reflection.input_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは6キー（`user_new_comments`, `execution_result`含む）、AGENT_DEFINITION_SPEC.md §4.1は4キー、STANDARD_MR_PROCESSING_FLOW.md §2は3キーの表記 |
| `plan_reflection.output_keys` | AGENT_DEFINITION_SPEC.md §4.1 | **矛盾あり**: JSONは8キー（`replan_mode`, `replan_reason`, `delta_requirements`, `affected_todos`, `new_requirements`, `conflicts`, `comment_response`含む）、AGENT_DEFINITION_SPEC.md §4.1は1キー（`reflection_result`）のみ |
| `code_generation.output_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result"]`（単数）、両ドキュメントは`["execution_results"]`（複数） |
| `bug_fix.output_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result"]`（単数）、両ドキュメントは`["execution_results"]`（複数） |
| `test_creation.output_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result"]`（単数）、両ドキュメントは`["execution_results"]`（複数） |
| `documentation.output_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result"]`（単数）、両ドキュメントは`["execution_results"]`（複数） |
| `code_review.input_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result", "task_context"]`（単数）、両ドキュメントは`["execution_results", "task_context"]`（複数） |
| `documentation_review.input_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result", "task_context"]`（単数）、両ドキュメントは`["execution_results", "task_context"]`（複数） |
| `test_execution_evaluation.input_keys` | AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`["execution_result", "task_context"]`（単数）、両ドキュメントは`["execution_results", "task_context"]`（複数） |
| `code_generation_reflection.description` | STANDARD_MR_PROCESSING_FLOW.md §2, AGENT_DEFINITION_SPEC.md §4.1 | 問題なし（「コード生成・バグ修正の成果物を検証」と記述） |
| `test_creation_reflection`, `documentation_reflection` | AGENT_DEFINITION_SPEC.md §4.1 | 問題なし |

### standard_mr_processing_graph.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| ノード構成（全体）| GRAPH_DEFINITION_SPEC.md §4.1 | **矛盾あり（重大）**: 実JSONには`code_generation_reflection`, `code_gen_reflection_branch`, `test_creation_reflection`, `test_reflection_branch`, `documentation_reflection`, `doc_reflection_branch`が存在するが、GRAPH_DEFINITION_SPEC.md §4.1のインラインJSONにはこれらのノードが欠落している |
| エッジ構成（code_generation以降）| GRAPH_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §3 | **矛盾あり（重大）**: 実JSONは`code_generation → code_generation_reflection → code_gen_reflection_branch → execution_type_branch`の経路をとるが、GRAPH_DEFINITION_SPEC.md §4.1インラインJSONは`code_generation → execution_type_branch`と直接接続されている |
| エッジ順序（test_execution_evaluation と code_review）| STANDARD_MR_PROCESSING_FLOW.md §3（mermaid図）| **矛盾あり**: 実JSONでは`test_execution_evaluation → code_review → plan_reflection`の順だが、STANDARD_MR_PROCESSING_FLOW.md §3の図は`code_review → test_execution_evaluation → plan_reflection`（コードレビューが先）と逆順で示されている |
| replan_branchのエッジ（proceed→null）| GRAPH_DEFINITION_SPEC.md §3.3（toにnullを指定）| 問題なし |
| check_comments_before メタデータ | GRAPH_DEFINITION_SPEC.md §3.2（metadataフィールド）| 問題なし |
| env_ref設定 | GRAPH_DEFINITION_SPEC.md §3.2, CLASS_IMPLEMENTATION_SPEC.md §1.3 | 問題なし |

### standard_mr_processing_prompts.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| バージョン・トップレベル構造 | PROMPT_DEFINITION_SPEC.md §3.1 | 問題なし |
| `default_llm_params` | PROMPT_DEFINITION_SPEC.md §3.2 | 問題なし |
| `task_classifier`プロンプト内容 | PROMPTS.md §1 | 問題なし（内容は一致） |
| `code_generation_planning`プロンプト内容 | PROMPTS.md §2 | 問題なし（内容は一致） |
| `bug_fix_planning`プロンプト内容 | PROMPTS.md §3 | 問題なし（内容は一致） |
| `test_creation_planning`プロンプト内容 | PROMPTS.md §4 | 問題なし（内容は一致） |
| `documentation_planning`プロンプト内容 | PROMPTS.md §5 | 問題なし（内容は一致） |
| `plan_reflection`プロンプト内容 | PROMPTS.md §6 | 問題なし（内容は一致） |
| `code_generation`プロンプト内容 | PROMPTS.md §7 | 問題なし（内容は一致） |
| `bug_fix`プロンプト内容 | PROMPTS.md §8 | 問題なし（内容は一致） |
| `documentation`プロンプト内容 | PROMPTS.md §9 | 問題なし（内容は一致） |
| `test_creation`プロンプト内容 | PROMPTS.md §10 | 問題なし（内容は一致） |
| `code_generation_reflection`, `test_creation_reflection`, `documentation_reflection`プロンプト | PROMPTS.md §11, §12, §13 | 問題なし |
| `code_review`, `documentation_review`, `test_execution_evaluation`プロンプト | PROMPTS.md §14, §15, §16 | 問題なし |

### multi_codegen_mr_processing_agents.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| `code_generation_fast`, `code_generation_standard`, `code_generation_creative`エージェント定義 | AGENT_DEFINITION_SPEC.md §4.2, MULTI_MR_PROCESSING_FLOW.md §2 | 問題なし |
| `code_review.input_keys` | AGENT_DEFINITION_SPEC.md §4.2, MULTI_MR_PROCESSING_FLOW.md §2 | **矛盾あり（軽微）**: MULTI_MR_PROCESSING_FLOW.md §2の表では`execution_result`（単数）と`execution_results`（複数）の両方が入力として記載されているが、JSONは`["branch_envs", "execution_results", "task_context"]`（`execution_result`単数形なし） |
| `plan_reflection.input_keys` | AGENT_DEFINITION_SPEC.md §4.2 | **矛盾あり（重大）**: JSONは6キー（`plan_result`, `todo_list`, `task_context`, `review_result`, `user_new_comments`, `execution_result`）、AGENT_DEFINITION_SPEC.md §4.2は2キー（`review_result`, `task_context`） |
| `plan_reflection.output_keys` | AGENT_DEFINITION_SPEC.md §4.2 | **矛盾あり（重大）**: JSONは8キー、AGENT_DEFINITION_SPEC.md §4.2は1キー（`reflection_result`） |
| `plan_reflection.mcp_servers` | AGENT_DEFINITION_SPEC.md §4.2 | **矛盾あり**: JSONは`["text_editor", "todo_list"]`（2サーバー）、AGENT_DEFINITION_SPEC.md §4.2は`["text_editor"]`（1サーバー） |
| `code_generation_reflection.description` | standard_mr_processing_agents.json | **矛盾あり（軽微）**: multiの`code_generation_reflection`の`description`が「バグ修正の成果物を検証」のみ、standardは「コード生成・バグ修正の成果物を検証」であり説明が不一致 |
| `bug_fix`, `test_creation`, `documentation`エージェント（単数のoutput_keys）| AGENT_DEFINITION_SPEC.md §4.1, MULTI_MR_PROCESSING_FLOW.md §2 | **矛盾あり**: JSONは`output_keys: ["execution_result"]`（単数）、AGENT_DEFINITION_SPEC.md §4.1は`["execution_results"]`（複数） |

### multi_codegen_mr_processing_graph.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| ノード構成（全体）| GRAPH_DEFINITION_SPEC.md §4.2 | **矛盾あり（重大）**: GRAPH_DEFINITION_SPEC.md §4.2のインラインJSONにはコード生成並列分岐の一部ノード（9ノード）のみ記載されているが、実JSONにはbug_fix, test_creation, documentation, replan_branch等を含む大幅に多くのノードが定義されている |
| エッジ構成（コード生成並列分岐）| GRAPH_DEFINITION_SPEC.md §4.2, MULTI_MR_PROCESSING_FLOW.md §3 | 問題なし（実JSONと仕様の記述は概ね一致） |
| BranchMergeExecutorノード | MULTI_MR_PROCESSING_FLOW.md §4.6, AUTOMATA_CODEX_SPEC.md §4.4.2 | 問題なし（実JSONにBranchMergeExecutorが存在する） |

### multi_codegen_mr_processing_prompts.json

| 項目 | 参照ドキュメント/章 | 問題 |
|------|-------------------|------|
| `code_generation_fast`プロンプト（temperature設定）| MULTI_MR_PROCESSING_FLOW.md §2.1（temperature: 0.1）| 問題なし |
| `code_generation_standard`プロンプト（temperature設定）| MULTI_MR_PROCESSING_FLOW.md §2.1（temperature: 0.2）| 問題なし |
| `code_generation_creative`プロンプト（temperature設定）| MULTI_MR_PROCESSING_FLOW.md §2.1（temperature: 0.7）| 問題なし |
| `code_review_multi`プロンプト | MULTI_MR_PROCESSING_FLOW.md §4.5, AGENT_DEFINITION_SPEC.md §4.2 | 問題なし |
| トップレベル構造 | PROMPT_DEFINITION_SPEC.md §3.1 | 問題なし |

---

## チェック観点3：クラス/メソッドの実装情報完全性チェック

全クラス/メソッドをリストし、実装に必要な情報が揃っているかを確認する。

凡例: ✅ = 情報十分 / ⚠️ = 情報不十分 / ❌ = 設計情報なし

### ConfigurableAgent（CLASS_IMPLEMENTATION_SPEC.md §1）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `ConfigurableAgent` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §1, AUTOMATA_CODEX_SPEC.md §4.3.1, AGENT_DEFINITION_SPEC.md §3 | ✅ 問題なし |
| `handle(msg, ctx)` | CLASS_IMPLEMENTATION_SPEC.md §1.4, AUTOMATA_CODEX_SPEC.md §4.3.1 | ✅ 問題なし |
| `get_chat_history()` | CLASS_IMPLEMENTATION_SPEC.md §1.4 | ✅ 問題なし |
| `get_context(keys)` | CLASS_IMPLEMENTATION_SPEC.md §1.4 | ✅ 問題なし |
| `store_result(output_keys, result)` | CLASS_IMPLEMENTATION_SPEC.md §1.4 | ✅ 問題なし |
| `invoke_mcp_tool(tool_name, params)` | CLASS_IMPLEMENTATION_SPEC.md §1.4 | ✅ 問題なし |
| `get_environment_id()` | AUTOMATA_CODEX_SPEC.md §4.3.1 | ⚠️ **情報不十分**: AUTOMATA_CODEX_SPEC.md §4.3.1 に概要記載はあるが、CLASS_IMPLEMENTATION_SPEC.md §1.4 のメソッド一覧に `get_environment_id()` が記載されていない |
| `report_progress(phase, message, details)` | AUTOMATA_CODEX_SPEC.md §4.3.1 | ⚠️ **情報不十分**: AUTOMATA_CODEX_SPEC.md §4.3.1 に概要記載はあるが、CLASS_IMPLEMENTATION_SPEC.md §1.4 に `report_progress()` が記載されていない |

### WorkflowFactory（CLASS_IMPLEMENTATION_SPEC.md §2.1）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `WorkflowFactory` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §2.1, AUTOMATA_CODEX_SPEC.md §4.4.2 | ✅ 問題なし |
| `create_workflow_from_definition(user_id, task_context)` | CLASS_IMPLEMENTATION_SPEC.md §2.1, AUTOMATA_CODEX_SPEC.md §4.4.2 | ✅ 問題なし |
| `_build_nodes(graph_def, agent_def, prompt_def)` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ⚠️ **情報不十分（軽微）**: AUTOMATA_CODEX_SPEC.md §4.4.2では引数に`user_id`が追加（`_build_nodes(graph_def, agent_def, prompt_def, user_id)`）されているが、CLASS_IMPLEMENTATION_SPEC.md §2.1には`user_id`なし。パラメータ定義が不一致 |
| `_setup_plan_environment()` | CLASS_IMPLEMENTATION_SPEC.md §2.1, AUTOMATA_CODEX_SPEC.md §4.4.2 | ✅ 問題なし |
| `save_workflow_state(execution_id, current_node_id, completed_nodes)` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `load_workflow_state(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `resume_workflow(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `_setup_signal_handlers()` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `_handle_sigterm(signum, frame)` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `_check_shutdown_between_nodes()` | CLASS_IMPLEMENTATION_SPEC.md §2.1 | ✅ 問題なし |
| `_inject_learning_node(graph_def)` | AUTOMATA_CODEX_SPEC.md §4.4.2, §11 | ❌ **設計情報なし**: AUTOMATA_CODEX_SPEC.md §4.4.2 に機能概要の記載はあるが、CLASS_IMPLEMENTATION_SPEC.md §2.1 の WorkflowFactory メソッド一覧に `_inject_learning_node()` の詳細処理フローが記載されていない |

### ExecutorFactory（CLASS_IMPLEMENTATION_SPEC.md §2.2）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `ExecutorFactory` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §2.2, AUTOMATA_CODEX_SPEC.md §4.4.2 | ✅ 問題なし |
| `create_user_resolver()` | CLASS_IMPLEMENTATION_SPEC.md §2.2 | ✅ 問題なし |
| `create_content_transfer()` | CLASS_IMPLEMENTATION_SPEC.md §2.2 | ✅ 問題なし |
| `create_plan_env_setup()` | CLASS_IMPLEMENTATION_SPEC.md §2.2, AUTOMATA_CODEX_SPEC.md §4.4.2 | ✅ 問題なし |
| `create_branch_merge(context)` | AUTOMATA_CODEX_SPEC.md §4.4.2 | ❌ **設計情報なし**: AUTOMATA_CODEX_SPEC.md §4.4.2 に記述はあるが、CLASS_IMPLEMENTATION_SPEC.md §2.2 の ExecutorFactory 主要メソッド一覧に `create_branch_merge()` が存在しない |

### AgentFactory（CLASS_IMPLEMENTATION_SPEC.md §2.3）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `AgentFactory` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §2.3, AUTOMATA_CODEX_SPEC.md §4.4.3 | ✅ 問題なし |
| `create_agent(agent_config, prompt_config, user_email, progress_reporter, env_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.3 | ✅ 問題なし |

### MCPClientFactory（CLASS_IMPLEMENTATION_SPEC.md §2.4）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `MCPClientFactory` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §2.4, AUTOMATA_CODEX_SPEC.md §4.4.4 | ✅ 問題なし |
| `create_mcp_tool(server_name, env_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.4 | ✅ 問題なし |
| `create_text_editor_tool(env_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.4 | ✅ 問題なし |
| `create_command_executor_tool(env_id)` | CLASS_IMPLEMENTATION_SPEC.md §2.4 | ✅ 問題なし |

### TaskStrategyFactory（CLASS_IMPLEMENTATION_SPEC.md §2.5）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `TaskStrategyFactory` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §2.5, AUTOMATA_CODEX_SPEC.md §4.4.5 | ✅ 問題なし |
| `create_strategy(task)` | CLASS_IMPLEMENTATION_SPEC.md §2.5 | ✅ 問題なし |
| `should_convert_issue_to_mr(task)` | CLASS_IMPLEMENTATION_SPEC.md §2.5 | ✅ 問題なし |

### Executor群（CLASS_IMPLEMENTATION_SPEC.md §3）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `BaseExecutor` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §3.1, AUTOMATA_CODEX_SPEC.md §4.3.1 | ✅ 問題なし |
| `BaseExecutor.handle(msg, ctx)` （抽象）| CLASS_IMPLEMENTATION_SPEC.md §3.1 | ✅ 問題なし |
| `BaseExecutor.get_context_value(key, scope_name)` | CLASS_IMPLEMENTATION_SPEC.md §3.1 | ✅ 問題なし |
| `BaseExecutor.set_context_value(key, value, scope_name)` | CLASS_IMPLEMENTATION_SPEC.md §3.1 | ✅ 問題なし |
| `UserResolverExecutor` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §3.2, AUTOMATA_CODEX_SPEC.md §4.3.2 | ✅ 問題なし |
| `UserResolverExecutor.handle(msg, ctx)` | CLASS_IMPLEMENTATION_SPEC.md §3.2 | ✅ 問題なし |
| `ContentTransferExecutor` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §3.3, AUTOMATA_CODEX_SPEC.md §5.0 | ✅ 問題なし |
| `ContentTransferExecutor.handle(msg, ctx)` | CLASS_IMPLEMENTATION_SPEC.md §3.3 | ✅ 問題なし |
| `PlanEnvSetupExecutor` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §3.4, AUTOMATA_CODEX_SPEC.md §4.3.2 | ✅ 問題なし |
| `PlanEnvSetupExecutor.handle(msg, ctx)` | CLASS_IMPLEMENTATION_SPEC.md §3.4 | ✅ 問題なし |
| `ExecEnvSetupExecutor` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §3.5, AUTOMATA_CODEX_SPEC.md §4.3.2 | ✅ 問題なし |
| `ExecEnvSetupExecutor.handle(msg, ctx)` | CLASS_IMPLEMENTATION_SPEC.md §3.5 | ✅ 問題なし |
| `BranchMergeExecutor` クラス全体 | MULTI_MR_PROCESSING_FLOW.md §4.6, AUTOMATA_CODEX_SPEC.md §4.4.2 | ❌ **設計情報なし**: MULTI_MR_PROCESSING_FLOW.md §4.6 に機能概要の記述はあるが、CLASS_IMPLEMENTATION_SPEC.md に `BranchMergeExecutor` の独立した設計章が存在しない。`handle()` の処理フローが未定義 |

### Custom Provider群（CLASS_IMPLEMENTATION_SPEC.md §4）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `PostgreSqlChatHistoryProvider` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §4.1, AUTOMATA_CODEX_SPEC.md §8.3 | ✅ 問題なし |
| `PostgreSqlChatHistoryProvider.get_messages(session_id)` | CLASS_IMPLEMENTATION_SPEC.md §4.1 | ✅ 問題なし |
| `PostgreSqlChatHistoryProvider.save_messages(session_id, messages)` | CLASS_IMPLEMENTATION_SPEC.md §4.1 | ✅ 問題なし |
| `PlanningContextProvider` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §4.2, AUTOMATA_CODEX_SPEC.md §8.3 | ✅ 問題なし |
| `PlanningContextProvider.before_run(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.2 | ✅ 問題なし |
| `PlanningContextProvider.after_run(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.2 | ✅ 問題なし |
| `ToolResultContextProvider` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §4.3, AUTOMATA_CODEX_SPEC.md §8.3 | ✅ 問題なし |
| `ToolResultContextProvider.before_run(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.3 | ✅ 問題なし |
| `ToolResultContextProvider.after_run(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.3 | ✅ 問題なし |
| `ContextCompressionService` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §4.4, AUTOMATA_CODEX_SPEC.md §8.5 | ✅ 問題なし |
| `ContextCompressionService.check_and_compress_async(task_uuid, user_email)` | CLASS_IMPLEMENTATION_SPEC.md §4.4 | ✅ 問題なし |
| `ContextCompressionService.compress_messages_async(task_uuid, start_seq, end_seq)` | CLASS_IMPLEMENTATION_SPEC.md §4.4 | ✅ 問題なし |
| `ContextCompressionService.replace_with_summary_async(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.4 | ✅ 問題なし |

### Middleware実装（CLASS_IMPLEMENTATION_SPEC.md §5）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `CommentCheckMiddleware` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §5.2, AUTOMATA_CODEX_SPEC.md §8.9, GRAPH_DEFINITION_SPEC.md §3.2 | ✅ 問題なし |
| `CommentCheckMiddleware.intercept(...)` | CLASS_IMPLEMENTATION_SPEC.md §5.2 | ✅ 問題なし |
| `TokenUsageMiddleware` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §5.3, AUTOMATA_CODEX_SPEC.md §8.9, DATABASE_SCHEMA_SPEC.md §13 | ✅ 問題なし |
| `TokenUsageMiddleware.intercept(...)` | CLASS_IMPLEMENTATION_SPEC.md §5.3 | ✅ 問題なし |
| `ErrorHandlingMiddleware` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §5.4, AUTOMATA_CODEX_SPEC.md §8.9, §10 | ✅ 問題なし |
| `ErrorHandlingMiddleware.intercept(...)` | CLASS_IMPLEMENTATION_SPEC.md §5.4 | ✅ 問題なし |
| `LoopGuardMiddleware` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §5（詳細は本文中）, GRAPH_DEFINITION_SPEC.md §3.2（max_retriesフィールド）| ✅ 問題なし |

### ExecutionEnvironmentManager（CLASS_IMPLEMENTATION_SPEC.md §6）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `ExecutionEnvironmentManager` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §6, AUTOMATA_CODEX_SPEC.md §8.8 | ✅ 問題なし |
| `prepare_environments(count, environment_name, mr_iid, node_ids)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `get_environment(node_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `execute_command(node_id, command)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `clone_repository(node_id, repo_url, branch)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `cleanup_environments()` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `save_environment_mapping(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `load_environment_mapping(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `stop_all_containers(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `start_all_containers(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |
| `check_containers_exist(execution_id)` | CLASS_IMPLEMENTATION_SPEC.md §6.3 | ✅ 問題なし |

### EnvironmentAnalyzer（CLASS_IMPLEMENTATION_SPEC.md §7）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `EnvironmentAnalyzer` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §7, AUTOMATA_CODEX_SPEC.md §2.3.3, STANDARD_MR_PROCESSING_FLOW.md §4.1 | ✅ 問題なし |
| `detect_environment_files(file_list)` | CLASS_IMPLEMENTATION_SPEC.md §7.3 | ✅ 問題なし |
| `analyze_environment_files(detected_files)` | CLASS_IMPLEMENTATION_SPEC.md §7.3 | ✅ 問題なし |

### PrePlanningManager（CLASS_IMPLEMENTATION_SPEC.md §8）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `PrePlanningManager` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8, AUTOMATA_CODEX_SPEC.md §2.3.3 | ✅ 問題なし |
| `execute()` | CLASS_IMPLEMENTATION_SPEC.md §8.3 | ✅ 問題なし |
| `select_execution_environment()` | CLASS_IMPLEMENTATION_SPEC.md §8.3 | ✅ 問題なし |

### MCPClient関連（CLASS_IMPLEMENTATION_SPEC.md §9）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `MCPClient` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §9.1, AUTOMATA_CODEX_SPEC.md §9, CLASS_IMPLEMENTATION_SPEC.md §2.4（MCPClientFactory）| ✅ 問題なし |
| `MCPClient.connect()` | CLASS_IMPLEMENTATION_SPEC.md §9.1.3 | ✅ 問題なし |
| `MCPClient.list_tools()` | CLASS_IMPLEMENTATION_SPEC.md §9.1.3 | ✅ 問題なし |
| `MCPClient.call_tool(tool_name, arguments)` | CLASS_IMPLEMENTATION_SPEC.md §9.1.3 | ✅ 問題なし |
| `MCPClient.disconnect()` | CLASS_IMPLEMENTATION_SPEC.md §9.1.3 | ✅ 問題なし |
| `EnvironmentAwareMCPClient` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §9.2, AUTOMATA_CODEX_SPEC.md §9 | ✅ 問題なし |
| `EnvironmentAwareMCPClient.call_tool(tool_name, arguments)` | CLASS_IMPLEMENTATION_SPEC.md §9.2.3 | ✅ 問題なし |

### その他の主要クラス（CLASS_IMPLEMENTATION_SPEC.md §8（重複セクション番号））

> **注意**: CLASS_IMPLEMENTATION_SPEC.md のセクション番号「§8」が二重に存在する（§8: PrePlanningManager以降と §8: その他の主要クラス）。これはドキュメント構造の誤りである（矛盾14）。

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `TodoManagementTool` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8.1（その他主要クラス）, AGENT_DEFINITION_SPEC.md §3.2（todo_list MCPサーバー）| ✅ 問題なし（§8.1に詳細設計あり） |
| `TodoManagementTool.create_todo_list(project_id, mr_iid, todos)` | CLASS_IMPLEMENTATION_SPEC.md §8.1.3 | ✅ 問題なし |
| `TodoManagementTool.sync_to_gitlab(project_id, mr_iid)` | CLASS_IMPLEMENTATION_SPEC.md §8.1.3 | ✅ 問題なし |
| `IssueToMRConverter` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8.2（その他主要クラス）, AUTOMATA_CODEX_SPEC.md §5.0 | ✅ 問題なし（§8.2に詳細設計あり） |
| `IssueToMRConverter.convert(issue)` | CLASS_IMPLEMENTATION_SPEC.md §8.2.3 | ✅ 問題なし |
| `ProgressReporter` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8.3（その他主要クラス）, AUTOMATA_CODEX_SPEC.md §6 | ✅ 問題なし |
| `ProgressReporter.initialize(context, mr_iid)` | CLASS_IMPLEMENTATION_SPEC.md §8.3.3 | ✅ 問題なし |
| `ProgressReporter.report_progress(context, event, node_id, details)` | CLASS_IMPLEMENTATION_SPEC.md §8.3.3 | ✅ 問題なし |
| `ProgressReporter.finalize(context, mr_iid, summary)` | CLASS_IMPLEMENTATION_SPEC.md §8.3.3 | ✅ 問題なし |
| `MermaidGraphRenderer` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8.4（その他主要クラス）| ✅ 問題なし |
| `MermaidGraphRenderer.render(node_states)` | CLASS_IMPLEMENTATION_SPEC.md §8.4.3 | ✅ 問題なし |
| `ProgressCommentManager` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §8.5（その他主要クラス）| ✅ 問題なし |
| `ProgressCommentManager.create_progress_comment(context, mr_iid, node_states)` | CLASS_IMPLEMENTATION_SPEC.md §8.5.3 | ✅ 問題なし |
| `ProgressCommentManager.update_progress_comment(context, mr_iid, node_states, event_summary, llm_response, error_detail)` | CLASS_IMPLEMENTATION_SPEC.md §8.5.3 | ✅ 問題なし |
| `TaskInheritanceContextProvider` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §4.5（Custom Provider群）, AUTOMATA_CODEX_SPEC.md §8.6 | ✅ 問題なし |
| `TaskInheritanceContextProvider.before_run(...)` | CLASS_IMPLEMENTATION_SPEC.md §4.5.4 | ✅ 問題なし |
| `TaskInheritanceContextProvider._get_past_tasks_async()` | CLASS_IMPLEMENTATION_SPEC.md §4.5.4 | ✅ 問題なし |
| `TaskInheritanceContextProvider._format_inheritance_data()` | CLASS_IMPLEMENTATION_SPEC.md §4.5.4 | ✅ 問題なし |
| `DefinitionLoader` クラス全体 | AUTOMATA_CODEX_SPEC.md §4.4 | ⚠️ **情報不十分**: AUTOMATA_CODEX_SPEC.md §4.4に処理概要が記載されているが、CLASS_IMPLEMENTATION_SPEC.md に独立した設計章が存在しない |
| `WorkflowBuilder` クラス全体 | AUTOMATA_CODEX_SPEC.md §2.3.3 | ⚠️ **情報不十分**: AUTOMATA_CODEX_SPEC.md §2.3.3に記載があるが、CLASS_IMPLEMENTATION_SPEC.md に独立した設計章が存在しない |

### GuidelineLearningAgent（CLASS_IMPLEMENTATION_SPEC.md §10）

| クラス/メソッド | 記述ドキュメント/章 | 問題 |
|---------------|-------------------|------|
| `GuidelineLearningAgent` クラス全体 | CLASS_IMPLEMENTATION_SPEC.md §10, AUTOMATA_CODEX_SPEC.md §11 | ✅ 問題なし |

### クラス設計情報が存在しないクラス

AUTOMATA_CODEX_SPEC.md 等で言及されているが、CLASS_IMPLEMENTATION_SPEC.md に設計章が存在しないクラス。

| クラス | 言及ドキュメント/章 | 問題 |
|-------|-------------------|------|
| `BranchMergeExecutor` | AUTOMATA_CODEX_SPEC.md §4.4.2, MULTI_MR_PROCESSING_FLOW.md §4.6 | ❌ **設計情報なし**: 機能の概要説明のみで、CLASS_IMPLEMENTATION_SPEC.md にクラス設計章が存在しない |
| `TaskHandler` | AUTOMATA_CODEX_SPEC.md §2.2.2 | ❌ **設計情報なし**: `handle()`, `_should_convert_issue_to_mr()`, `_convert_issue_to_mr()` 等のメソッドが言及されているが、CLASS_IMPLEMENTATION_SPEC.md に設計章が存在しない |
| `TaskDBManager` | AUTOMATA_CODEX_SPEC.md §2.3.4 | ❌ **設計情報なし**: DB記録・重複排除の責務が記載されているが、CLASS_IMPLEMENTATION_SPEC.md に設計章が存在しない |
| `GitLabClient` | AUTOMATA_CODEX_SPEC.md §7.2 | ⚠️ **情報不十分**: §7.2 に責務と主要メソッドグループの概要が記載されているが、CLASS_IMPLEMENTATION_SPEC.md に詳細な処理フローが存在しない |
| `Producer（producer.py）` | AUTOMATA_CODEX_SPEC.md §4.3（Producer）, §2.2.1 | ⚠️ **情報不十分**: 処理フローが記載されているが、CLASS_IMPLEMENTATION_SPEC.md に設計章が存在しない |
| `Consumer（consumer.py）` | AUTOMATA_CODEX_SPEC.md §4.3（Consumer）, §2.2.2 | ⚠️ **情報不十分**: 処理フローが記載されているが、CLASS_IMPLEMENTATION_SPEC.md に設計章が存在しない |
| `ConfigManager` | AUTOMATA_CODEX_SPEC.md §14.2（設定管理クラス設計）| ⚠️ **情報不十分**: §14.2 に概要と主要メソッドが記載されているが、CLASS_IMPLEMENTATION_SPEC.md に詳細処理フローが存在しない |

---

## 矛盾サマリー

### 重大な矛盾（実装に影響が大きい）

| # | 矛盾の内容 | 関係するドキュメント |
|---|-----------|-------------------|
| 1 | `standard_mr_processing_agents.json` の実行エージェント（code_generation, bug_fix, test_creation, documentation）、コードレビュー/テスト評価エージェントの `output_keys`/`input_keys` が単数形（`execution_result`）、仕様ドキュメントは複数形（`execution_results`） | standard_mr_processing_agents.json, AGENT_DEFINITION_SPEC.md §4.1, STANDARD_MR_PROCESSING_FLOW.md §2 |
| 2 | `GRAPH_DEFINITION_SPEC.md §4.1` のインライン標準グラフJSONに `code_generation_reflection` 等のリフレクションノードが欠落 | GRAPH_DEFINITION_SPEC.md §4.1, standard_mr_processing_graph.json |
| 3 | `STANDARD_MR_PROCESSING_FLOW.md §3` のフロー図でコードレビューとテスト実行評価の順序が実JSONと逆（図: code_review→test_execution_evaluation、JSON: test_execution_evaluation→code_review） | STANDARD_MR_PROCESSING_FLOW.md §3, standard_mr_processing_graph.json |
| 4 | `AGENT_DEFINITION_SPEC.md §4.1`（standard）と `standard_mr_processing_agents.json` でplan_reflectionの入力キー（4 vs 6）と出力キー（1 vs 8）が大きく異なる | AGENT_DEFINITION_SPEC.md §4.1, standard_mr_processing_agents.json |
| 5 | `AGENT_DEFINITION_SPEC.md §4.2`（multi）と `multi_codegen_mr_processing_agents.json` でplan_reflectionの入力キー（2 vs 6）・出力キー（1 vs 8）・MCPサーバー（1 vs 2）が大きく異なる | AGENT_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_agents.json |
| 6 | `DATABASE_SCHEMA_SPEC.md §3.1` のJSONB例で `executor_type`（graph_definition）、`tools`（agent_definition）、`prompt_id`（prompt_definition）のフィールド名が実仕様（executor_class, mcp_servers, id）と異なる | DATABASE_SCHEMA_SPEC.md §3.1, GRAPH_DEFINITION_SPEC.md, AGENT_DEFINITION_SPEC.md, PROMPT_DEFINITION_SPEC.md |
| 7 | `GRAPH_DEFINITION_SPEC.md §4.2` のマルチコード生成グラフインラインJSONが実JSON（multi_codegen_mr_processing_graph.json）と大幅に異なる（実JSONには多数のノードが存在） | GRAPH_DEFINITION_SPEC.md §4.2, multi_codegen_mr_processing_graph.json |

### 中程度の矛盾

| # | 矛盾の内容 | 関係するドキュメント |
|---|-----------|-------------------|
| 8 | `AGENT_DEFINITION_SPEC.md §6.3` の plan_reflection に `env_ref: "plan"` と記載されているが、AUTOMATA_CODEX_SPEC.md ではreflectionロールはenv_ref省略のみ許容と明記 | AGENT_DEFINITION_SPEC.md §6.3, AUTOMATA_CODEX_SPEC.md §4.4.2 |
| 9 | `STANDARD_MR_PROCESSING_FLOW.md §3` のフロー図で code_generation_reflection → code_review へ直接遷移しているが、実JSONでは execution_type_branch を経由する | STANDARD_MR_PROCESSING_FLOW.md §3, standard_mr_processing_graph.json |
| 10 | `AGENT_DEFINITION_SPEC.md §4.1` の task_classifier の `output_keys` に `selected_environment` が含まれているが、標準JSONには含まれない | AGENT_DEFINITION_SPEC.md §4.1, standard_mr_processing_agents.json |
| 11 | `CLASS_IMPLEMENTATION_SPEC.md §2.1` に WorkflowFactory メソッド `_inject_learning_node()` の詳細処理フローが存在しない | CLASS_IMPLEMENTATION_SPEC.md §2.1, AUTOMATA_CODEX_SPEC.md §4.4.2 |
| 12 | `CLASS_IMPLEMENTATION_SPEC.md §2.2` に ExecutorFactory メソッド `create_branch_merge()` が存在しない | CLASS_IMPLEMENTATION_SPEC.md §2.2, AUTOMATA_CODEX_SPEC.md §4.4.2 |
| 13 | `CLASS_IMPLEMENTATION_SPEC.md` に `BranchMergeExecutor` の設計章が存在しない | CLASS_IMPLEMENTATION_SPEC.md, MULTI_MR_PROCESSING_FLOW.md §4.6 |

### 軽微な矛盾・誤字

| # | 矛盾の内容 | 関係するドキュメント |
|---|-----------|-------------------|
| 14 | `CLASS_IMPLEMENTATION_SPEC.md` のセクション番号「§8」が二重に存在する（ドキュメント構造の誤り） | CLASS_IMPLEMENTATION_SPEC.md §8（EnvironmentAnalyzer等）, §8（その他の主要クラス） |
| 15 | `PROMPTS.md §2`（コード生成 Planning Agent）のプロンプト本文に誤字「徒底読み」（「徹底的に読み」の誤り） | PROMPTS.md §2 |
| 16 | `WorkflowFactory._build_nodes()` のシグネチャが AUTOMATA_CODEX_SPEC.md では `user_id` を含む4引数、CLASS_IMPLEMENTATION_SPEC.md では3引数 | AUTOMATA_CODEX_SPEC.md §4.4.2, CLASS_IMPLEMENTATION_SPEC.md §2.1 |
| 17 | `multi_codegen_mr_processing_agents.json` の `code_generation_reflection.description` が「バグ修正の成果物を検証」のみで、standard版の「コード生成・バグ修正の成果物を検証」と説明が不一致 | multi_codegen_mr_processing_agents.json, standard_mr_processing_agents.json |
| 18 | `MULTI_MR_PROCESSING_FLOW.md §2` の `code_review` 入力キーに `execution_result`（単数）が記載されているが、実JSONには存在しない | MULTI_MR_PROCESSING_FLOW.md §2, multi_codegen_mr_processing_agents.json |

### SPEC_CHECK.md 自体の誤記（前バージョンから修正済み）

前バージョンのチェックレポート自体に以下の誤記が存在した。本バージョンで修正済み。

| # | 誤記の内容 | 修正内容 |
|---|-----------|---------|
| S1 | `USER_MANAGEMENT_SPEC.md` の §1〜§7 章名が全て誤記（例: §1「ユーザー管理概要」→実際は「概要」、§2「ユーザーデータモデル」→実際は「ユーザー登録フロー」など）。また §8〜§9 が完全欠落 | 実際の章構造（§1〜§9）に基づき修正済み |
| S2 | `DATABASE_SCHEMA_SPEC.md` の章番号が全てずれており誤記（§4を「tasksテーブル」と記載したが実際は§4.1、§5を「workflow_execution_states」と記載したが実際は§4.5.1など）。§8〜§13が完全欠落 | 実際の章番号（§4.1, §4.5.1, §4.5.2, §5.1〜§5.5, §6.1, §7.1, §8〜§13）に修正し欠落章を追加 |
| S3 | `PROMPTS.md` §11〜§16 の章タイトルが実際のドキュメントと異なる順序で誤記（§11「Code Generation Reflection」→実際は「Test Execution & Evaluation Agent」、§14「Code Review Agent」→実際は「Code Generation Reflection Agent」など）。§17〜§20（multi_codegen専用プロンプト）が完全欠落 | 実際の章順序に修正し §17〜§20 を追加 |
| S4 | `STANDARD_MR_PROCESSING_FLOW.md` の §1.1〜§1.3、§2.1、§4.6〜§4.8（§4.8.1〜§4.8.8含む）、§5〜§7 が完全欠落 | 欠落章を全て追加 |
| S5 | `MULTI_MR_PROCESSING_FLOW.md` の §1.1〜§1.4、§2.1〜§2.2、§3.1〜§3.2、§4.8、§5〜§7 が完全欠落 | 欠落章を全て追加 |
| S6 | `AGENT_DEFINITION_SPEC.md` §6.5〜§6.7 の章タイトルが誤記（§6.5「Code Review Agent」→実際は「Test Execution & Evaluation Agent」、§6.7「Test Execution Evaluation Agent」→実際は「Execution Reflection Agent群」など）。§6.2.1〜§6.2.4、§6.4.1〜§6.4.4、§6.6.1〜§6.6.2、§6.7.1〜§6.7.3 の詳細が欠落 | 実際の章構造に修正し詳細を追加 |
| S7 | `GRAPH_DEFINITION_SPEC.md` §3.1、§3.3、§4.2.1、§5〜§6 が完全欠落 | 欠落章を全て追加 |
| S8 | `PROMPT_DEFINITION_SPEC.md` §3.2、§4.2、§5〜§6 が完全欠落 | 欠落章を全て追加 |
| S9 | クラス/メソッドの完全性チェックで `MermaidGraphRenderer`（§8.4）、`ProgressCommentManager`（§8.5）、`TodoManagementTool`（§8.1）のメソッド詳細が完全欠落 | 各クラスの全メソッドを追加 |
| S10 | `IssueToMRConverter` が「設計情報なし（❌）」と誤記されていたが、実際は CLASS_IMPLEMENTATION_SPEC.md §8.2 に詳細設計が存在する | 「✅ 問題なし」に修正し「クラス設計情報が存在しないクラス」リストから除外 |
| S11 | `TodoManagementTool` が「情報不十分（⚠️）」と分類されていたが、実際は CLASS_IMPLEMENTATION_SPEC.md §8.1 に詳細設計が存在する | 「✅ 問題なし」に修正し「クラス設計情報が存在しないクラス」リストから除外 |
| S12 | `MCPClient` の全メソッド（connect, list_tools, call_tool, disconnect）と `EnvironmentAwareMCPClient.call_tool()` がチェック対象から完全欠落 | 各メソッドをチェック対象に追加 |
| S13 | `EnvironmentAnalyzer` と `PrePlanningManager` のメソッド詳細（detect_environment_files, analyze_environment_files, execute, select_execution_environment）がチェック対象から欠落 | 各メソッドをチェック対象に追加 |
| S14 | `ExecutionEnvironmentManager` の複数メソッド（get_environment, cleanup_environments, load_environment_mapping, start_all_containers, check_containers_exist）がチェック対象から欠落し、既存メソッドのシグネチャも不正確だった | 全メソッドを正確なシグネチャで追加 |
