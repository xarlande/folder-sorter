# 📁 Folder Sorter

**Folder Sorter** is a modern cross-platform software suite for automatically organizing files into category subdirectories based on their file extensions. The project combines a high-performance **Rust CLI core engine** with a feature-rich, user-friendly **Python (Tkinter) GUI** supporting background automated task scheduling.

---

[🇺🇦 Українська версія](README_UA.md)

---

## ✨ Features

- ⚡ **High Performance (Rust Core)**: Ultra-fast file scanning and relocation with automatic index suffixing for duplicate filename collisions.
- 🎨 **Modern Graphical Interface (Python GUI)**: Elegant dark theme featuring dedicated tabs for folder sorting, rules management, and automated background scheduling.
- ⏰ **Native OS Scheduling**: Built-in setup for system background tasks:
  - **macOS**: `launchd` (LaunchAgents)
  - **Windows**: Task Scheduler (`schtasks`)
  - **Linux**: `cron` (`crontab`)
- 🔍 **Dry Run Mode**: Safe preview mode showing all proposed filesystem modifications before applying them.
- ⚙️ **Flexible TOML Rules**: Easily customize categories and file extension associations stored in `~/.foldersorter/cleaner_config.toml`.

---

## 📂 Repository Structure

```text
folder-sorter/
├── cli/                        # High-performance Rust CLI engine
│   ├── Cargo.toml              # Rust package manifest
│   ├── README.md               # CLI English documentation
│   ├── README_UA.md            # CLI Ukrainian documentation
│   └── src/
│       ├── main.rs             # CLI binary entry point (Clap CLI parser)
│       ├── lib.rs              # Crate root & module exports
│       ├── file_organizer.rs   # Scanner & file organizer engine
│       ├── config.rs           # TOML config manager & default rules
│       └── error.rs            # Custom error types
├── gui/                        # Modular Python GUI application
│   ├── main.py                 # Application launcher entry point
│   ├── build_installer.py      # Standalone binary packager (PyInstaller)
│   ├── README.md               # GUI English documentation
│   ├── README_UA.md            # GUI Ukrainian documentation
│   ├── pyproject.toml / uv.lock # Python environment lockfiles
│   └── foldersorter/           # Modular Python package
│       ├── config.py           # Configuration manager & default fallbacks
│       ├── exceptions.py       # Domain-specific custom exceptions
│       ├── scheduler.py        # OS background scheduler integration
│       ├── runner.py           # Cargo builder & CLI execution runner
│       └── ui/                 # Tkinter views & custom widgets
│           ├── app.py          # FolderSorterApp main window
│           ├── components.py   # Reusable flat widgets (CustomButton, ScrollableFrame)
│           ├── sorter_tab.py   # Sorting tab & live console logger
│           ├── rules_tab.py    # Category & extension editor tab
│           └── scheduler_tab.py # Background task scheduler tab
├── README.md                   # Root English documentation
└── README_UA.md                # Root Ukrainian documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Rust / Cargo**: Required to build the CLI core engine ([Install Rust](https://rustup.rs/)).
- **Python 3.10+** (or [uv](https://docs.astral.sh/uv/)): Required to run the GUI desktop app.

### 2. Running the Desktop GUI App

Using `uv`:
```bash
cd gui
uv run main.py
```

Using standard `python3`:
```bash
cd gui
python3 main.py
```

> 💡 *Note: The GUI automatically detects and compiles the Rust CLI binary in release mode if a compiled executable is not found.*

### 3. Running the CLI directly (Rust)

```bash
cd cli

# Run preview mode (Dry Run)
cargo run --release -- --path ~/Downloads --dry-run

# Organize files in specified directory
cargo run --release -- --path ~/Downloads
```

---

## ⚙️ Configuration Guide

Configuration options are stored in `~/.foldersorter/cleaner_config.toml`.

Example `cleaner_config.toml`:

```toml
[rules]
"Зображення" = ["jpg", "png", "jpeg", "gif", "svg"]
"Відео" = ["mp4", "mkv", "mov", "avi"]
"Музика" = ["mp3", "wav", "flac"]
"Документи" = ["pdf", "doc", "docx", "txt"]
"Архіви" = ["zip", "rar", "7z", "tar"]
"Програми" = ["exe", "msi", "deb"]
```

Rule categories and extension mappings can be edited directly in the file or managed graphically via the **"Rules Settings"** tab in the GUI app.

---

## 📦 Standalone Installer Bundling

To generate single-file executables (`.app` on macOS, `.exe` on Windows, or standalone binaries on Linux):

```bash
cd gui
python3 build_installer.py
```

This automated script will:
1. Compile the Rust CLI core engine in `--release` mode.
2. Bundle the Python GUI and CLI binary into a self-contained distribution using PyInstaller.
3. Package ready-to-use compressed archives under `gui/dist/`.

---

## 📄 License

[MIT](LICENSE)
