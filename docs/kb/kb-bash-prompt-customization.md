# Bash プロンプトのカスタマイズ（Python仮想環境 + Gitブランチ表示）

## 概要
Bash のプロンプト（`PS1`）をカスタマイズして、Python 仮想環境名と Git ブランチ名を同時に表示する方法を解説します。

---

## 1. PS1 とは

`PS1` は **Bash のプロンプト文字列（Prompt String 1）** を定義する環境変数です。ターミナルでコマンドを入力する前に表示される文字列をカスタマイズできます。

### 特殊文字一覧

| 要素 | 説明 |
|------|------|
| `\u` | ユーザー名 |
| `\h` | ホスト名 |
| `\H` | 完全なホスト名（FQDN） |
| `\w` | カレントディレクトリのフルパス（`~` 表記） |
| `\W` | カレントディレクトリ名のみ（パスなし） |
| `\$` | 通常ユーザーなら `$`、root なら `#` |
| `\t` | 現在時刻（24時間形式） |
| `\d` | 日付 |
| `\n` | 改行 |

---

## 2. Python 仮想環境とGitブランチを表示する設定

### .bashrc の設定

```bash
# Prevent virtualenv from modifying PS1
export VIRTUAL_ENV_DISABLE_PROMPT=1

# color
USER_COLOR="\[\033[1;37m\]"      # white
LOCATION_COLOR="\[\033[1;32m\]"  # green
GIT_BRANCH_COLOR="\[\033[0;33m\]" # orange
VENV_COLOR="\[\033[1;36m\]"      # cyan
NO_COLOR="\[\033[0m\]"           # No_Color

# git branch
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# virtual environment
show_virtual_env() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "($(basename $VIRTUAL_ENV)) "
    fi
}

# PS1
PS1="${VENV_COLOR}\$(show_virtual_env)${USER_COLOR}\u ${LOCATION_COLOR}\w${GIT_BRANCH_COLOR}\$(parse_git_branch) ${NO_COLOR}\$ "
```

### 表示例

```bash
(.venv) koishizu ~/projects/github-copilot-sdk (main) $
```

- `(.venv)` - 仮想環境名（シアン色）
- `koishizu` - ユーザー名（白色）
- `~/projects/github-copilot-sdk` - カレントディレクトリ（緑色）
- `(main)` - Git ブランチ（オレンジ色）

---

## 3. 重要なポイント

### VIRTUAL_ENV_DISABLE_PROMPT の役割

```bash
export VIRTUAL_ENV_DISABLE_PROMPT=1
```

この設定がないと、Python 仮想環境をアクティベートしたときに、`activate` スクリプトが独自の `PS1` を設定してしまい、カスタム設定が上書きされます。

**この環境変数を設定することで:**
- 仮想環境のアクティベートスクリプトが `PS1` を変更しない
- カスタムプロンプトが維持される
- Git ブランチと仮想環境名の両方が表示される

### 関数の実行タイミング

```bash
PS1="${VENV_COLOR}\$(show_virtual_env)..."
```

`\$(show_virtual_env)` のようにバックスラッシュでエスケープすることで、プロンプトが表示されるたびに関数が実行されます。エスケープしないと、`.bashrc` 読み込み時に一度だけ実行されます。

---

## 4. カスタマイズ例

### プロジェクト名を表示する

`.venv` という名前の場合、親ディレクトリ名（プロジェクト名）を表示:

```bash
show_virtual_env() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        local venv_name=$(basename "$VIRTUAL_ENV")
        if [[ "$venv_name" == ".venv" ]] || [[ "$venv_name" == "venv" ]]; then
            venv_name=$(basename $(dirname "$VIRTUAL_ENV"))
        fi
        echo "(${venv_name}) "
    fi
}
```

表示例:
```bash
(github-copilot-sdk) koishizu ~/projects/github-copilot-sdk (main) $
```

### 色のカスタマイズ

| コード | 色 |
|--------|-----|
| `\[\033[0;30m\]` | 黒 |
| `\[\033[0;31m\]` | 赤 |
| `\[\033[0;32m\]` | 緑 |
| `\[\033[0;33m\]` | 黄 |
| `\[\033[0;34m\]` | 青 |
| `\[\033[0;35m\]` | マゼンタ |
| `\[\033[0;36m\]` | シアン |
| `\[\033[0;37m\]` | 白 |
| `\[\033[1;XXm\]` | 太字（XX は色コード） |

---

## 5. トラブルシューティング

### 変更が反映されない

```bash
# .bashrc を再読み込み
source ~/.bashrc
```

### 仮想環境アクティベート後にブランチが消える

`VIRTUAL_ENV_DISABLE_PROMPT=1` が設定されているか確認:

```bash
echo $VIRTUAL_ENV_DISABLE_PROMPT
# 出力: 1
```

### 既存のターミナルで反映されない

仮想環境を一度無効化してから再読み込み:

```bash
deactivate
source ~/.bashrc
source .venv/bin/activate
```

または新しいターミナルを開く。

---

## 6. 適用方法

1. `.bashrc` に上記の設定を追加
2. ターミナルで再読み込み:
   ```bash
   source ~/.bashrc
   ```
3. 仮想環境をアクティベート:
   ```bash
   source .venv/bin/activate
   ```

---

## 参考リンク
- [Bash Prompt HOWTO](https://tldp.org/HOWTO/Bash-Prompt-HOWTO/)
- [ANSI Color Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-02-04 | 初版作成 |
