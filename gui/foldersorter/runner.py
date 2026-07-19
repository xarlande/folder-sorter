"""CLI discovery, cargo compilation, and process execution runner module."""

import os
import platform
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from foldersorter.config import get_config_dir


def get_cli_path(cli_dir: Path | str) -> Path | None:
    """Discovers the executable location of the folder-sorter Rust CLI binary."""
    is_windows = platform.system() == "Windows"
    binary_name = "folder-sorter.exe" if is_windows else "folder-sorter"

    # 0. Check PyInstaller bundle path
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        bundle_bin = Path(meipass) / binary_name
        if bundle_bin.exists():
            try:
                bundle_bin.chmod(0o755)
            except OSError:
                pass
            return bundle_bin

    cli_path = Path(cli_dir).resolve()
    release_path = cli_path / "target" / "release" / binary_name
    debug_path = cli_path / "target" / "debug" / binary_name

    if release_path.exists():
        return release_path
    if debug_path.exists():
        return debug_path

    # Check system PATH
    sys_path = shutil.which("folder-sorter")
    if sys_path:
        return Path(sys_path)

    return None


def compile_cli(
    cli_dir: Path | str, log_callback: Callable[[str], None]
) -> bool:
    """Compiles Rust CLI binary using Cargo, outputting build logs to log_callback."""
    log_callback("🔧 CLI бінарник не знайдено. Починаю компіляцію з Cargo...")
    cli_path = Path(cli_dir).resolve()

    if not cli_path.exists():
        log_callback(f"❌ Помилка: Папка CLI не знайдена за шляхом {cli_path}.")
        return False

    creation_flags = (
        subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
    )

    try:
        process = subprocess.Popen(
            ["cargo", "build", "--release"],
            cwd=cli_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=creation_flags,
        )

        if process.stdout:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                log_callback(line.strip())

        process.wait()
        if process.returncode == 0:
            log_callback("✅ Компіляція завершена успішно!")
            return True
        else:
            log_callback(
                f"❌ Помилка компіляції: cargo build повернув код {process.returncode}"
            )
            return False

    except FileNotFoundError:
        log_callback(
            "❌ Помилка: інструмент 'cargo' не встановлено або не додано в PATH."
        )
        log_callback(
            "Встановіть Rust/Cargo з https://rustup.rs/ для автоматичної компіляції."
        )
        return False
    except Exception as e:
        log_callback(f"❌ Помилка при компіляції: {e}")
        return False


def run_sorter_process(
    cli_path: Path | str,
    src_path: Path | str,
    target_path: Path | str | None,
    dry_run: bool,
    log_callback: Callable[[str], None],
) -> int:
    """Runs the Rust CLI binary to sort the directory, logging stdout to log_callback."""
    cli_str = str(Path(cli_path).resolve())
    src_str = str(Path(src_path).resolve())
    target_str = str(Path(target_path).resolve()) if target_path else ""

    log_callback(f"📁 Використовую CLI: {cli_str}")
    log_callback(f"📂 Вихідна папка: {src_str}")
    log_callback(
        f"📥 Папка призначення: {target_str if target_str else '[та сама]'}"
    )
    log_callback(f"🔍 Режим перевірки (Dry Run): {'Так' if dry_run else 'Ні'}")
    log_callback("-" * 60)

    cmd = [cli_str, "-p", src_str]
    if target_str:
        cmd.extend(["-o", target_str])
    if dry_run:
        cmd.append("-d")

    creation_flags = (
        subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
    )

    try:
        process = subprocess.Popen(
            cmd,
            cwd=get_config_dir(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=creation_flags,
        )

        if process.stdout:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                log_callback(line.strip())

        process.wait()
        log_callback("-" * 60)
        if process.returncode == 0:
            log_callback("🎉 Сортування успішно завершено!")
        else:
            log_callback(
                f"⚠️ CLI повернув помилку з кодом: {process.returncode}"
            )
        return process.returncode
    except Exception as e:
        log_callback(f"❌ Помилка при виконанні: {e}")
        return -1
