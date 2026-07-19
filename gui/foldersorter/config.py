"""Configuration management module for FolderSorter."""

import os
from dataclasses import dataclass
from pathlib import Path
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        tomllib = None  # type: ignore[assignment]

from foldersorter.exceptions import ConfigurationError


@dataclass(frozen=True)
class IntervalSpec:
    """Specifies interval timing parameters for different platform schedulers."""

    macos_seconds: int
    windows_minutes: int
    linux_cron: str


# Default fallback rules matching the CLI's default config
DEFAULT_RULES: dict[str, list[str]] = {
    "Зображення": ["jpg", "png", "jpeg", "gif", "svg"],
    "Відео": ["mp4", "mkv", "mov", "avi"],
    "Музика": ["mp3", "wav", "flac"],
    "Документи": ["pdf", "doc", "docx", "txt"],
    "Архіви": ["zip", "rar", "7z", "tar"],
    "Програми": ["exe", "msi", "deb"],
}

# Configuration intervals for schedulers
INTERVALS: dict[str, IntervalSpec] = {
    "Кожні 15 хвилин": IntervalSpec(
        macos_seconds=900,
        windows_minutes=15,
        linux_cron="*/15 * * * *",
    ),
    "Кожні 30 хвилин": IntervalSpec(
        macos_seconds=1800,
        windows_minutes=30,
        linux_cron="*/30 * * * *",
    ),
    "Кожну годину": IntervalSpec(
        macos_seconds=3600,
        windows_minutes=60,
        linux_cron="0 * * * *",
    ),
    "Кожні 12 годин": IntervalSpec(
        macos_seconds=43200,
        windows_minutes=720,
        linux_cron="0 */12 * * *",
    ),
    "Щодня (о 12:00)": IntervalSpec(
        macos_seconds=86400,
        windows_minutes=1440,
        linux_cron="0 12 * * *",
    ),
}


def get_config_dir() -> Path:
    """Gets the global configuration directory for the user (~/.foldersorter)."""
    config_dir = Path.home() / ".foldersorter"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_rules(config_path: Path | str) -> dict[str, list[str]]:
    """Loads configuration rules from TOML config file.

    Falls back to default rules if file is missing or unreadable.
    """
    path = Path(config_path)
    if tomllib is not None and path.exists() and path.is_file():
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
                rules = data.get("rules", {})
                if isinstance(rules, dict):
                    parsed_rules: dict[str, list[str]] = {}
                    for cat, exts in rules.items():
                        if isinstance(exts, list):
                            parsed_rules[str(cat)] = [str(x) for x in exts]
                    return parsed_rules
        except (tomllib.TOMLDecodeError, OSError) as e:
            print(f"Помилка при зчитуванні TOML ({path}): {e}")

    return {cat: list(exts) for cat, exts in DEFAULT_RULES.items()}


def save_rules(config_path: Path | str, rules: dict[str, list[str]]) -> bool:
    """Saves rules to TOML config file in the correct format."""
    path = Path(config_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("[rules]\n")
            for cat, exts in rules.items():
                ext_list_str = ", ".join(
                    f'"{x.strip().lower()}"' for x in exts if x.strip()
                )
                f.write(f'"{cat}" = [{ext_list_str}]\n')
        return True
    except OSError as e:
        print(f"Помилка при збереженні TOML ({path}): {e}")
        return False
