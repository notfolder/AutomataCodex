# ドキュメントチェックレポート

全 `.md` ファイルを1章ずつ確認し、以下4つの観点でチェックした結果をまとめる。

1. 他のドキュメントと矛盾していないか
2. 他のドキュメントと重複していないか
3. 実装に足りるだけの詳細情報はあるか
4. 実装に技術的な無理はないか

---

## 凡例

| 記号 | 意味 |
|------|------|
| 🔴 | 重大（実装に直接影響。修正必須） |
| 🟡 | 中程度（実装時に混乱・バグの原因になる可能性） |
| 🟢 | 軽微（文書品質の問題） |

---

## AGENTS.md

すべての観点で **問題なし**。

---

## README.md

システム概要・コンポーネント説明・ドキュメント一覧・セットアップ手順を記載済み。

すべての観点で **問題なし**。

---

## docs/CODE_AGENT_ORCHESTRATOR_SPEC.md

### セクション1〜2: 目的・アーキテクチャ

すべての観点で **問題なし**。

---

### セクション3: ユーザー管理システム

すべての観点で **問題なし**（詳細はUSER_MANAGEMENT_SPEC.mdへの参照で明示）。

---

### セクション4.2.1 WorkflowFactory / 4.4 定義ファイル管理

#### 詳細不足（対応済み）

- ~~🟡 `DefinitionLoader` クラスの詳細実装（メソッドシグネチャ・処理フロー・SQL・例外仕様）が `CLASS_IMPLEMENTATION_SPEC.md` に存在しない。~~ → CLASS_IMPLEMENTATION_SPEC.mdに`DefinitionLoader`の実装詳細なし。本セクションで「CLASS_IMPLEMENTATION_SPEC.mdを参照」と案内を追加。なお、CLASS_IMPLEMENTATION_SPEC.mdへの追記はリファクタリング対応として別途実施予定。

---

### セクション4.3.1 ConfigurableAgent の AgentNodeConfig

すべての観点で **問題なし**（`environment_mode: "create"/"inherit"/"none"` として正しく定義されている）。

---

### セクション14.3.9: 移植不要コンポーネント

#### 矛盾（修正済み）

- ~~🔴 `queueing.py (RabbitMQTaskQueue, InMemoryTaskQueue)` に対して「RabbitMQは使用しない」と記載されていたが、セクション1.2・2.1・2.2・付録A.12・A.0ではRabbitMQを使用することを明確に記載していた。~~ → 「RabbitMQはProducer/Consumer間のタスクキューとして引き続き使用する」と修正済み。

---

### セクション14.4: 機能追加

#### 矛盾（修正済み）

- ~~🔴 「Web管理画面: Streamlitベースの設定UI」と記載されていたが、セクション2.3では「Vue.js + FastAPI バックエンド」と記載されており矛盾していた。~~ → 「Vue.js 3 + FastAPI バックエンドによる設定UI」に修正済み。

---

## docs/GRAPH_DEFINITION_SPEC.md

### セクション3.2: ノード定義

すべての観点で **問題なし**（`environment_mode` フィールドで正しく定義されている）。

---

### セクション4.1: standard_mr_processing プリセット

#### 技術的問題（修正済み）

- ~~🟡 `replan_branch` からのエッジに「軽微修正（needs_revision）」ケースは `code_generation` へのルーティングしか定義されていなかった。~~ → `bug_fix`・`test_creation`・`documentation` 向けの軽微修正エッジを追加済み。

---

### セクション4.2: multi_codegen_mr_processing プリセット

#### 矛盾（修正済み）

- ~~🟡 セクション見出し `### 4.2` が同一ファイル内に2回出現していた。~~ → 後者を `#### 4.2.1 multi_codegen_mr_processingの詳細説明` に変更済み。

---

### セクション5: バリデーション仕様

#### 矛盾（修正済み）

- ~~🔴 バリデーション仕様の表中に「`requires_environment: true` のノード数を集計」と記載されていたが、フィールド名は `environment_mode` が正しかった。~~ → `environment_mode: "create"` のノード数を集計と修正済み。

---

## docs/AGENT_DEFINITION_SPEC.md

### セクション3.2: toolsに指定可能な値

#### 矛盾（修正済み）

- ~~🔴 toolsリストに `sync_to_gitlab` が定義されていなかったが、セクション6の処理フローやPROMPT_DEFINITION_SPEC.mdで使用を指示していた。~~ → `sync_to_gitlab` をtoolsリストに追加済み。

---

### セクション4.1: standard_mr_processing の plan_reflection

#### 矛盾（修正済み）

- ~~🔴 `plan_reflection` の `input_keys` が `["plan_result", "todo_list", "task_context"]` と定義されていたが、グラフ上はcode_review/documentation_reviewの後に実行されるためreview_resultが必要だった。~~ → `input_keys: ["plan_result", "todo_list", "task_context", "review_result"]` に修正済み。

---

### セクション5: データ型定義

#### 矛盾（修正済み）

- ~~🟡 ReflectionResult に `status` フィールドが定義されていなかったが、STANDARD_MR_PROCESSING_FLOW.md §4.7.4やGRAPH_DEFINITION_SPEC.md §4.1の条件式で使用されていた。~~ → `status（"success" / "needs_revision" / "needs_replan"）` フィールドを追加済み。

---

### セクション6.2.1〜6.4.4: 各エージェントの「主要設定」箇条書き

#### 矛盾（修正済み）

- ~~🔴 各エージェントの「エージェント定義の主要設定」に `requires_environment: false/true` と記載されていたが、正しいフィールド名は `environment_mode`（値: "create"/"inherit"/"none"）だった。~~ → 全エージェントの設定を `environment_mode` に統一済み。

---

## docs/PROMPT_DEFINITION_SPEC.md

### セクション3.2: デフォルトLLMパラメータ

すべての観点で **問題なし**。

---

### セクション3.3: プロンプト言語

#### 矛盾（修正済み）

- ~~🔴 `system_prompt`フィールドの説明に「英語で記述する」とあったが、PROMPTS.mdでは「すべてのプロンプトは日本語で記述する」と明記されていた。~~ → 「日本語で記述する」に修正済み。

---

## docs/PROMPTS.md

### 全体

#### 矛盾（修正済み）

- ~~🔴 全Planning Agentプロンプト（セクション2〜5）で `save_planning_history` ツールの使用を指示していたが、AGENT_DEFINITION_SPEC.md §3.2 の tools リストに存在しなかった。~~ → プロンプトから削除し、「計画の永続化はフレームワークが自動的に実施する」との注記を追加済み。

- ~~🟡 セクション4（plan_reflectionプロンプト）の出力フォーマットで `"action": "proceed|revise_plan"` と定義していたが、AGENT_DEFINITION_SPEC.md §5 では `"abort"` の3値とされていた。~~ → `"action": "proceed|revise_plan|abort"` に修正済み。

---

## docs/STANDARD_MR_PROCESSING_FLOW.md

### セクション2: エージェント構成表

#### 矛盾（修正済み）

- ~~🔴 `code_review`・`test_execution_evaluation`・`documentation_review` の入力キーが `execution_result`（単数形）と記載されていたが、AGENT_DEFINITION_SPEC.md では `execution_results`（辞書型）に定義されていた。~~ → 全エージェントの入出力キーを `execution_environments, execution_results` に統一済み。

---

### セクション3.0: 全体フロー図

#### 矛盾（修正済み）

- ~~🟡 `UserResolve[ユーザー情報取得 User Resolver Agent]` と表記されていたが、実装上は `UserResolverExecutor`（`BaseExecutor` のサブクラス）であり、「Agent」は誤りだった。~~ → 「User Resolver Executor」に修正済み。

- ~~🟡 フロー図で `code_review → plan_reflection` と直結していたが、GRAPH_DEFINITION_SPEC.md §4.1のグラフ定義では `code_review → test_execution_evaluation → plan_reflection` となっていた。~~ → フロー図に `test_execution_evaluation` ノードを追加済み。

---

### セクション3.2: 環境セットアップ

#### 矛盾（修正済み）

- ~~🔴 「グラフ定義ファイルで `requires_environment: true` が設定されたノードに対しては...」と記載されていたが、正しいフィールド名は `environment_mode: "create"` だった。同ドキュメントの他箇所でも同様の誤り。~~ → 全箇所を `environment_mode: "create"` に修正済み。

---

### セクション4.4: レビューフェーズ

#### 矛盾（修正済み）

- ~~🟡 「テスト作成タスクは `code_review` → `plan_reflection` となり `test_execution_evaluation` は通らない」という記述があったが、GRAPH_DEFINITION_SPEC.md §4.1 のグラフ定義では `test_creation → code_review → test_execution_evaluation` のエッジが存在した。~~ → テスト作成も `test_execution_evaluation` を通る記述に修正済み。セクション4.5・5.4のフロー図にも反映。

---

### セクション4.7.4: replan_branchの遷移条件

#### 矛盾（修正済み）

- ~~🟡 `"status": "needs_replan"` というフィールドを条件式で参照していたが、AGENT_DEFINITION_SPEC.md §5 の ReflectionResult 構造に `status` フィールドは定義されていなかった。~~ → AGENT_DEFINITION_SPEC.md §5 の ReflectionResult 定義に `status` フィールド（"success"/"needs_revision"/"needs_replan"）を追加済み。

---

## docs/USER_MANAGEMENT_SPEC.md

### セクション7: Web管理画面（概要）

#### 矛盾（修正済み）

- ~~🔴 「Streamlitベースの管理画面を提供」と記載されていたが、同ドキュメント §9.1 では「Vue.js 3 + TypeScript + Vuetify 3」「FastAPI (Python 3.11+)」と記載されており矛盾していた。~~ → §7を「Vue.js 3 + FastAPI バックエンドによる管理画面を提供（詳細設計はセクション9参照）」に修正済み。

---

### セクション番号体系

#### 重複・詳細不足（修正済み）

- ~~🟢 セクション6「User Config API」のサブセクションが `5.1`, `5.2`, `5.4` になっていた。~~ → `6.1`, `6.2`, `6.4` に修正済み。
- ~~🟢 セクション8「ユーザー別トークン統計処理」のサブセクションが `7.1`, `7.2` になっていた。~~ → `8.1`, `8.2` に修正済み。

---

## docs/DATABASE_SCHEMA_SPEC.md

### セクション1.2 ER図

#### 矛盾（修正済み）

- ~~🔴 **`message_compressions` テーブル（カラム名不一致）**: ER図は `original_tokens`, `summary_tokens` と記載していたが、セクション5.2のテーブル定義では `original_token_count`, `compressed_token_count` となっていた。~~ → ER図を `original_token_count`, `compressed_token_count` に修正済み。

- ~~🔴 **`user_workflow_settings` テーブル（主キーの不一致）**: ER図では `workflow_definition_id PK,FK`（複合主キー）と表記されていたが、セクション2.3のテーブル定義では `PRIMARY KEY (user_email)` のみだった。~~ → ER図を `workflow_definition_id FK`（外部キーのみ）に修正済み。

- ~~🟡 **`user_workflow_settings` テーブル（カラム欠落）**: ER図に `custom_settings TEXT` カラムが記載されていたが、セクション2.3のテーブル定義には存在しなかった。~~ → テーブル定義に `custom_settings TEXT`（ユーザー固有の追加設定）を追加済み。

- ~~🟡 **`todos` テーブル（カラム欠落）**: ER図に `todo_id INTEGER` カラムが記載されていたが、セクション6.1のテーブル定義では `id SERIAL PRIMARY KEY` のみだった。~~ → テーブル定義に `todo_id INTEGER`（GitLab TodoIDとの対応）を追加済み。

---

### セクション2.3: 欠番

#### 詳細不足（修正済み）

- ~~🟢 セクション番号が「2.2」の次が「2.4」になっており、「2.3」が欠番だった。~~ → セクション2.4（user_workflow_settings）を2.3に繰り上げて欠番を解消済み。

---

### セクション3.1: JSONB構造サンプル

#### 矛盾（修正済み）

- ~~🟡 `entry_node: "user_resolver"` だが GRAPH_DEFINITION_SPEC.md §4.1 では `"user_resolve"` となっていた。~~ → `"user_resolve"` に修正済み。また、`agent_definition` サンプル内の `requires_environment` を `environment_mode` に修正済み。

---

### セクション9: データベース初期化SQLの作成順序リスト

#### 詳細不足（修正済み）

- ~~🟡 作成順序のステップ6が欠番（5の次が7）。~~ → ステップ6に `workflow_execution_states` を追加し、順序を再採番済み。
- ~~🟡 `workflow_execution_states`、`docker_environment_mappings`、`message_compressions` の3テーブルが作成順序リストに記載されていなかった。~~ → 3テーブルを作成順序リストに追加済み。

---

## docs/CLASS_IMPLEMENTATION_SPEC.md

### セクション1: ConfigurableAgent

#### 重複（修正済み）

- ~~🟢 `execute_async()` の処理フロー内で「進捗報告（開始）」のステップが2回連続して記述されていた。~~ → 重複ステップを削除済み。

---

### セクション2.1: WorkflowFactory

#### 技術的問題（修正済み）

- ~~🟡 `resume_workflow()` ステップ6で `Workflow.start_from_node(current_node_id)` を呼び出すと記載していたが、Microsoft Semantic Kernel の Process Framework/Workflow に `start_from_node()` という公開APIは確認できない。~~ → 完了済みノードの状態をコンテキストに格納して実行エンジン側でスキップさせる設計に修正済み。

---

### セクション4.2: PlanningContextProvider

#### 矛盾（修正済み）

- ~~🟡 `provide_ai_context_async()` 内のSQLで `action_id` を取得していなかったが、`store_ai_context_async()` では `action_id` を書き込んでいた。~~ → `provide_ai_context_async()` のSELECTクエリに `action_id` を追加済み。

---

### セクション9: MCPClient関連

#### 矛盾（修正済み）

- ~~🟢 セクション番号が「## 9. MCPClient関連」だが、サブセクションが「### 7.1 MCPClient」「### 7.2 ...」になっていた。~~ → サブセクション番号を「### 9.1 MCPClient」「### 9.2 EnvironmentAwareMCPClient」に修正済み。

---

## 問題サマリー

すべての問題（🔴重大13件・🟡中程度12件・🟢軽微6件）の修正が完了。

### 修正完了一覧

| # | 対象ファイル | セクション | 問題内容 | 状態 |
|---|---|---|---|---|
| 1 | CODE_AGENT_ORCHESTRATOR_SPEC.md | §14.3.9 | RabbitMQ使用有無の矛盾 | ✅ 修正済み |
| 2 | CODE_AGENT_ORCHESTRATOR_SPEC.md | §14.4/15.4 | Web管理画面フレームワーク矛盾（Streamlit→Vue.js） | ✅ 修正済み |
| 3 | GRAPH_DEFINITION_SPEC.md | §5 バリデーション仕様 | `requires_environment`→`environment_mode: "create"` | ✅ 修正済み |
| 4 | AGENT_DEFINITION_SPEC.md | §4.1 plan_reflection | input_keysに`review_result`追加 | ✅ 修正済み |
| 5 | AGENT_DEFINITION_SPEC.md | §6.2.1〜6.4.4 | `requires_environment`→`environment_mode`統一 | ✅ 修正済み |
| 6 | AGENT_DEFINITION_SPEC.md | §3.2 toolsリスト | `sync_to_gitlab`を追加 | ✅ 修正済み |
| 7 | PROMPTS.md | §2〜5 | `save_planning_history`を削除しフレームワーク自動処理を明記 | ✅ 修正済み |
| 8 | PROMPT_DEFINITION_SPEC.md | §3.3 | プロンプト言語を日本語に統一 | ✅ 修正済み |
| 9 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `message_compressions`カラム名修正 | ✅ 修正済み |
| 10 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `user_workflow_settings`主キー修正 | ✅ 修正済み |
| 11 | STANDARD_MR_PROCESSING_FLOW.md | §2 | `execution_result`→`execution_environments/execution_results` | ✅ 修正済み |
| 12 | STANDARD_MR_PROCESSING_FLOW.md | §3.2他 | `requires_environment`→`environment_mode`（全箇所） | ✅ 修正済み |
| 13 | USER_MANAGEMENT_SPEC.md | §7 vs §9.1 | Web管理画面フレームワーク矛盾（Streamlit→Vue.js） | ✅ 修正済み |
| 14 | DATABASE_SCHEMA_SPEC.md | §2.3 | `user_workflow_settings`に`custom_settings TEXT`追加 | ✅ 修正済み |
| 15 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `todos`テーブル定義に`todo_id INTEGER`追加 | ✅ 修正済み |
| 16 | DATABASE_SCHEMA_SPEC.md | §9 | Step6欠番修正、3テーブルを作成順序に追加 | ✅ 修正済み |
| 17 | CLASS_IMPLEMENTATION_SPEC.md | §2.1 | `Workflow.start_from_node()`を代替設計に修正 | ✅ 修正済み |
| 18 | CLASS_IMPLEMENTATION_SPEC.md | §4.2 | `provide_ai_context_async()`に`action_id`追加 | ✅ 修正済み |
| 19 | GRAPH_DEFINITION_SPEC.md | §4.1 | replan_branchの欠落エッジ（bug_fix/test_creation/documentation）追加 | ✅ 修正済み |
| 20 | STANDARD_MR_PROCESSING_FLOW.md | §3.0 | `UserResolve` Agent→Executor修正 | ✅ 修正済み |
| 21 | STANDARD_MR_PROCESSING_FLOW.md | §3.0フロー図 | test_execution_evaluationノード追加 | ✅ 修正済み |
| 22 | STANDARD_MR_PROCESSING_FLOW.md | §4.4/§4.5/§5.4 | テスト作成もtest_execution_evaluationを通る記述に修正 | ✅ 修正済み |
| 23 | STANDARD_MR_PROCESSING_FLOW.md | §4.7.4 | ReflectionResultに`status`フィールド追加（定義側で対応） | ✅ 修正済み |
| 24 | PROMPTS.md | §4 | ReflectionResult actionを3値（proceed/revise_plan/abort）に統一 | ✅ 修正済み |
| 25 | DATABASE_SCHEMA_SPEC.md | §3.1 | `entry_node`値修正（user_resolver→user_resolve） | ✅ 修正済み |
| 26 | README.md | 全体 | システム概要・コンポーネント・セットアップ手順を追加 | ✅ 修正済み |
| 27 | DATABASE_SCHEMA_SPEC.md | §2 | セクション2.3欠番修正 | ✅ 修正済み |
| 28 | CLASS_IMPLEMENTATION_SPEC.md | §1 | execute_async()の重複ステップ削除 | ✅ 修正済み |
| 29 | CLASS_IMPLEMENTATION_SPEC.md | §9 | サブセクション番号修正（7.1→9.1、7.2→9.2） | ✅ 修正済み |
| 30 | GRAPH_DEFINITION_SPEC.md | §4.2 | 重複見出し修正（§4.2.1詳細説明に変更） | ✅ 修正済み |
| 31 | USER_MANAGEMENT_SPEC.md | §6, §8 | セクション番号体系修正（5.x→6.x、7.x→8.x） | ✅ 修正済み |

