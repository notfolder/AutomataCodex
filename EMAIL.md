# emailベースのユーザー識別 → GitLab username ベースへの仕様変更

GitLabではemailの取得が困難なため、ユーザー識別キーをメールアドレスからGitLab usernameに変更する。

## 変更方針

| 変更前 | 変更後 |
|--------|--------|
| `users.email` (PK) | `users.username` (PK、GitLabユーザー名) |
| `users.username` (表示名) | ※削除（usernameがPKを兼ねる） |
| `user_email` カラム/FK | `username` カラム/FK |
| APIパス `{email}` | APIパス `{username}` |
| ログイン: `{"email": "...", "password": "..."}` | ログイン: `{"username": "...", "password": "..."}` |
| コンテキストキー `user_email` | コンテキストキー `username` |
| MR.author.email | MR.author.username |

---

## 変更箇所一覧

### docs/DATABASE_SCHEMA_SPEC.md

| 行番号 | 修正前 | 修正後 |
|--------|--------|--------|
| 47 | `TEXT email PK` (Mermaid図) | `TEXT username PK` |
| 57 | `TEXT user_email PK,FK` (Mermaid図 user_configs) | `TEXT username PK,FK` |
| 84 | `TEXT user_email PK,FK` (Mermaid図 user_llm_settings) | `TEXT username PK,FK` |
| 109 | `TEXT user_email FK` (Mermaid図 tasks) | `TEXT username FK` |
| 216 | `TEXT user_email FK` (Mermaid図 token_usage) | `TEXT username FK` |
| 246 | `ユーザー基本情報を管理する。メールアドレスをプライマリキーとして使用する。` | `ユーザー基本情報を管理する。GitLabユーザー名をプライマリキーとして使用する。` |
| 252 | `\| email \| TEXT \| PRIMARY KEY \| ユーザーのメールアドレス（一意識別子） \|` | `\| username \| TEXT \| PRIMARY KEY \| GitLabユーザー名（一意識別子） \|` |
| 253 | `\| username \| TEXT \| NOT NULL \| ユーザー表示名 \|` | ※削除（usernameがPKを兼ねる） |
| 261 | `PRIMARY KEY (email)` - メールアドレスでの高速検索 | `PRIMARY KEY (username)` - GitLabユーザー名での高速検索 |
| 266 | `メールアドレスは大文字小文字を区別せず、すべて小文字に正規化して保存する` | `usernameはGitLabユーザー名をそのまま保存する` |
| 282 | `\| user_email \| TEXT \| PRIMARY KEY \| ユーザーメールアドレス（外部キー） \|` | `\| username \| TEXT \| PRIMARY KEY \| GitLabユーザー名（外部キー） \|` |
| 308 | `FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE` | `FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE` |
| 311 | `PRIMARY KEY (user_email)` | `PRIMARY KEY (username)` |
| 343 | `\| user_email \| TEXT \| PRIMARY KEY \| ユーザーメールアドレス（外部キー） \|` | `\| username \| TEXT \| PRIMARY KEY \| GitLabユーザー名（外部キー） \|` |
| 350 | `FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE` | `FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE` |
| 354 | `PRIMARY KEY (user_email)` | `PRIMARY KEY (username)` |
| 378 | `\| created_by \| TEXT \| \| 作成者メールアドレス（外部キー、プリセットの場合はNULL） \|` | `\| created_by \| TEXT \| \| 作成者GitLabユーザー名（外部キー、プリセットの場合はNULL） \|` |
| 388 | `FOREIGN KEY (created_by) REFERENCES users(email) ON DELETE SET NULL` | `FOREIGN KEY (created_by) REFERENCES users(username) ON DELETE SET NULL` |
| 484 | `\| user_email \| TEXT \| NOT NULL \| 処理ユーザーのメールアドレス（外部キー） \|` | `\| username \| TEXT \| NOT NULL \| 処理ユーザーのGitLabユーザー名（外部キー） \|` |
| 500 | `FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE` | `FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE` |
| 506 | `idx_tasks_user_email ON (user_email)` | `idx_tasks_username ON (username)` |
| 789 | `\| user_email \| TEXT \| NOT NULL \| ユーザーメールアドレス（外部キー） \|` | `\| username \| TEXT \| NOT NULL \| GitLabユーザー名（外部キー） \|` |
| 796 | `FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE` | `FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE` |
| 800 | `idx_context_metadata_user ON (user_email)` | `idx_context_metadata_user ON (username)` |
| 894 | `\| user_email \| TEXT \| NOT NULL \| ユーザーメールアドレス（外部キー） \|` | `\| username \| TEXT \| NOT NULL \| GitLabユーザー名（外部キー） \|` |
| 904 | `FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE` | `FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE` |
| 909 | `idx_token_usage_user_date ON (user_email, created_at DESC)` | `idx_token_usage_user_date ON (username, created_at DESC)` |
| 1072 | `ユーザー管理: メールアドレスベースの設定管理とAPIキー暗号化` | `ユーザー管理: GitLabユーザー名ベースの設定管理とAPIキー暗号化` |

---

### docs/USER_MANAGEMENT_SPEC.md

| 行番号 | 修正前 | 修正後 |
|--------|--------|--------|
| 5 | `Issue/MRの作成者メールアドレスをキーとして、ユーザーごとのOpenAI APIキーと設定を管理する。` | `Issue/MRの作成者GitLabユーザー名をキーとして、ユーザーごとのOpenAI APIキーと設定を管理する。` |
| 18 | `Admin->>Web: ユーザー登録 (email, username, password, role)` | `Admin->>Web: ユーザー登録 (username, password, role)` |
| 24 | `API->>DB: INSERT users (email, username, password_hash, role)` | `API->>DB: INSERT users (username, password_hash, role)` |
| 25 | `API->>DB: INSERT user_configs (user_email, api_key_encrypted, ...)` | `API->>DB: INSERT user_configs (username, api_key_encrypted, ...)` |
| 89 | `Enter admin email: admin@example.com` | `Enter admin username: admin` |
| 96 | `Email: admin@example.com` | `Username: admin` |
| 103 | `ADMIN_EMAIL=admin@example.com \` | `ADMIN_USERNAME=admin \` |
| 114 | `--email admin@example.com \` | `--username admin \` |
| 130 | `CLI->>Input: メールアドレス、ユーザー名、パスワードを要求` | `CLI->>Input: GitLabユーザー名、パスワードを要求` |
| 132 | `CLI->>CLI: バリデーション（メール形式、パスワード要件）` | `CLI->>CLI: バリデーション（ユーザー名形式、パスワード要件）` |
| 133 | `CLI->>DB: 既存ユーザー確認 (SELECT FROM users WHERE email = ?)` | `CLI->>DB: 既存ユーザー確認 (SELECT FROM users WHERE username = ?)` |
| 142 | `CLI->>DB: INSERT INTO users (email, username, password_hash, role, is_active)` | `CLI->>DB: INSERT INTO users (username, password_hash, role, is_active)` |
| 143 | `CLI->>DB: INSERT INTO user_configs (user_email, デフォルト設定)` | `CLI->>DB: INSERT INTO user_configs (username, デフォルト設定)` |
| 152 | `**メールアドレス**: 有効なメール形式であること` | `**GitLabユーザー名**: 英数字・ハイフン・アンダースコアのみ使用可能であること` |
| 159 | `**既存ユーザーチェック**: 同じメールアドレスのユーザーが存在しないこと` | `**既存ユーザーチェック**: 同じGitLabユーザー名のユーザーが存在しないこと` |
| 181 | `**既存ユーザーエラー**: メールアドレスが既に登録されている場合、エラーメッセージを表示して終了` | `**既存ユーザーエラー**: GitLabユーザー名が既に登録されている場合、エラーメッセージを表示して終了` |
| 199 | `**GET /api/v1/config/{email}**` | `**GET /api/v1/config/{username}**` |
| 200 | `- Purpose: メールアドレスからユーザー設定を取得（LLM設定、コンテキスト圧縮設定、学習機能設定）` | `- Purpose: GitLabユーザー名からユーザー設定を取得（LLM設定、コンテキスト圧縮設定、学習機能設定）` |
| 207 | `- Body: ユーザー情報（email、username、password、role、is_active）とLLM設定...` | `- Body: ユーザー情報（username、password、role、is_active）とLLM設定...` |
| 214 | `**PUT /api/v1/users/{email}**` | `**PUT /api/v1/users/{username}**` |
| 222 | `**PUT /api/v1/users/{email}/password**` | `**PUT /api/v1/users/{username}/password**` |
| 238 | `- Response: ユーザーリスト（email、username、role、is_active、created_at）` | `- Response: ユーザーリスト（username、role、is_active、created_at）` |
| 272 | `- Purpose: メールアドレスとパスワードで認証し、JWTアクセストークンを発行する` | `- Purpose: GitLabユーザー名とパスワードで認証し、JWTアクセストークンを発行する` |
| 274 | `- Body: {"email": "...", "password": "..."}` | `- Body: {"username": "...", "password": "..."}` |
| 276 | `- エラー: メールアドレスまたはパスワードが不正な場合は HTTP 401 を返す` | `- エラー: ユーザー名またはパスワードが不正な場合は HTTP 401 を返す` |
| 311 | `- Query: user_email (optional), period (日数, default 30)` | `- Query: username (optional), period (日数, default 30)` |
| 312 | `- Response: {"period_days": N, "user_email_filter": "...", "stats": [...]}` | `- Response: {"period_days": N, "username_filter": "...", "stats": [...]}` |
| 317 | `- Query: user_email (optional), status (optional)...` | `- Query: username (optional), status (optional)...` |
| 384 | `GET /api/v1/config/{email}で設定取得、PUT /api/v1/users/{email}で設定更新` | `GET /api/v1/config/{username}で設定取得、PUT /api/v1/users/{username}で設定更新` |
| 385 | `PUT /api/v1/users/{email}/passwordで変更` | `PUT /api/v1/users/{username}/passwordで変更` |
| 443 | `│  メールアドレス  │` (ログイン画面) | `│  GitLabユーザー名  │` |
| 502 | `│ ID │ メールアドレス │ 表示名 │ ステータス │` | `│ ID │ GitLabユーザー名 │ ステータス │` |
| 533 | `│  メールアドレス: user1@example.com  │` (ユーザー詳細) | `│  GitLabユーザー名: user1  │` |
| 598 | `│  メールアドレス *  │` (ユーザー登録フォーム) | `│  GitLabユーザー名 *  │` |
| 686 | `│  メールアドレス (変更不可)  │` | `│  GitLabユーザー名 (変更不可)  │` |
| 1079 | `│  メールアドレス: user1@example.com (変更不可)  │` | `│  GitLabユーザー名: user1 (変更不可)  │` |

---

### docs/AUTOMATA_CODEX_SPEC.md

| 行番号 | 修正前 | 修正後 |
|--------|--------|--------|
| 23 | `ユーザー別設定管理: メールアドレスベースでのAPIキー管理と設定分離` | `ユーザー別設定管理: GitLabユーザー名ベースでのAPIキー管理と設定分離` |
| 56 | `ユーザー登録・管理機能（メールアドレスベース）` | `ユーザー登録・管理機能（GitLabユーザー名ベース）` |
| 298 | `ユーザー登録・管理: メールアドレスベースのユーザー管理` | `ユーザー登録・管理: GitLabユーザー名ベースのユーザー管理` |
| 609 | `**責務**: メールアドレスからユーザー設定を取得し、ワークフロー内で利用可能にする` | `**責務**: GitLabユーザー名からユーザー設定を取得し、ワークフロー内で利用可能にする` |
| 617 | `1. ワークフローからメールアドレスを受け取る` | `1. ワークフローからGitLabユーザー名を受け取る` |
| 618 | `2. User Config APIに問い合わせる (GET /api/v1/config/{email})` | `2. User Config APIに問い合わせる (GET /api/v1/config/{username})` |
| 1596 | `\| user_email \| str \| タスク実行ユーザーのメールアドレス \| UserResolverExecutor実行時 \|` | `\| username \| str \| タスク実行ユーザーのGitLabユーザー名 \| UserResolverExecutor実行時 \|` |
| 1873 | `この際、user_emailを渡すことで...user_configsテーブルからユーザーの圧縮設定を読み込む。` | `この際、usernameを渡すことで...user_configsテーブルからユーザーの圧縮設定を読み込む。` |
| 2412 | `user_email: ワークフローコンテキストから取得（token_usageテーブルのFK: users.email）` | `username: ワークフローコンテキストから取得（token_usageテーブルのFK: users.username）` |
| 2422 | `ラベル: model、node_id、user_email` | `ラベル: model、node_id、username` |
| 2426 | `各タスクのuser_emailとtask_uuidで区別` | `各タスクのusernameとtask_uuidで区別` |
| 3108 | `WF->>UserAPI: get_user_config(user_email)` | `WF->>UserAPI: get_user_config(username)` |
| 3981 | `メールアドレスベースの設定管理` | `GitLabユーザー名ベースの設定管理` |

---

### docs/CLASS_IMPLEMENTATION_SPEC.md

| 行番号 | 修正前 | 修正後 |
|--------|--------|--------|
| 300 | `create_agent(..., user_email: str, ...)` | `create_agent(..., username: str, ...)` |
| 314 | `UserConfigClientからuser_emailのLLM設定を取得` | `UserConfigClientからusernameのLLM設定を取得` |
| 658 | `MR.authorからユーザーメールアドレスを取得` | `MR.authorからGitLabユーザー名（author.username）を取得` |
| 661 | `user_config_client.get_user_config(user_email)を呼び出し` | `user_config_client.get_user_config(username)を呼び出し` |
| 665 | `ctx.set_state('user_email', user_email)` | `ctx.set_state('username', username)` |
| 892 | `kwargsからユーザーメールアドレス（user_email）を取得` | `kwargsからGitLabユーザー名（username）を取得` |
| 893 | `compression_serviceが設定されており、user_emailが非空文字列の場合のみ実行する` | `compression_serviceが設定されており、usernameが非空文字列の場合のみ実行する` |
| 894 | `await ContextCompressionService.check_and_compress_async(task_uuid, user_email)` | `await ContextCompressionService.check_and_compress_async(task_uuid, username)` |
| 1032 | `user_email: str - ユーザーメールアドレス（設定取得用）` | `username: str - GitLabユーザー名（設定取得用）` |
| 1038 | `check_and_compress_async(task_uuid: str, user_email: str)` | `check_and_compress_async(task_uuid: str, username: str)` |
| 1043 | `SELECT ... FROM user_configs WHERE user_email = ?` | `SELECT ... FROM user_configs WHERE username = ?` |
| 1249 | `save_token_usage(user_email: str, task_uuid: str, ...)` | `save_token_usage(username: str, task_uuid: str, ...)` |
| 1257 | `token_usage_repository.record_token_usage(user_email, ...)` | `token_usage_repository.record_token_usage(username, ...)` |
| 1372 | `user_email、task_uuid、node_id、model、...を渡す` | `username、task_uuid、node_id、model、...を渡す` |
| 1378 | `labels={'model': model, 'node_id': node_id, 'user_email': user_email}` | `labels={'model': model, 'node_id': node_id, 'username': username}` |

---

### docs/AGENT_DEFINITION_SPEC.md

| 行番号 | 修正前 | 修正後 |
|--------|--------|--------|
| 351 | `TaskContextのフィールドに user_email` | `TaskContextのフィールドに username` |

---

## コード修正方針

仕様変更をコードに反映する際の変更方針を変更点別に記載する。

### 1. データモデル（`shared/models/task.py`）

| 変更前 | 変更後 | 対象フィールド |
|--------|--------|---------------|
| `user_email: str \| None` (Taskモデル) | `username: str \| None` | `Task.user_email` → `Task.username` |
| `user_email: str \| None` (TaskContextモデル) | `username: str \| None` | `TaskContext.user_email` → `TaskContext.username` |

変更方針: Pydanticフィールド名を `user_email` から `username` に変更し、説明文を「GitLabユーザー名」に更新する。

---

### 2. データベース定義（`shared/database/`）

DBはまだ運用していないため、マイグレーションは不要。テーブル作成DDLを直接変更する。

#### 変更対象テーブルとカラム

| テーブル | 変更前カラム名 | 変更後カラム名 |
|--------|--------------|--------------|
| `users` | `email TEXT PRIMARY KEY`, `username TEXT NOT NULL` | `username TEXT PRIMARY KEY`（`email`列削除、`username`列がPKを兼ねる） |
| `user_configs` | `user_email TEXT PRIMARY KEY` | `username TEXT PRIMARY KEY` |
| `user_llm_settings` | `user_email TEXT PRIMARY KEY` | `username TEXT PRIMARY KEY` |
| `tasks` | `user_email TEXT NOT NULL` | `username TEXT NOT NULL` |
| `context_metadata` | `user_email TEXT NOT NULL` | `username TEXT NOT NULL` |
| `token_usage` | `user_email TEXT NOT NULL` | `username TEXT NOT NULL` |

変更方針: テーブル定義ファイル（`shared/database/schema.sql` または DDLを定義している箇所）のカラム名・FK定義・インデックス名を一括変更する。`.lower()` による正規化は不要（usernameは大文字小文字が区別される）。

---

### 3. リポジトリ層（`shared/database/repositories/`）

#### `user_repository.py`

| 変更箇所 | 変更内容 |
|---------|---------|
| 全メソッドシグネチャの `user_email: str` | `username: str` に変更 |
| SQLの `WHERE user_email = $N`, `user_email` カラム参照 | `WHERE username = $N`, `username` に変更 |
| `get_user_by_email()` メソッド | `get_user_by_username()` に改名 |
| `user_email.lower()` 正規化 | 削除（usernameは正規化不要） |

#### `task_repository.py`

| 変更箇所 | 変更内容 |
|---------|---------|
| `create_task(..., user_email: str, ...)` | `create_task(..., username: str, ...)` |
| `get_tasks(..., user_email: str | None, ...)` | `get_tasks(..., username: str | None, ...)` |
| SQL内の `user_email` カラム参照・インデックス | `username` に変更 |
| `user_email.lower()` 正規化 | 削除 |

#### `token_usage_repository.py`

| 変更箇所 | 変更内容 |
|---------|---------|
| `record_token_usage(user_email: str, ...)` | `record_token_usage(username: str, ...)` |
| `get_user_usage(user_email: str, ...)` | `get_user_usage(username: str, ...)` |
| SQL内の `user_email` カラム参照 | `username` に変更 |
| `user_email.lower()` 正規化 | 削除 |

#### `context_repository.py`

| 変更箇所 | 変更内容 |
|---------|---------|
| `save_context_metadata(..., user_email: str, ...)` | `save_context_metadata(..., username: str, ...)` |
| SQL内の `user_email` カラム参照 | `username` に変更 |
| `user_email.lower()` 正規化 | 削除 |

---

### 4. ユーザー設定クライアント（`consumer/user_config_client.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `self.email: str = data.get("email", "")` | `self.username: str = data.get("username", "")` |
| `"email": self.email` (シリアライズ) | `"username": self.username` |

---

### 5. Executorクラス（`consumer/executors/user_resolver_executor.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `author.email` 取得 | `author.username` 取得に変更（GitLab APIはusernameを返す） |
| `user_email = author.email` | `username = author.username` |
| `await self.user_config_client.get_user_config(user_email)` | `await self.user_config_client.get_user_config(username)` |
| `ctx.set_state("user_email", user_email)` | `ctx.set_state("username", username)` |
| ログメッセージ内の `email=` | `username=` |

---

### 6. ファクトリクラス（`consumer/factories/agent_factory.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `create_agent(..., user_email: str, ...)` シグネチャ | `create_agent(..., username: str, ...)` |
| `self.user_config_client.get_user_config(user_email)` | `self.user_config_client.get_user_config(username)` |
| ログメッセージ内の `user_email=` | `username=` |

---

### 7. ミドルウェア（`consumer/middleware/token_usage_middleware.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `context.get_state("user_email")` | `context.get_state("username")` |
| `user_email=user_email or ""` (引数渡し) | `username=username or ""` |
| `"user_email": user_email or ""` (辞書キー) | `"username": username or ""` |

---

### 8. コンテキスト圧縮サービス（`consumer/providers/context_compression_service.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `check_and_compress_async(self, task_uuid: str, user_email: str)` | `check_and_compress_async(self, task_uuid: str, username: str)` |
| `WHERE user_email = $1` SQL | `WHERE username = $1` |
| ログメッセージ内の `user_email=` | `username=` |

---

### 9. Producerコード（`producer/task_getter_from_gitlab.py`、`producer/gitlab_event_handler.py`）

| ファイル | 変更箇所 | 変更内容 |
|---------|---------|---------|
| `task_getter_from_gitlab.py` | `issue_to_task(..., user_email: str)` | `issue_to_task(..., username: str)` |
| `task_getter_from_gitlab.py` | `mr_to_task(..., user_email: str)` | `mr_to_task(..., username: str)` |
| `task_getter_from_gitlab.py` | `get_all_unprocessed_tasks(..., user_email: str)` | `get_all_unprocessed_tasks(..., username: str)` |
| `task_getter_from_gitlab.py` | `issue.author.email` / `mr.author.email` 参照 | `issue.author.username` / `mr.author.username` に変更 |
| `gitlab_event_handler.py` | `author.email` 参照箇所 | `author.username` に変更 |

---

### 10. バックエンドAPI（`backend/user_management/api.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `user_repo.get_user_by_email(body.email)` | `user_repo.get_user_by_username(body.username)` |
| `create_user_config(user_email=email)` | `create_user_config(username=username)` |
| `"user_email": t["user_email"]` (レスポンス) | `"username": t["username"]` |
| `user_email: str \| None = Query(...)` | `username: str \| None = Query(...)` |
| `WHERE user_email = $1` SQL | `WHERE username = $1` |
| APIパス `/{email}` のパスパラメータ | `/{username}` に変更 |

---

### 11. 管理者CLIツール（`backend/user_management/cli/create_admin.py`）

| 変更箇所 | 変更内容 |
|---------|---------|
| `args.email` によるユーザー識別 | `args.username` による識別に統一 |
| `--email` 引数（parser定義） | `--username` のみ残す（emailは削除） |
| `user_email` 変数名・引数名 | `username` に変更 |

---

### 12. テストコード（`tests/`）

上記の本体コード変更に合わせて、`user_email` が登場するすべてのテストファイル内の変数名・モックデータ・アサーション内のキー名を `username` に変更する。対象ファイル:

- `tests/unit/consumer/test_executors.py`
- `tests/unit/consumer/test_middleware.py`
- `tests/unit/consumer/test_factories.py`
- `tests/unit/consumer/test_task_handler.py`
- `tests/unit/consumer/test_strategies.py`
- `tests/unit/consumer/test_providers.py`
- `tests/unit/producer/test_task_getter_from_gitlab.py`
- `tests/unit/backend/test_api.py`
- `tests/unit/shared/test_models.py`
- `tests/unit/shared/test_token_usage_repository.py`
- `tests/unit/shared/test_user_repository.py`
- `tests/unit/shared/test_task_repository.py`
- `tests/integration/test_standard_mr_processing.py`
- `tests/integration/test_multi_codegen_mr_processing.py`
