#!/usr/bin/env python3
import sys
from pathlib import Path

extensions = [
    '.c', '.cpp', '.cc', '.cxx', '.h', '.hh', '.hpp', '.hxx', '.ino',
    '.py', '.pyw', '.java', '.js', '.ts', '.tsx', '.jsx', '.rb',
    '.go', '.rs', '.swift', '.kt', '.kts', '.cs', '.php',
    '.html', '.htm', '.css', '.scss', '.sass', '.lua', '.sh',
    '.bat', '.ps1', '.sql', '.r', '.m', '.asm', '.s',
    '.json', '.xml', '.yml', '.yaml', '.toml', '.ini',
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
    script_file = Path(__file__).resolve()
    files = [
        f for f in current_dir.iterdir()
        if f.is_file()
        and f.suffix in extensions
        and f.resolve() != script_file
    ]

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
