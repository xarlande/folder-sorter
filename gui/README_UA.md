# 🎨 Folder Sorter GUI

Графічний десктопний застосунок для **FolderSorter**, побудований на Python 3.10+ та Tkinter.

---

[🇬🇧 English version](README.md) | [👉 Головна документація](../README_UA.md)

---

## 🛠️ Архітектура та структура пакету

GUI-застосунок використовує чисту модульну структуру в пакеті `foldersorter/`:

- **`main.py`**: Легка точка входу для запуску застосунку.
- **`build_installer.py`**: Автоматизований скрипт упаковки Python GUI та вихідного Rust CLI у самостійні дистрибутиви через PyInstaller.
- **`foldersorter/`**:
  - `config.py`: Завантаження та збереження TOML правил (`~/.foldersorter/cleaner_config.toml`), дефолтні категорії та сумісність з `tomllib`/`tomli`.
  - `exceptions.py`: Ієрархія доменних винятки (`FolderSorterError`, `SchedulerError` тощо).
  - `scheduler.py`: Управління фоновими планивальниками ОС (macOS `launchd`, Windows `schtasks`, Linux `cron`).
  - `runner.py`: Пошук CLI-бінарника, автокомпіляція через Cargo та запуск сортування у фонових процессах.
  - `ui/`:
    - `app.py`: Головне вікно `FolderSorterApp` та макет вкладок.
    - `components.py`: Перевикористовувані віджети (`CustomButton`, `ScrollableFrame`).
    - `sorter_tab.py`: Вкладка 1 — Вибір папок, опції сортування, режим Dry Run та інтерактивна лог-консоль.
    - `rules_tab.py`: Вкладка 2 — Редагування категорій та розширень файлів.
    - `scheduler_tab.py`: Вкладка 3 — Управління системним планувальником та інтервалами.

---

## 🚀 Запуск GUI

### Варіант 1: За допомогою `uv` (Рекомендовано)
```bash
uv run main.py
```

### Варіант 2: За допомогою стандартного `python3`
```bash
python3 main.py
```

> 💡 *Примітка: Застосунок GUI автоматично скомпілює Rust CLI у фоні за допомогою Cargo, якщо готовий бінарник відсутній на вашому ПК.*

---

## 📦 Збірка автономних інсталяторів

Для створення готових бінарних пакетиків (`.app` на macOS, `.exe` на Windows, виконуваний файл на Linux):

```bash
python3 build_installer.py
```

Готові архіви будуть збережені у папці `gui/dist/`.

---

## 📄 Ліцензія

[MIT](LICENSE)
