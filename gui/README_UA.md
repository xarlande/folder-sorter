# 🎨 Folder Sorter GUI

Графічний інтерфейс користувача для **FolderSorter**, побудований на Python 3.10+ та Tkinter.

---

[🇬🇧 English version](README.md) | [👉 Головна документація](../README_UA.md)

---

## 🛠️ Архітектура та структура пакету

GUI-застосунок використовує модульну структуру, розташовану в пакеті `foldersorter/`:

- **`main.py`**: Точка входу застосунку.
- **`build_installer.py`**: Скрипт автоматичної збірки Python GUI та скомпільованого Rust CLI у самостійні бінарники за допомогою PyInstaller.
- **`foldersorter/`**:
  - `config.py`: Збереження/завантаження правил, стандартні категорії, робота з TOML (`tomllib`/`tomli`), визначення папки `~/.foldersorter`.
  - `exceptions.py`: Кастомні доменні винятки (`FolderSorterError`, `SchedulerError` тощо).
  - `scheduler.py`: Управління системними планувальниками для macOS `launchd`, Windows `schtasks`, Linux `cron`.
  - `runner.py`: Пошук CLI-бінарника, компіляція Cargo та фоновий запуск сортувальника.
  - `ui/`:
    - `app.py`: Головне вікно `FolderSorterApp` та макет вкладок.
    - `components.py`: Перевикористовувані віджети (`CustomButton`, `ScrollableFrame`).
    - `sorter_tab.py`: Вкладка 1 — Вибір папок, режим Dry Run та консоль логів.
    - `rules_tab.py`: Вкладка 2 — Редагування категорій та розширень.
    - `scheduler_tab.py`: Вкладка 3 — Налаштування фонового розкладу.

---

## 🚀 Запуск GUI

### Варіант 1: За допомогою `uv` (Рекомендовано)
```bash
uv run main.py
```

### Варіант 2: За допомогою `python3`
```bash
python3 main.py
```

---

## 📦 Збірка автономних інсталяторів

Для створення готових бінарних пакетиків (`.app` на macOS, `.exe` на Windows, виконуваний файл на Linux):

```bash
python3 build_installer.py
```

Готові архіви будуть збережені в папці `gui/dist/`.
