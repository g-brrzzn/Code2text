#!/usr/bin/env python3
import sys
import os
import platform
import subprocess
from pathlib import Path

EXTENSIONS = [
    '.c', '.cpp', '.cc', '.cxx', '.h', '.hh', '.hpp', '.hxx', '.ino',
    '.py', '.pyw', '.java', '.js', '.ts', '.tsx', '.jsx', '.rb',
    '.go', '.rs', '.swift', '.kt', '.kts', '.cs', '.php',
    '.html', '.htm', '.css', '.scss', '.sass', '.lua', '.sh',
    '.bat', '.ps1', '.sql', '.r', '.m', '.asm', '.s',
    '.xml', '.yml', '.yaml', '.toml', '.ini',
    '.md', '.shader', '.cginc', '.hlsl', '.json'
]
OUTPUT_FILE = 'code2text_output.txt'
MAX_FILE_SIZE = 1024 * 256

IGNORE_ITEMS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 'env', '.env',
    'virtualenv', '__pycache__', '.pytest_cache', 'build', 'dist',
    'target', '.DS_Store', '.metadata', '.gradle', '.settings',
    'Library', 'Temp', 'Logs', 'UserSettings', 'obj', 'Build', 'Builds',
    'MemoryCaptures', 'Recordings'
}

def read_file_with_fallback(file_path: Path):
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return f"File skipped: size ({file_path.stat().st_size} bytes) exceeds limit."
    except Exception:
        pass

    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be', 'cp1252', 'latin1']
    
    for enc in encodings:
        try:
            return file_path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
        except Exception as e:
            print(f"Error reading {file_path} with {enc}: {e}")
            continue

    try:
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Total failure reading {file_path}: {e}")
        return None

def generate_tree(dir_path: Path, script_file: Path, output_path: Path, prefix: str = ''):
    tree_lines = []
    try:
        items = list(dir_path.iterdir())
    except PermissionError:
        return []

    valid_items = []
    for item in items:
        if item.name in IGNORE_ITEMS or item.name.endswith('.meta'):
            continue
        if item.resolve() == script_file or item.resolve() == output_path:
            continue
        valid_items.append(item)
    
    valid_items.sort(key=lambda x: (x.is_file(), x.name.lower()))

    for i, path in enumerate(valid_items):
        is_last = (i == len(valid_items) - 1)
        connector = '└── ' if is_last else '├── '
        tree_lines.append(f"{prefix}{connector}{path.name}")

        if path.is_dir():
            new_prefix = prefix + ('    ' if is_last else '│   ')
            tree_lines.extend(generate_tree(path, script_file, output_path, new_prefix))
    return tree_lines

def find_files(current_dir: Path, script_file: Path, output_path: Path):
    files_list = []
    try:
        for item in current_dir.iterdir():
            if item.name in IGNORE_ITEMS or item.name.endswith('.meta'):
                continue
            if item.resolve() == script_file or item.resolve() == output_path:
                continue
            
            if item.is_dir():
                files_list.extend(find_files(item, script_file, output_path))
            elif item.is_file():
                if item.suffix.lower() in EXTENSIONS or item.name.lower() == 'requirements.txt':
                    files_list.append(item)
    except PermissionError:
        pass
    return files_list

def open_output_file(file_path: Path):
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(file_path.resolve())
        elif system == 'Darwin':
            subprocess.Popen(['open', file_path.resolve()])
        else:
            subprocess.Popen(['xdg-open', file_path.resolve()])
        print(f"Opening {OUTPUT_FILE} in default editor...")
    except Exception as e:
        print(f"Could not open the file automatically. Please open it manually: {file_path.resolve()}")
        print(f"Error: {e}")

def main():
    current_dir = Path('.').resolve()
    script_file = Path(__file__).resolve()
    output_path = (current_dir / OUTPUT_FILE).resolve()
    
    generate_tree_flag = '--tree' in sys.argv or '-t' in sys.argv

    try:
        files = find_files(current_dir, script_file, output_path)
        files.sort()
    except Exception as e:
        print(f"Error finding files: {e}")
        sys.exit(1)

    if not files:
        print(f"No relevant files found in {current_dir}. Exiting.")
        sys.exit(0)
        
    tree_structure = ""
    if generate_tree_flag:
        try:
            tree_lines = generate_tree(current_dir, script_file, output_path)
            tree_structure = "\n".join(tree_lines)
        except Exception as e:
            print(f"Error generating folder tree: {e}")
            tree_structure = "Error generating folder tree."

    try:
        with open(output_path, 'w', encoding='utf-8', errors='replace') as out:
            out.write(f"Project: {current_dir.name}\n")
            out.write("=" * 40 + "\n\n")
            
            if generate_tree_flag:
                out.write("Project Structure:\n")
                out.write("```\n")
                out.write(f"{current_dir.name}/\n")
                out.write(tree_structure)
                out.write("\n```\n\n")
                out.write("=" * 40 + "\n")

            out.write("File Contents:\n")
            out.write("=" * 40 + "\n\n")

            for file in files:
                content = read_file_with_fallback(file)
                if content is None:
                    continue
                
                try:
                    rel_path = file.resolve().relative_to(current_dir)
                except ValueError:
                    rel_path = file.resolve()
                
                out.write(f"--- File: {rel_path} ---\n\n")
                out.write(f"```{file.suffix.lstrip('.')} \n")
                out.write(content.strip())
                out.write("\n```\n\n")
        
        print_message = f"Generated {output_path.name} with {len(files)} files"
        if generate_tree_flag:
            print_message += " and folder structure"
        print(print_message + ".")
        
        open_output_file(output_path)

    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()