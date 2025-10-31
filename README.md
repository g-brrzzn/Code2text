# code2text

**code2text** is a lightweight Python utility that extracts the contents of source files in a project directory and compiles them into a single text file.  
It supports many common programming languages and optionally includes a visual folder tree for better project context.

---

## 📋 Features

- Recursively scans project directories
- Collects code from a wide variety of file types (`.cpp`, `.py`, `.js`, `.html`, `.css`, etc.)
- Generates a single `code2text_output.txt` file containing:
  - File paths
  - Formatted code blocks
  - (Optional) project structure tree
- Automatically skips irrelevant or temporary folders (e.g., `node_modules`, `.git`, `__pycache__`, etc.)
- Opens the generated output file in your system’s default text editor

---

## 🧩 Supported File Types

Includes common extensions for:
- **Programming languages:** C/C++, Python, Java, Go, Rust, Swift, Kotlin, C#, PHP, Ruby, Lua, etc.
- **Web files:** HTML, CSS, JS, TS, JSX, TSX, SCSS, etc.
- **Config/markup:** YAML, JSON, XML, INI, TOML, Markdown, SQL, and more.

---

## 🚀 Usage

python3 code2text.py [options]

Options
--tree or -t
Include a visual representation of the project folder structure at the top of the output.

---

## ⚙️ Requirements

- Python **3.6+**
- Works on **Windows**, **macOS**, and **Linux**

No external dependencies are required.

---

## 💡 Notes

- The tool automatically ignores temporary and environment directories to keep output clean.  
- Binary or unreadable files are safely skipped.
