# 📁 Folder Sorter

**Folder Sorter** is a modern cross-platform software suite for automatically organizing files into category subdirectories based on their file extensions. The project combines a high-performance **Rust CLI core engine** with a modern, high-performance **Tauri GUI** (Rust + Vue 3) supporting background automated task scheduling.

---

[🇺🇦 Українська версія](README_UA.md)

---

## ✨ Features

- ⚡ **High Performance (Rust Core)**: Ultra-fast file scanning and relocation with automatic index suffixing for duplicate filename collisions.
- 🎨 **Modern Graphical Interface (Tauri GUI)**: Elegant dark theme powered by Vue 3 and Tailwind CSS featuring dedicated tabs for folder sorting, rules management, and automated background scheduling.
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
├── tauri-gui/                  # Modern Tauri desktop GUI application
│   ├── package.json            # Node.js dependencies & scripts
│   ├── vite.config.js          # Vite build configuration
│   ├── src/                    # Frontend Vue 3 application
│   │   ├── App.vue             # Main App component
│   │   └── components/         # Tab views & UI components
│   └── src-tauri/              # Rust desktop backend for Tauri
│       ├── Cargo.toml          # Tauri Rust package manifest
│       └── src/
│           └── lib.rs          # Tauri command handlers & scheduler integration
├── README.md                   # Root English documentation
└── README_UA.md                # Root Ukrainian documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Rust / Cargo**: Required to build the CLI core engine and Tauri GUI ([Install Rust](https://rustup.rs/)).
- **Node.js 18+**: Required to run and build the Tauri frontend.

### 2. Running the Desktop GUI App

```bash
cd tauri-gui
pnpm install
pnpm tauri dev
```

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

## 📦 Building Desktop Releases

To compile and package native executable installers (`.dmg`/`.app` on macOS, `.msi`/`.exe` on Windows, `.deb`/`.AppImage` on Linux):

```bash
cd tauri-gui
pnpm tauri build
```

The compiled bundles will be generated in `tauri-gui/src-tauri/target/release/bundle/`.

---

## 📄 License

[MIT](LICENSE)
