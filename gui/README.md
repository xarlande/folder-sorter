# 🎨 Folder Sorter GUI

Graphical User Interface for **FolderSorter**, built with Python 3.10+ and Tkinter.

---

[🇺🇦 Українська версія](README_UA.md) | [👉 Main Documentation](../README.md)

---

## 🛠️ Architecture & Package Structure

The GUI application follows a clean modular architecture located under the `foldersorter/` package:

- **`main.py`**: Lightweight launcher entry point script.
- **`build_installer.py`**: Automated script to bundle Python GUI and compiled Rust CLI into standalone release executables using PyInstaller.
- **`foldersorter/`**:
  - `config.py`: Rule loading/saving, default categories, TOML handler (`tomllib`/`tomli`), configuration directory resolution (`~/.foldersorter`).
  - `exceptions.py`: Custom domain exceptions (`FolderSorterError`, `SchedulerError`, etc.).
  - `scheduler.py`: Platform-specific OS background scheduler management (macOS `launchd`, Windows `schtasks`, Linux `cron`).
  - `runner.py`: CLI binary discovery, Cargo compilation helper, and background sorting execution runner.
  - `ui/`:
    - `app.py`: `FolderSorterApp` main window and notebook layout.
    - `components.py`: Reusable styled widgets (`CustomButton`, `ScrollableFrame`).
    - `sorter_tab.py`: Tab 1 — Folder pickers, target options, dry run toggle, and console logger.
    - `rules_tab.py`: Tab 2 — Category and file extension rule editor.
    - `scheduler_tab.py`: Tab 3 — Background schedule configuration interface.

---

## 🚀 Running the GUI

### Option 1: Using `uv` (Recommended)
```bash
uv run main.py
```

### Option 2: Using `python3`
```bash
python3 main.py
```

---

## 📦 Building Standalone Executables

To build standalone single-file executables (`.app` on macOS, `.exe` on Windows, binary on Linux):

```bash
python3 build_installer.py
```

Output archives will be generated in `gui/dist/`.
