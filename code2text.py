#!/usr/bin/env python3
import sys
from pathlib import Path

extensions = [
    '.c',        # C
    '.cpp',      # C++
    '.cc',       # C++
    '.cxx',      # C++
    '.h',        # Header (C/C++)
    '.hh',       # Header (C++)
    '.hpp',      # Header (C++)
    '.hxx',      # Header (C++)
    '.ino',      # Arduino
    '.py',       # Python
    '.pyw',      # Python (Windows GUI)
    '.java',     # Java
    '.js',       # JavaScript
    '.ts',       # TypeScript
    '.tsx',      # TypeScript with JSX
    '.jsx',      # JavaScript with JSX
    '.rb',       # Ruby
    '.go',       # Go
    '.rs',       # Rust
    '.swift',    # Swift
    '.kt',       # Kotlin
    '.kts',      # Kotlin Script
    '.cs',       # C#
    '.php',      # PHP
    '.html',     # HTML
    '.htm',      # HTML
    '.css',      # CSS
    '.scss',     # SASS
    '.sass',     # SASS
    '.lua',      # Lua
    '.sh',       # Shell Script
    '.bat',      # Batch
    '.ps1',      # PowerShell
    '.sql',      # SQL
    '.r',        # R
    '.m',        # MATLAB / Objective-C
    '.asm',      # Assembly
    '.s',        # Assembly
    '.json',     # JSON
    '.xml',      # XML
    '.yml',      # YAML
    '.yaml',     # YAML
    '.toml',     # TOML
    '.ini',      
]
output_file = 'output.txt'

def read_file_with_fallback(file_path):
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding='latin1')
        except Exception as e:
            print(f"Failed to read {file_path.name}: {e}")
            return None

def main():
    current_dir = Path('.')
    files = [f for f in current_dir.iterdir() if f.is_file() and f.suffix in extensions]

    if not files:
        print(f"No files with extensions {extensions} found in {current_dir.resolve()}. Exiting.")
        sys.exit(0)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('Code:\n\n')
        for file in files:
            content = read_file_with_fallback(file)
            if content is None:
                continue
            out.write(f"{file.name}:\n")
            out.write(content)
            out.write('\n\n')

    print(f"Generated {output_file} with {len(files)} files.")

if __name__ == '__main__':
    main()
