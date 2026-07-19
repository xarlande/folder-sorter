# ⚡ Folder Sorter CLI

High-performance command-line file organization utility written in Rust.

---

[🇺🇦 Українська версія](README_UA.md) | [👉 Main Documentation](../README.md)

---

## ✨ Features

- **Blazing Fast**: Compiled Rust binary designed for maximum I/O performance.
- **Automatic Sorting**: Moves files into category subdirectories based on their file extensions.
- **Configurable TOML Rules**: Easily customize categories and extension lists.
- **Collision Indexing**: Automatically appends numbers `filename_1.ext` if a destination file already exists.
- **Dry Run Mode**: Safely test and preview operations without altering files on disk.

---

## 🛠️ Build & Installation

Prerequisites: [Rust and Cargo](https://rustup.rs/).

```bash
# Build release binary locally
cargo build --release

# Install binary to ~/.cargo/bin
cargo install --path .
```

---

## 🚀 Usage

```bash
folder-sorter --path <DIRECTORY_PATH> [OPTIONS]
```

### Options

- `-p, --path <PATH>` — Target directory path to organize.
- `-o, --output <OUTPUT>` — *(Optional)* Destination directory. Defaults to source path.
- `-d, --dry-run` — Run in preview mode without moving files.
- `-V, --version` — Print version information.
- `-h, --help` — Display help information.

### Examples

```bash
# Preview proposed changes in Downloads directory
folder-sorter --path ~/Downloads --dry-run

# Organize files in Downloads directory
folder-sorter --path ~/Downloads

# Specify a custom target destination directory
folder-sorter --path ~/Downloads --output ~/Organized

# Run using Cargo during development
cargo run --release -- --path . --dry-run
```

---

## ⚙️ Configuration

On execution, the tool reads `cleaner_config.toml` from the current working directory. If missing, it creates a default configuration file.

Default rules:
```toml
[rules]
"Зображення" = ["jpg", "png", "jpeg", "gif", "svg"]
"Відео" = ["mp4", "mkv", "mov", "avi"]
"Музика" = ["mp3", "wav", "flac"]
"Документи" = ["pdf", "doc", "docx", "txt"]
"Архіви" = ["zip", "rar", "7z", "tar"]
"Програми" = ["exe", "msi", "deb"]
```

Unrecognized extensions are automatically moved to an `"Інше"` (Other) folder.

---

## 📄 License

[MIT](LICENSE)
