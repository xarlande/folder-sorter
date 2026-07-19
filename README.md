# 📁 Folder Sorter

**Folder Sorter** is a modern cross-platform utility for automatically organizing files into category subdirectories based on their file extensions. The project combines a high-performance **Rust CLI core engine** with a feature-rich, user-friendly **Python (Tkinter) GUI** supporting background automated task scheduling.

---

## ✨ Features

- ⚡ **High Performance (Rust Engine)**: Blazing-fast directory scanning and file organization with automatic filename collision indexing.
- 🎨 **Modern Graphical Interface (Python/Tkinter)**: Elegant dark theme UI featuring dedicated tabs for folder sorting, rules management, and system scheduling.
- ⏰ **Automated System Scheduling**: Native integration with OS background schedulers:
  - **macOS**: `launchd` (LaunchAgents)
  - **Windows**: Task Scheduler (`schtasks`)
  - **Linux**: `cron` (`crontab`)
- 🔍 **Dry Run Mode**: Safely preview file relocations before making actual filesystem changes.
- ⚙️ **Flexible TOML Configuration**: User-customizable rules stored globally in `~/.foldersorter/cleaner_config.toml`.

---

## 📂 Repository Structure

```text
folder-sorter/
├── cli/                        # High-performance Rust CLI engine
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs             # CLI entry point
│       ├── lib.rs              # File scanner and mover logic
│       └── config.rs           # TOML configuration parser
├── gui/                        # Modular Python GUI application
│   ├── main.py                 # Application launcher entry point
│   ├── build_installer.py      # Standalone binary builder (PyInstaller)
│   ├── pyproject.toml / uv.lock
│   └── foldersorter/           # Modular Python package
│       ├── config.py           # Config loader and rule persistence
│       ├── exceptions.py       # Domain-specific error types
│       ├── scheduler.py        # OS background scheduler integration
│       ├── runner.py           # CLI binary discovery and Cargo builder
│       └── ui/                 # Tkinter view modules
│           ├── app.py          # FolderSorterApp main window
│           ├── components.py   # Reusable flat widgets (CustomButton, ScrollableFrame)
│           ├── sorter_tab.py   # Sorting tab & live output console
│           ├── rules_tab.py    # Category & extension editor tab
│           └── scheduler_tab.py # Background task scheduler tab
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Rust / Cargo**: Required to build the CLI engine ([Install Rust](https://rustup.rs/)).
- **Python 3.10+** (or [uv](https://docs.astral.sh/uv/)): Required to run the GUI.

### 2. Running the GUI (Python)

Using `uv`:
```bash
cd gui
uv run main.py
```

Using system `python3`:
```bash
cd gui
python3 main.py
```

> 💡 *Note: On first run, the GUI automatically builds the Rust CLI binary in the background if a compiled executable is not yet present.*

### 3. Running the CLI directly (Rust)

```bash
cd cli

# Dry Run (preview mode)
cargo run --release -- --path ~/Downloads --dry-run

# Organize files in specified path
cargo run --release -- --path ~/Downloads
```

---

## ⚙️ Configuration Guide

Configuration options are stored in `~/.foldersorter/cleaner_config.toml`.

Example `cleaner_config.toml`:

```toml
[rules]
"Images" = ["jpg", "png", "jpeg", "gif", "svg"]
"Videos" = ["mp4", "mkv", "mov", "avi"]
"Audio" = ["mp3", "wav", "flac"]
"Documents" = ["pdf", "doc", "docx", "txt"]
"Archives" = ["zip", "rar", "7z", "tar"]
"Executables" = ["exe", "msi", "deb"]
```

Categories and file extensions can be modified either directly in the TOML file or via the **"Rules Settings"** tab in the GUI.

---

## 📦 Building Standalone Installers (PyInstaller)

To build standalone, single-file bundles or executable app packages (`.app` for macOS, `.exe` for Windows, executable for Linux):

```bash
cd gui
python3 build_installer.py
```

The script automatically:
1. Compiles the Rust CLI engine in `--release` mode.
2. Packages the Python GUI alongside the compiled CLI binary via PyInstaller.
3. Generates release archives inside `gui/dist/`.

---

## 📄 License

[MIT](LICENSE)
