# Folder Sorter

A simple Rust utility for automatically sorting files into categories (Images, Videos, Documents, etc.) based on their extensions.

---

[🇺🇦 Українська версія](README_UA.md)

## Features

- **Automatic Sorting**: Organizes files into subfolders based on their extensions.
- **Flexible Configuration**: Customize categories and extensions via a TOML file.
- **Dry Run Mode**: Preview planned changes without actually moving files.
- **Duplicate Handling**: Automatically adds an index to the filename if a file with the same name already exists in the destination folder.

## Installation

You need [Rust](https://www.rust-lang.org/) installed to build the project.

```bash
# Clone the repository and run:
cargo install --path .
```

Ensure `~/.cargo/bin` is added to your `PATH` environment variable.

## Usage

```bash
folder-sorter --path <DIRECTORY_PATH> [OPTIONS]
```

### Parameters

- `-p, --path <PATH>` — Path to the directory you want to organize.
- `-o, --output <OUTPUT>` — (Optional) Path to the directory where sorted files will be moved. Defaults to the source path.
- `-d, --dry-run` — Run in preview mode (files will not be moved).
- `-V, --version` — Show program version.
- `-h, --help` — Show help message.

### Examples

```bash
# Check what will be done in the Downloads folder
folder-sorter --path ~/Downloads --dry-run

# Organize files in the Downloads folder
folder-sorter --path ~/Downloads

# Using cargo run (development)
cargo run -- --path . --dry-run
```

## Configuration

On the first run, the program creates a `cleaner_config.toml` file in the current directory. You can edit it to add your own categories or extensions.

Default categories:

- **Images**: jpg, png, jpeg, gif, svg
- **Video**: mp4, mkv, mov, avi
- **Music**: mp3, wav, flac
- **Documents**: pdf, doc, docx, txt
- **Archives**: zip, rar, 7z, tar
- **Apps**: exe, msi, deb
- **Other**: All other file types

Example `cleaner_config.toml`:

```toml
[rules]
"Images" = ["jpg", "png", "jpeg", "gif", "svg"]
"Documents" = ["pdf", "doc", "docx", "txt"]
"Projects" = ["rs", "py", "js", "cpp"]
```

## License

MIT
