"""Platform-specific scheduler management module (macOS launchd, Windows schtasks, Linux cron)."""

import os
import platform
import subprocess
from pathlib import Path

from foldersorter.config import get_config_dir


def get_system_scheduler_name(system: str | None = None) -> str:
    """Returns the human-readable system scheduler name."""
    sys_name = system or platform.system()
    if sys_name == "Darwin":
        return "launchd (macOS LaunchAgents)"
    elif sys_name == "Windows":
        return "Task Scheduler (Windows schtasks)"
    else:
        return "cron (Linux crontab)"


def is_scheduler_active(system: str | None = None) -> bool:
    """Checks whether background scheduling task is active on current platform."""
    sys_name = system or platform.system()

    if sys_name == "Darwin":
        plist_path = Path.home() / "Library" / "LaunchAgents" / "com.user.foldersorter.plist"
        if not plist_path.exists():
            return False
        try:
            res = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
            return "com.user.foldersorter" in res.stdout
        except OSError:
            return False

    elif sys_name == "Windows":
        try:
            res = subprocess.run(
                ["schtasks", "/query", "/tn", "FolderSorterTask"],
                capture_output=True,
                text=True,
            )
            return res.returncode == 0
        except OSError:
            return False

    else:  # Linux / Unix
        try:
            res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            if res.returncode != 0:
                return False
            return "# FOLDER-SORTER-TASK" in res.stdout
        except OSError:
            return False


def enable_schedule(
    bin_path: str | Path,
    src_path: str | Path,
    dest_path: str | Path | None,
    dry_run: bool,
    interval_data: dict[str, int | str] | None = None,
    macos_seconds: int = 3600,
    windows_minutes: int = 60,
    linux_cron: str = "0 * * * *",
    system: str | None = None,
) -> tuple[bool, str]:
    """Enables automatic folder sorting on current platform using specified interval settings."""
    sys_name = system or platform.system()
    bin_str = str(bin_path)
    src_str = str(src_path)
    dest_str = str(dest_path) if dest_path else ""

    if sys_name == "Darwin":
        return setup_launchd(bin_str, src_str, dest_str, dry_run, macos_seconds)
    elif sys_name == "Windows":
        return setup_schtasks(bin_str, src_str, dest_str, dry_run, windows_minutes)
    else:
        return setup_cron(bin_str, src_str, dest_str, dry_run, linux_cron)


def disable_schedule(system: str | None = None) -> tuple[bool, str]:
    """Disables automatic folder sorting on current platform."""
    sys_name = system or platform.system()
    if sys_name == "Darwin":
        return remove_launchd()
    elif sys_name == "Windows":
        return remove_schtasks()
    else:
        return remove_cron()


# --- macOS launchd Implementation ---

def setup_launchd(
    bin_path: str, src_path: str, dest_path: str, dry_run: bool, seconds: int
) -> tuple[bool, str]:
    """Sets up macOS LaunchAgent plist file."""
    plist_path = Path.home() / "Library" / "LaunchAgents" / "com.user.foldersorter.plist"
    plist_path.parent.mkdir(parents=True, exist_ok=True)

    args = [bin_path, "-p", src_path]
    if dest_path:
        args.extend(["-o", dest_path])
    if dry_run:
        args.append("-d")

    args_xml = "".join(f"        <string>{arg}</string>\n" for arg in args)
    config_dir = get_config_dir()

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.foldersorter</string>
    <key>ProgramArguments</key>
    <array>
{args_xml}    </array>
    <key>StartInterval</key>
    <integer>{seconds}</integer>
    <key>WorkingDirectory</key>
    <string>{config_dir}</string>
    <key>StandardOutPath</key>
    <string>/tmp/foldersorter.out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/foldersorter.err.log</string>
</dict>
</plist>
"""
    try:
        with open(plist_path, "w", encoding="utf-8") as f:
            f.write(plist_content)

        subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
        res = subprocess.run(
            ["launchctl", "load", str(plist_path)], capture_output=True, text=True
        )

        if res.returncode == 0:
            return True, "Агент завантажено в launchd."
        else:
            return False, f"Помилка launchctl: {res.stderr.strip()}"
    except Exception as e:
        return False, f"Помилка створення файлу: {e}"


def remove_launchd() -> tuple[bool, str]:
    """Removes macOS LaunchAgent plist file and unloads service."""
    plist_path = Path.home() / "Library" / "LaunchAgents" / "com.user.foldersorter.plist"
    if not plist_path.exists():
        return True, "Агент вже вимкнений (файл конфігурації відсутній)."

    subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
    try:
        plist_path.unlink(missing_ok=True)
    except OSError:
        pass
    return True, "Файл агента вивантажено та видалено."


# --- Windows Task Scheduler Implementation ---

def setup_schtasks(
    bin_path: str, src_path: str, dest_path: str, dry_run: bool, minutes: int
) -> tuple[bool, str]:
    """Creates Windows schtasks entry."""
    cmd_args = f'cmd.exe /c "cd /d \\"%USERPROFILE%\\.foldersorter\\" && \\"{bin_path}\\" -p \\"{src_path}\\"'
    if dest_path:
        cmd_args += f' -o \\"{dest_path}\\"'
    if dry_run:
        cmd_args += " -d"
    cmd_args += '"'

    if minutes == 1440:  # 1 Day
        cmd = [
            "schtasks",
            "/create",
            "/tn",
            "FolderSorterTask",
            "/tr",
            cmd_args,
            "/sc",
            "DAILY",
            "/st",
            "12:00",
            "/f",
        ]
    elif minutes == 720:  # 12 Hours
        cmd = [
            "schtasks",
            "/create",
            "/tn",
            "FolderSorterTask",
            "/tr",
            cmd_args,
            "/sc",
            "HOURLY",
            "/mo",
            "12",
            "/f",
        ]
    else:  # Minutes (15, 30, 60)
        cmd = [
            "schtasks",
            "/create",
            "/tn",
            "FolderSorterTask",
            "/tr",
            cmd_args,
            "/sc",
            "MINUTE",
            "/mo",
            str(minutes),
            "/f",
        ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return True, "Завдання створено в Task Scheduler."
        else:
            return False, f"schtasks помилка: {res.stderr.strip()}"
    except Exception as e:
        return False, f"Помилка створення завдання: {e}"


def remove_schtasks() -> tuple[bool, str]:
    """Deletes Windows schtasks entry."""
    cmd = ["schtasks", "/delete", "/tn", "FolderSorterTask", "/f"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return True, "Завдання видалено з Task Scheduler."
        else:
            err_msg = res.stderr.lower()
            if "не знайдено" in err_msg or "not found" in err_msg:
                return True, "Завдання вже було вилучено."
            return False, f"schtasks помилка: {res.stderr.strip()}"
    except Exception as e:
        return False, f"Помилка видалення завдання: {e}"


# --- Linux Crontab Implementation ---

def setup_cron(
    bin_path: str, src_path: str, dest_path: str, dry_run: bool, cron_expr: str
) -> tuple[bool, str]:
    """Configures user crontab entry for Linux."""
    args = [f'"{bin_path}"', "-p", f'"{src_path}"']
    if dest_path:
        args.extend(["-o", f'"{dest_path}"'])
    if dry_run:
        args.append("-d")

    cmd_str = " ".join(args)
    config_dir = get_config_dir()
    cron_line = f"{cron_expr} cd {config_dir} && {cmd_str} # FOLDER-SORTER-TASK\n"

    try:
        res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        lines: list[str] = []
        if res.returncode == 0:
            lines = res.stdout.splitlines()

        lines = [line for line in lines if "# FOLDER-SORTER-TASK" not in line]
        lines.append(cron_line.strip())

        new_cron_content = "\n".join(lines) + "\n"

        proc = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        _, err = proc.communicate(input=new_cron_content)

        if proc.returncode == 0:
            return True, "Завдання додано в crontab."
        else:
            return False, f"crontab помилка: {err.strip()}"
    except Exception as e:
        return False, f"Помилка crontab: {e}"


def remove_cron() -> tuple[bool, str]:
    """Removes user crontab entry for Linux."""
    try:
        res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if res.returncode != 0:
            return True, "crontab порожній або відсутній."

        lines = res.stdout.splitlines()
        filtered = [line for line in lines if "# FOLDER-SORTER-TASK" not in line]

        if len(filtered) == len(lines):
            return True, "Завдання не знайдено в crontab."

        if not filtered or (len(filtered) == 1 and not filtered[0].strip()):
            subprocess.run(["crontab", "-r"], capture_output=True)
            return True, "crontab очищено."
        else:
            new_cron_content = "\n".join(filtered) + "\n"
            proc = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            _, err = proc.communicate(input=new_cron_content)
            if proc.returncode == 0:
                return True, "Завдання видалено з crontab."
            else:
                return False, f"crontab помилка: {err.strip()}"
    except Exception as e:
        return False, f"Помилка crontab: {e}"
