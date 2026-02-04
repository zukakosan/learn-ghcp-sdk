# GitHub Copilot SDK - ツール定義ガイド

## 概要
GitHub Copilot SDK の `define_tool` デコレータを使用すると、LLM が呼び出せるカスタムツールを定義できます。ツールのパラメータは、LLM がユーザーのプロンプトから自動的に推測・設定します。

---

## 1. 基本的なツールの定義

### ツールの作成方法

```python
from copilot import define_tool

@define_tool(description="Get files in a local directory")
async def list_local_files(directory: str = ".") -> str:
    """
    List all files in the specified directory.
    
    Args:
        directory: The directory path to list files from. 
                   Can be absolute path (e.g., /home/user/documents) 
                   or relative path (e.g., ../parent_dir)
                   Default is current directory.
    
    Returns:
        A newline-separated list of file names
    """
    try:
        expanded_path = os.path.expanduser(directory)
        files = os.listdir(expanded_path)
        return f"Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing files in {directory}: {str(e)}"
```

### セッションへの登録

```python
session = await client.create_session({
    "model": "gpt-4.1",
    "streaming": True,
    "tools": [list_local_files]  # ツールのリストを渡す
})
```

---

## 2. パラメータの自動判断

### LLM による自動解釈

定義したツールのパラメータは、**LLM が自動的に判断して値を設定**します:

1. **ツールの説明とパラメータ情報を LLM に渡す**
   - `description` とパラメータの型ヒント、docstring が LLM に提供される
   
2. **LLM がユーザーのプロンプトを解釈**
   - ユーザーの質問内容から、どのツールを使うべきか判断
   - 必要なパラメータの値を推測・抽出

3. **ツールを実行**
   - LLM が決定したパラメータ値でツールが呼び出される

### 実行例

```python
# ユーザープロンプト: "このディレクトリのファイルを教えてください"
# → LLM は directory="." を設定

# ユーザープロンプト: "~/projects 内のファイルを教えて"
# → LLM は directory="/home/koishizu/projects" を設定

# ユーザープロンプト: "/home/koishizu/Documents のファイルを教えてください"
# → LLM は directory="/home/koishizu/Documents" を設定
```

---

## 3. ベストプラクティス

### デフォルト値の設定

```python
async def list_local_files(directory: str = ".") -> str:
    """デフォルト値を設定すると、LLM がパラメータを省略しやすくなる"""
    pass
```

### 詳細な Docstring

```python
@define_tool(description="Search for files in a directory by name pattern")
async def search_files(directory: str, pattern: str) -> str:
    """
    Search for files matching a pattern in the specified directory.
    
    Args:
        directory: The directory path to search in
        pattern: File name pattern (e.g., "*.py", "test_*")
    
    Returns:
        A formatted string with matching file paths
    """
    # 詳細な説明を書くと、LLM がより正確にパラメータを推測できる
```

### エラーハンドリング

```python
@define_tool(description="Read the contents of a text file")
async def read_file(filepath: str, max_lines: int = 100) -> str:
    """
    Read and return the contents of a text file.
    
    Args:
        filepath: Path to the file to read
        max_lines: Maximum number of lines to read (default: 100)
    
    Returns:
        The file contents or an error message
    """
    try:
        full_path = os.path.expanduser(filepath)
        
        if not os.path.exists(full_path):
            return f"File not found: {filepath}"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            content = ''.join(lines)
            
        return f"Contents of {filepath}:\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

---

## 4. 推奨ツール例

### ファイル検索ツール

```python
import glob

@define_tool(description="Search for files in a directory by name pattern")
async def search_files(directory: str, pattern: str) -> str:
    try:
        search_path = os.path.join(os.path.expanduser(directory), pattern)
        files = glob.glob(search_path, recursive=True)
        
        if not files:
            return f"No files found matching '{pattern}' in {directory}"
        
        result = f"Found {len(files)} file(s):\n"
        for f in files:
            size = os.path.getsize(f)
            result += f"- {f} ({size} bytes)\n"
        
        return result
    except Exception as e:
        return f"Error searching files: {str(e)}"
```

### ディレクトリ統計ツール

```python
@define_tool(description="Get statistics about files in a directory")
async def get_directory_stats(directory: str) -> str:
    try:
        dir_path = os.path.expanduser(directory)
        
        if not os.path.isdir(dir_path):
            return f"Directory not found: {directory}"
        
        file_count = 0
        total_size = 0
        extensions = {}
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_count += 1
                filepath = os.path.join(root, file)
                total_size += os.path.getsize(filepath)
                
                ext = os.path.splitext(file)[1] or "no extension"
                extensions[ext] = extensions.get(ext, 0) + 1
        
        result = f"Directory: {directory}\n"
        result += f"Total files: {file_count}\n"
        result += f"Total size: {total_size / 1024:.2f} KB\n"
        result += "\nFile types:\n"
        
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            result += f"  {ext}: {count} files\n"
        
        return result
    except Exception as e:
        return f"Error analyzing directory: {str(e)}"
```

---

## 5. セキュリティ上の注意

- **書き込み操作は慎重に実装**する
- ファイルパスのバリデーションを行う
- 重要なシステムディレクトリへのアクセスを制限する
- エラーメッセージで機密情報を漏らさない

---

## 参考リンク
- [GitHub Copilot SDK Python](https://github.com/github/copilot-sdk/tree/main/python)

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-02-04 | 初版作成 |
