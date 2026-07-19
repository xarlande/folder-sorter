# 🎨 Folder Sorter GUI

Graphical User Interface desktop application for **FolderSorter**, built with Python 3.10+ and Tkinter.

---

[🇺🇦 Українська версія](README_UA.md) | [👉 Main Documentation](../README.md)

---

## 🛠️ Architecture & Package Structure

The GUI application follows a clean, modular Python package structure located in `foldersorter/`:

- **`main.py`**: Lightweight launcher entry point.
- **`build_installer.py`**: Automated script bundling Python GUI and release Rust CLI binary into single executable distributions using PyInstaller.
- **`foldersorter/`**:
  - `config.py`: Persistent TOML rule loading and saving (`~/.foldersorter/cleaner_config.toml`), default rules, and fallback handlers (`tomllib`/`tomli`).
  - `exceptions.py`: Custom domain exception hierarchy (`FolderSorterError`, `SchedulerError`, etc.).
  - `scheduler.py`: Platform-specific OS background scheduling logic (macOS `launchd`, Windows `schtasks`, Linux `cron`).
  - `runner.py`: CLI binary location resolver, automated Cargo compilation helper, and background subprocess sorter execution.
  - `ui/`:
    - `app.py`: `FolderSorterApp` main window and notebook layout manager.
    - `components.py`: Reusable styled widgets (`CustomButton`, `ScrollableFrame`).
    - `sorter_tab.py`: Tab 1 — Directory pickers, target path toggle, dry run option, and live text console logger.
    - `rules_tab.py`: Tab 2 — Category and extension editor form.
    - `scheduler_tab.py`: Tab 3 — Background scheduler activation and interval configuration view.

---

## 🚀 Running the GUI

### Option 1: Using `uv` (Recommended)
```bash
uv run main.py
```

### Option 2: Using standard `python3`
```bash
python3 main.py
```

> 💡 *Note: The GUI application automatically compiles the Rust CLI binary using Cargo if a pre-compiled executable is not found on your system.*

---

## 📦 Building Standalone Executables

To build standalone single-file bundles or app bundles (`.app` on macOS, `.exe` on Windows, or standalone binaries on Linux):

```bash
python3 build_installer.py
```

Output release archives will be generated inside `gui/dist/`.

---

## 📄 License

[MIT](LICENSE)
