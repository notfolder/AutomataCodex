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

### 詳細不足

- 🟡 ファイルが空。システム概要・セットアップ手順・使い方が一切記載されていない。他のドキュメントへの参照すらない。

---

## docs/CODE_AGENT_ORCHESTRATOR_SPEC.md

### セクション1〜2: 目的・アーキテクチャ

すべての観点で **問題なし**。

---

### セクション3: ユーザー管理システム

すべての観点で **問題なし**（詳細はUSER_MANAGEMENT_SPEC.mdへの参照で明示）。

---

### セクション4.2.1 WorkflowFactory / 4.4 定義ファイル管理

#### 詳細不足

- 🟡 `DefinitionLoader` クラスの詳細実装（メソッドシグネチャ・処理フロー・SQL・例外仕様）が `CLASS_IMPLEMENTATION_SPEC.md` に存在しない。本セクションに概要は記載されているが、エンジニアが実装開始するには不十分。

---

### セクション4.3.1 ConfigurableAgent の AgentNodeConfig

すべての観点で **問題なし**（`environment_mode: "create"/"inherit"/"none"` として正しく定義されている）。

---

### セクション14.3.9: 移植不要コンポーネント

#### 矛盾

- 🔴 `queueing.py (RabbitMQTaskQueue, InMemoryTaskQueue)` に対して「RabbitMQは使用しない。タスク管理はPostgreSQLとAgent Framework Workflowsで代替」と記載されているが、セクション1.2・2.1・2.2・付録A.12・A.0ではRabbitMQを使用することを明確に記載している。セクション14.3.12の注記にもRabbitMQ使用と記載されており、14.3.9の記述が誤り。

---

### セクション14.4: 機能追加

#### 矛盾

- 🔴 「Web管理画面: Streamlitベースの設定UI」と記載されているが、同ドキュメントのセクション2.3（アーキテクチャ概要）には「Vue.js + FastAPI バックエンド」と記載されており、同一ドキュメント内で矛盾している（後述の USER_MANAGEMENT_SPEC.md の矛盾と連動）。

---

## docs/GRAPH_DEFINITION_SPEC.md

### セクション3.2: ノード定義

すべての観点で **問題なし**（`environment_mode` フィールドで正しく定義されている）。

---

### セクション4.1: standard_mr_processing プリセット

#### 技術的問題

- 🟡 `replan_branch` からのエッジに「軽微修正（needs_revision）」ケースは `code_generation` へのルーティングしか定義されていない。`bug_fix`・`test_creation`・`documentation` タスク種別で同ケースが発生した場合のルーティングエッジが欠落しており、グラフが不完全。

---

### セクション4.2: multi_codegen_mr_processing プリセット

#### 矛盾

- 🟡 セクション見出し `### 4.2` が同一ファイル内に2回出現している（重複見出し）。

---

### セクション5: バリデーション仕様

#### 矛盾

- 🔴 バリデーション仕様の表中に「`requires_environment: true` のノード数を集計」と記載されているが、実際の定義フィールド名はセクション3.2で `environment_mode` と定義されており、`requires_environment` というフィールドは存在しない。バリデーション仕様の記述が誤り（正: `environment_mode: "create"` のノード数を集計）。

---

## docs/AGENT_DEFINITION_SPEC.md

### セクション3.2: toolsに指定可能な値

#### 矛盾

- 🔴 toolsリストに `sync_to_gitlab` が定義されていないが、セクション6（各エージェントノードの詳細）の処理フロー内で「GitLabにコメント投稿」・「sync_to_gitlabツール」という表現が登場する。PROMPT_DEFINITION_SPEC.md の一部プロンプトでも同ツールの使用を指示している。toolsリストへの追加または「GitLab投稿はフレームワークが自動実施」と明示する必要がある。

---

### セクション4.1: standard_mr_processing の plan_reflection

#### 矛盾

- 🔴 `plan_reflection` の `input_keys` が `["plan_result", "todo_list", "task_context"]` と定義されているが、GRAPH_DEFINITION_SPEC.md §4.1 のグラフ定義では `plan_reflection` は `code_review` / `documentation_review` の後に実行される。これらが出力する `review_result` が `input_keys` に含まれていないため、レビュー結果を参照できない。multi_codegen版の `plan_reflection` の定義（`input_keys: ["review_result", "task_context"]`）が正しい設計であり、standard版も同様に修正が必要。

---

### セクション6.2.1〜6.4.4: 各エージェントの「主要設定」箇条書き

#### 矛盾

- 🔴 各エージェントの「エージェント定義の主要設定」に `requires_environment: false` / `requires_environment: true` と記載されているが、JSON仕様（セクション3.2）および CODE_AGENT_ORCHESTRATOR_SPEC.md のAgentNodeConfig定義で採用されているフィールド名は `environment_mode`（値: "create"/"inherit"/"none"）である。`requires_environment` というフィールドはエージェント定義に存在しない。

---

## docs/PROMPT_DEFINITION_SPEC.md

### セクション3.2: デフォルトLLMパラメータ

すべての観点で **問題なし**。

---

### セクション4.1: standard_mr_processing のプロンプト一覧

#### 矛盾

- 🔴 PROMPTS.md のヘッダーに「すべてのプロンプトは日本語で記述する」と明記されているが、本ドキュメントの全 `system_prompt` が英語で記述されている。どちらを正とするか設計上の方針が未定義。PROMPTS.md と PROMPT_DEFINITION_SPEC.md のプロンプトが同一エージェントに対して異なる言語・内容で定義されており、どちらが使用されるか不明確。

---

## docs/DATABASE_SCHEMA_SPEC.md

### セクション1.2: ER図

#### 矛盾（ER図 vs 実テーブル定義）

- 🔴 **`message_compressions` テーブル（カラム名不一致）**: ER図は `original_tokens`, `summary_tokens` と記載しているが、セクション5.2のテーブル定義では `original_token_count`, `compressed_token_count` となっており名前が異なる。実装時にどちらを使用するか判断できない。

- 🔴 **`user_workflow_settings` テーブル（主キーの不一致）**: ER図では `workflow_definition_id PK,FK`（複合主キー）と表記されているが、セクション2.4のテーブル定義では `PRIMARY KEY (user_email)` のみであり、`workflow_definition_id` はNOT NULL制約のみ。

- 🟡 **`user_workflow_settings` テーブル（カラム欠落）**: ER図に `custom_settings TEXT` カラムが記載されているが、セクション2.4のテーブル定義には存在しない。

- 🟡 **`todos` テーブル（カラム欠落）**: ER図に `todo_id INTEGER` カラムが記載されているが、セクション6.1のテーブル定義では `id SERIAL PRIMARY KEY` のみで `todo_id` は存在しない。

---

### セクション2.3: 欠番

#### 詳細不足

- 🟢 セクション番号が「2.2」の次が「2.4」になっており、「2.3」が欠番。

---

### セクション9: データベース初期化SQLの作成順序リスト

#### 詳細不足

- 🟡 作成順序のステップ6が欠番（5の次が7）。
- 🟡 `workflow_execution_states`、`docker_environment_mappings`、`message_compressions` の3テーブルが作成順序リストに記載されていない。初期化SQLが不完全な状態になる可能性がある。

---

## docs/CLASS_IMPLEMENTATION_SPEC.md

### セクション1: ConfigurableAgent

#### 重複

- 🟢 `execute_async()` の処理フロー内で「進捗報告（開始）」のステップが2回連続して記述されている（実装フローとしては1回のはず）。

---

### セクション2.1: WorkflowFactory

#### 詳細不足

- 🟡 `DefinitionLoader` クラスの実装詳細がこのファイルに存在しない。CODE_AGENT_ORCHESTRATOR_SPEC.md §4.4.4 でインタフェースが定義されているが、実装詳細（クラス構造・SQL・例外仕様）の記載場所がどのドキュメントにも存在しない。

#### 技術的問題

- 🟡 `resume_workflow()` ステップ6で `Workflow.start_from_node(current_node_id)` を呼び出すと記載しているが、Microsoft Semantic Kernel の Process Framework/Workflow に `start_from_node()` という公開APIは確認できない。ワークフロー再開のためのAPI設計を要確認。

---

### セクション4.2: PlanningContextProvider

#### 矛盾

- 🟡 `provide_ai_context_async()` 内のSQLで `SELECT phase, node_id, plan, result FROM context_planning_history` と記載されており `action_id` を取得していないが、同じクラスの `store_ai_context_async()` のSQLでは `INSERT INTO context_planning_history (task_uuid, phase, node_id, plan, action_id, result)` として `action_id` を書き込んでいる。読み込み時に `action_id` が取得されない設計の不整合。

---

### セクション9: MCPClient関連

#### 矛盾

- 🟢 セクション番号が「## 9. MCPClient関連」だが、サブセクションが「### 7.1 MCPClient」「### 7.2 ...」になっており、番号体系が崩れている（正: 9.1, 9.2）。

---

## docs/PROMPTS.md

### 全体

#### 矛盾

- 🔴 ヘッダーに「すべてのプロンプトは日本語で記述する」とあるが、PROMPT_DEFINITION_SPEC.md §4.1 の対応プロンプトはすべて英語で記述されている。どちらを採用するか、または両方を使用するかの方針が不明確。

- 🟡 セクション4（plan_reflectionプロンプト）の出力フォーマットで `"action": "proceed|revise_plan"` と定義しているが、AGENT_DEFINITION_SPEC.md §5 の ReflectionResult 定義では `action` が `"proceed" / "revise_plan" / "abort"` の3値とされており、`abort` 値の扱いが不統一。

#### 詳細不足

- 🔴 全Planning Agentプロンプト（セクション2〜5）で「`save_planning_history` を使用して計画を保存する」と LLM に指示しているが、`save_planning_history` は AGENT_DEFINITION_SPEC.md §3.2 の `tools` リストに存在しない。実装上は `PlanningContextProvider.store_ai_context_async()` が自動実行するフレームワーク機能であるなら、LLMに指示するツールとして公開するかどうかの設計判断が未定義。

---

## docs/STANDARD_MR_PROCESSING_FLOW.md

### セクション2: エージェント構成表

#### 矛盾

- 🔴 `code_review`・`test_execution_evaluation`・`documentation_review` の入力キーが `execution_result`（単数形）と記載されているが、AGENT_DEFINITION_SPEC.md では辞書型の `execution_results`（複数形）に変更されている。

---

### セクション3.0: 全体フロー図

#### 矛盾

- 🟡 `UserResolve[ユーザー情報取得 User Resolver Agent]` と表記されているが、実装上は `UserResolverExecutor`（`BaseExecutor` のサブクラス）であり、「Agent」は誤り。

---

### セクション3.2: 環境セットアップ

#### 矛盾

- 🔴 「グラフ定義ファイルで `requires_environment: true` が設定されたノードに対しては...」と記載されているが、正しいフィールド名は GRAPH_DEFINITION_SPEC.md §3.2 で定義された `environment_mode: "create"` であり、`requires_environment` というフィールドは存在しない。同ドキュメントの他箇所（行85・行92・行152・行169）でも同様に誤った用語を使用している。

---

### セクション4.4: レビューフェーズ

#### 矛盾

- 🟡 「テスト作成タスクは `code_review` → `plan_reflection` となり `test_execution_evaluation` は通らない」という読み取りができる記述があるが、GRAPH_DEFINITION_SPEC.md §4.1 のグラフ定義では `test_creation → code_review → test_execution_evaluation` のエッジが存在し、テスト作成も `test_execution_evaluation` を通る経路になっている。フロー仕様の確認が必要。

---

### セクション4.7.4: replan_branchの遷移条件

#### 矛盾

- 🟡 `"status": "needs_replan"` というフィールドを条件式で参照しているが、AGENT_DEFINITION_SPEC.md §5 の ReflectionResult 構造に `status` フィールドは定義されていない（`action` フィールドのみ）。

---

## docs/USER_MANAGEMENT_SPEC.md

### セクション7: Web管理画面（概要）

#### 矛盾

- 🔴 「Streamlitベースの管理画面を提供」と記載されているが、同ドキュメント §9.1 では「Vue.js 3 + TypeScript + Vuetify 3」「FastAPI (Python 3.11+)」と記載されており、採用フレームワークが矛盾している。CODE_AGENT_ORCHESTRATOR_SPEC.md §14.4 も Streamlit と記載しており、§9.1 のVue.js記述が浮いている状態。どちらを採用するか決定が必要。

---

### セクション番号体系

#### 重複・詳細不足

- 🟢 セクション6「User Config API」のサブセクションが `5.1`, `5.2`, `5.4` になっており（`6.1`, `6.2`, `6.4` が正）、`5.3` が欠番になっている。
- 🟢 セクション8「ユーザー別トークン統計処理」のサブセクションが `7.1`, `7.2` になっており（`8.1`, `8.2` が正）、番号体系が崩れている。

---

## 問題サマリー

### 🔴 重大（修正必須）

| # | 対象ファイル | セクション | 問題内容 |
|---|---|---|---|
| 1 | CODE_AGENT_ORCHESTRATOR_SPEC.md | §14.3.9 | RabbitMQ使用有無の矛盾（「使用しない」vs 他全箇所で「使用する」） |
| 2 | CODE_AGENT_ORCHESTRATOR_SPEC.md | §14.4 | Web管理画面フレームワーク矛盾（Streamlit vs Vue.js） |
| 3 | GRAPH_DEFINITION_SPEC.md | §5 バリデーション仕様 | `requires_environment: true` という存在しないフィールド名を使用（正: `environment_mode: "create"`） |
| 4 | AGENT_DEFINITION_SPEC.md | §4.1 plan_reflection | standard版のinput_keysに `review_result` が欠落（グラフ上はreview後に実行される） |
| 5 | AGENT_DEFINITION_SPEC.md | §6.2.1〜6.4.4 | `requires_environment: true/false` という存在しないフィールド名を記載（正: `environment_mode`） |
| 6 | AGENT_DEFINITION_SPEC.md | §3.2 toolsリスト | `sync_to_gitlab` が定義されていないが §6・PROMPT_DEFINITION_SPEC.mdで使用を指示 |
| 7 | PROMPTS.md | §2〜5 | `save_planning_history` が tools に未定義。LLMに呼び出しを指示しているが実装手段が不明確 |
| 8 | PROMPTS.md / PROMPT_DEFINITION_SPEC.md | 全体 | プロンプト言語の矛盾（PROMPTS.md: 日本語必須 / PROMPT_DEFINITION_SPEC.md: 英語で記述） |
| 9 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `message_compressions` カラム名の不一致（ER図: `original_tokens` / テーブル定義: `original_token_count`） |
| 10 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `user_workflow_settings` 主キーの不一致（ER図: 複合PK / テーブル定義: `user_email` のみPK） |
| 11 | STANDARD_MR_PROCESSING_FLOW.md | §2 | コンテキストキー名不一致（`execution_result` 単数 vs AGENT_DEFINITION_SPEC の `execution_results` 辞書型） |
| 12 | STANDARD_MR_PROCESSING_FLOW.md | §3.2 | `requires_environment: true` という存在しないフィールド名を使用（正: `environment_mode: "create"`） |
| 13 | USER_MANAGEMENT_SPEC.md | §7 vs §9.1 | Web管理画面フレームワーク矛盾（Streamlit vs Vue.js 3 + FastAPI） |

### 🟡 中程度（実装時に混乱・バグの原因）

| # | 対象ファイル | セクション | 問題内容 |
|---|---|---|---|
| 14 | CODE_AGENT_ORCHESTRATOR_SPEC.md | §4.4.4 | `DefinitionLoader` クラスの実装詳細が CLASS_IMPLEMENTATION_SPEC.md に存在しない |
| 15 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `user_workflow_settings` に `custom_settings TEXT` がER図にあるが定義に存在しない |
| 16 | DATABASE_SCHEMA_SPEC.md | §1.2 ER図 | `todos` に `todo_id INTEGER` がER図にあるが定義に存在しない |
| 17 | DATABASE_SCHEMA_SPEC.md | §9 | 初期化SQL作成順序にStep6欠番、3テーブル（workflow_execution_states等）が欠落 |
| 18 | CLASS_IMPLEMENTATION_SPEC.md | §2.1 | `Workflow.start_from_node()` がSemantic Kernel公式APIとして存在するか要確認 |
| 19 | CLASS_IMPLEMENTATION_SPEC.md | §4.2 | `provide_ai_context_async()` で `action_id` を取得しないが `store` では書き込む不整合 |
| 20 | GRAPH_DEFINITION_SPEC.md | §4.1 | replan_branchからbug_fix/test_creation/documentation向けの「軽微修正」エッジが欠落 |
| 21 | STANDARD_MR_PROCESSING_FLOW.md | §3.0 | `UserResolve` を「Agent」と表記しているが実装は `Executor`（UserResolverExecutor） |
| 22 | STANDARD_MR_PROCESSING_FLOW.md | §4.4 | テスト作成タスクが test_execution_evaluation を通るかどうかの記述がグラフ定義と矛盾 |
| 23 | STANDARD_MR_PROCESSING_FLOW.md | §4.7.4 | `status: "needs_replan"` フィールドが ReflectionResult 定義に存在しない |
| 24 | PROMPTS.md | §4 | ReflectionResultの `action` 値域が不統一（PROMPTS.md: 2値 / AGENT_DEFINITION_SPEC.md: 3値） |
| 25 | DATABASE_SCHEMA_SPEC.md | §3.1 JSONBサンプル | `entry_node: "user_resolver"` だが GRAPH_DEFINITION_SPEC.md §4.1 では `"user_resolve"` |

### 🟢 軽微（文書品質の問題）

| # | 対象ファイル | セクション | 問題内容 |
|---|---|---|---|
| 26 | README.md | 全体 | ファイルが空（システム概要・セットアップ手順なし） |
| 27 | DATABASE_SCHEMA_SPEC.md | §2 | セクション2.3が欠番 |
| 28 | CLASS_IMPLEMENTATION_SPEC.md | §1 | `execute_async()` の処理フローでステップ4「進捗報告（開始）」が2回重複 |
| 29 | CLASS_IMPLEMENTATION_SPEC.md | §9 | サブセクション番号が「7.1」「7.2」（正: 9.1, 9.2） |
| 30 | GRAPH_DEFINITION_SPEC.md | §4.2 | セクション見出し `### 4.2` が同一ファイル内に2回出現（重複） |
| 31 | USER_MANAGEMENT_SPEC.md | §6, §8 | セクション番号体系崩れ（§6内で5.x、§8内で7.x） |
