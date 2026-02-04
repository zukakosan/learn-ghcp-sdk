# Python 仮想環境の管理ベストプラクティス

## 概要
Python 仮想環境の命名規則、管理方法、uv コマンドの使い方について解説します。

---

## 1. 仮想環境の命名規則

### 一般的な命名パターン

**ドット付き（隠しディレクトリ）:**
- `.venv` - **最も一般的**（Python公式ドキュメントでも推奨）
- `.env` - 使われるが、環境変数ファイルと混同しやすい

**ドットなし:**
- `venv` - よく使われる
- `env` - よく使われる
- `virtualenv` - 古いスタイル

### ドットを付けるメリット・デメリット

| 観点 | 詳細 |
|------|------|
| **メリット** | `ls` で表示されない（隠しディレクトリ）<br>プロジェクトのルートがすっきり見える<br>`.gitignore` で扱いやすい |
| **デメリット** | 初心者には見つけにくい<br>`ls -a` で確認する必要がある |

### 推奨

- **`.venv`** を使うのが現在の標準的な慣例
- `.test` のような名前は一般的ではない
- テスト用の環境でも `.venv` で統一し、プロジェクトごとに分けるのが良い

---

## 2. 複数環境の管理戦略

### パターン1: プロジェクトごとに分ける（推奨）

```bash
~/projects/
├── project-a/
│   └── .venv/          # project-a 用の環境
├── project-b/
│   └── .venv/          # project-b 用の環境
└── project-c/
    └── .venv/          # project-c 用の環境
```

**これが最も一般的で推奨される方法です。**

### パターン2: 同じプロジェクト内で複数の環境

```bash
~/projects/my-project/
├── .venv/              # デフォルト（本番用）
├── .venv-dev/          # 開発用
├── .venv-test/         # テスト用
└── .venv-py311/        # Python 3.11 専用
```

```bash
# 環境を作成
uv venv .venv-dev

# アクティベート
source .venv-dev/bin/activate
```

### パターン3: ツールで管理

**pyenv + pyenv-virtualenv:**
```bash
# 名前付き環境を作成
pyenv virtualenv 3.11.0 my-project-dev
pyenv virtualenv 3.11.0 my-project-test

# アクティベート
pyenv activate my-project-dev
```

---

## 3. uv コマンドの使い方

### 仮想環境の作成

```bash
# 仮想環境を作成（デフォルトで .venv）
uv venv

# または明示的に名前を指定
uv venv .venv

# Python バージョンを指定して環境作成
uv venv --python 3.11

# 複数の Python バージョン
uv venv .venv-py312 --python 3.12
```

### 仮想環境のアクティベート

```bash
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat
```

### パッケージ管理

```bash
# パッケージをインストール
uv pip install <package-name>

# requirements.txt からインストール
uv pip install -r requirements.txt

# pyproject.toml がある場合、依存関係を同期
uv sync

# パッケージを追加してインストール
uv add <package-name>

# 開発用依存関係を追加
uv add --dev <package-name>
```

### 環境の確認と削除

```bash
# 環境があるか確認
test -d .venv && echo "仮想環境あり" || echo "仮想環境なし"

# どの環境がアクティブか確認
echo $VIRTUAL_ENV

# 環境を削除
rm -rf .venv

# 仮想環境を無効化
deactivate
```

---

## 4. 仮想環境のリスト表示

`uv` には仮想環境をリスト表示する専用コマンドはありません。仮想環境は単なるディレクトリなので、通常のコマンドで確認します:

### ディレクトリを確認

```bash
# カレントディレクトリの仮想環境を表示
ls -la | grep venv

# または
find . -maxdepth 1 -type d -name "*venv*"
```

### プロジェクト内の仮想環境を検索

```bash
# 現在のディレクトリ以下を検索
find . -name "pyvenv.cfg" -exec dirname {} \;

# または bin/activate があるディレクトリを探す
find . -path "*/bin/activate" | sed 's|/bin/activate||'
```

### pyenv で管理している場合

```bash
# pyenv で作成した仮想環境のリスト
pyenv versions

# pyenv-virtualenv のリスト
pyenv virtualenvs
```

---

## 5. .gitignore の設定

複数の仮想環境パターンに対応する `.gitignore`:

```gitignore
# Python virtual environments
.venv*
venv/
env/
ENV/
.env

# pyenv
.python-version

# uv
.uv/
```

---

## 6. ベストプラクティス

### 推奨される運用

1. **基本は1プロジェクト1環境**（`.venv`）
2. 複数必要なら、目的別に名前を付ける（`.venv-dev`, `.venv-test`）
3. `.gitignore` に仮想環境ディレクトリを追加
4. `requirements.txt` または `pyproject.toml` でパッケージを管理
5. `uv` を使うことで高速なパッケージ管理が可能

### uv の特徴

- **高速**: Rust で書かれており、pip より高速
- **シンプル**: プロジェクトごとに `.venv` を作成する設計思想
- **互換性**: pip と同じコマンド体系
- **効率的**: パッケージキャッシュで再利用可能

---

## 7. Git ブランチの管理

### master から main への変更

```bash
# ローカルブランチの名前変更
git branch -m master main

# 新しい main ブランチをプッシュ
git push -u origin main

# 古い master ブランチを削除
git push origin --delete master

# ローカルの追跡ブランチを更新
git fetch origin
git branch -u origin/main main
```

### GitHub でのデフォルトブランチ変更

1. GitHub のリポジトリページへ移動
2. **Settings** → **Branches**
3. Default branch を `main` に変更
4. その後、古い `master` ブランチを削除

---

## 参考リンク
- [uv公式ドキュメント](https://github.com/astral-sh/uv)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 668 – Marking Python base environments as "externally managed"](https://peps.python.org/pep-0668/)

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-02-04 | 初版作成 |
