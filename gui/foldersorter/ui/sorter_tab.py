"""Sorter tab component managing folder inputs, options, log console, and execution thread."""

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from foldersorter import runner
from foldersorter.ui.components import CustomButton

if TYPE_CHECKING:
    from foldersorter.ui.app import FolderSorterApp


class SorterTab(tk.Frame):
    """Tab 1: Select directories, toggle dry-run options, log sorting operations."""

    def __init__(self, parent: tk.Widget, app: "FolderSorterApp") -> None:
        super().__init__(parent, bg="#1e1e2e")
        self.app = app

        # Main Panel
        panel = tk.Frame(self, bg="#1e1e2e", padx=20, pady=10)
        panel.pack(fill="both", expand=True)

        # 1. Source Dir Row
        src_frame = tk.Frame(panel, bg="#1e1e2e")
        src_frame.pack(fill="x", pady=6)

        src_lbl = tk.Label(
            src_frame,
            text="Шлях до вихідної папки:",
            bg="#1e1e2e",
            fg="#a6adc8",
            font=("Helvetica", 10, "bold"),
            width=22,
            anchor="w",
        )
        src_lbl.pack(side="left")

        self.src_entry = tk.Entry(
            src_frame,
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            bd=5,
            font=("Helvetica", 10),
        )
        self.src_entry.pack(side="left", fill="x", expand=True, padx=10)

        src_browse = CustomButton(
            src_frame,
            "Огляд...",
            self.browse_src,
            bg_color="#313244",
            hover_color="#45475a",
            fg_color="#cdd6f4",
            padx=10,
            pady=5,
        )
        src_browse.pack(side="right")

        # 2. Target Dir Row
        target_toggle_frame = tk.Frame(panel, bg="#1e1e2e")
        target_toggle_frame.pack(fill="x", pady=(10, 2))

        self.use_target_var = tk.BooleanVar(value=False)
        self.target_cb = tk.Checkbutton(
            target_toggle_frame,
            text="Сортувати файли в іншу папку (за замовчуванням — туди ж)",
            variable=self.use_target_var,
            command=self.toggle_target_fields,
            bg="#1e1e2e",
            fg="#cdd6f4",
            activebackground="#1e1e2e",
            activeforeground="#cba6f7",
            selectcolor="#252538",
            font=("Helvetica", 9, "bold"),
        )
        self.target_cb.pack(side="left")

        self.dest_frame = tk.Frame(panel, bg="#1e1e2e")
        self.dest_frame.pack(fill="x", pady=4)

        self.dest_lbl = tk.Label(
            self.dest_frame,
            text="Папка призначення:",
            bg="#1e1e2e",
            fg="#585b70",
            font=("Helvetica", 10, "bold"),
            width=22,
            anchor="w",
        )
        self.dest_lbl.pack(side="left")

        self.dest_entry = tk.Entry(
            self.dest_frame,
            bg="#181825",
            fg="#585b70",
            insertbackground="#cdd6f4",
            relief="flat",
            bd=5,
            font=("Helvetica", 10),
            state="disabled",
        )
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=10)

        self.dest_browse = CustomButton(
            self.dest_frame,
            "Огляд...",
            self.browse_dest,
            bg_color="#181825",
            hover_color="#181825",
            fg_color="#585b70",
            padx=10,
            pady=5,
            state="disabled",
        )
        self.dest_browse.pack(side="right")

        # 3. Dry run checkbox
        options_frame = tk.Frame(panel, bg="#1e1e2e")
        options_frame.pack(fill="x", pady=10)

        self.dry_run_var = tk.BooleanVar(value=True)
        self.dry_cb = tk.Checkbutton(
            options_frame,
            text="🔍 Режим перевірки (Dry Run) — показати список змін без переміщення",
            variable=self.dry_run_var,
            bg="#1e1e2e",
            fg="#cdd6f4",
            activebackground="#1e1e2e",
            activeforeground="#cba6f7",
            selectcolor="#252538",
            font=("Helvetica", 10, "bold"),
        )
        self.dry_cb.pack(side="left")

        # 4. Action buttons frame
        actions_frame = tk.Frame(panel, bg="#1e1e2e", pady=10)
        actions_frame.pack(fill="x")

        self.run_btn = CustomButton(
            actions_frame,
            "🚀 Запустити сортування",
            self.start_sorting,
            bg_color="#a6e3a1",
            hover_color="#94e2d5",
            fg_color="#1e1e2e",
            font=("Helvetica", 11, "bold"),
            padx=25,
            pady=10,
        )
        self.run_btn.pack(side="left")

        self.clear_btn = CustomButton(
            actions_frame,
            "🧹 Очистити лог",
            self.clear_log,
            bg_color="#313244",
            hover_color="#45475a",
            fg_color="#cdd6f4",
            font=("Helvetica", 10),
            padx=15,
            pady=8,
        )
        self.clear_btn.pack(side="right", pady=3)

        # 5. Log area
        log_frame = tk.Frame(panel, bg="#181825", bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True, pady=(10, 0))

        log_scrollbar = tk.Scrollbar(log_frame)
        log_scrollbar.pack(side="right", fill="y")

        self.log_area = tk.Text(
            log_frame,
            bg="#181825",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            font=("Courier", 10),
            wrap="word",
            yscrollcommand=log_scrollbar.set,
        )
        self.log_area.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        log_scrollbar.config(command=self.log_area.yview)

        # Initial greeting in log
        self.log_area.insert("end", "=== Folder Sorter GUI Console ===\n")
        self.log_area.insert(
            "end",
            "Для початку роботи виберіть папку для сортування та натисніть кнопку Запуску.\n\n",
        )
        self.log_area.configure(state="disabled")

    def toggle_target_fields(self) -> None:
        """Enables/disables target directory inputs according to checkbox state."""
        use_target = self.use_target_var.get()
        if use_target:
            self.dest_lbl.configure(fg="#a6adc8")
            self.dest_entry.configure(
                state="normal", bg="#313244", fg="#cdd6f4"
            )
            self.dest_browse.configure_state(
                "normal", bg_color="#313244", hover_color="#45475a"
            )
            self.dest_browse.label.configure(fg="#cdd6f4")
        else:
            self.dest_lbl.configure(fg="#585b70")
            self.dest_entry.configure(
                state="disabled", bg="#181825", fg="#585b70"
            )
            self.dest_browse.configure_state(
                "disabled", bg_color="#181825", hover_color="#181825"
            )
            self.dest_browse.label.configure(fg="#585b70")

    def browse_src(self) -> None:
        """Opens folder dialog to pick source folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, "end")
            self.src_entry.insert(0, os.path.normpath(folder))

    def browse_dest(self) -> None:
        """Opens folder dialog to pick destination folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, os.path.normpath(folder))

    def log(self, message: str) -> None:
        """Thread-safe logging method targeting Tkinter main loop."""
        self.after(0, self._log_safe, message)

    def _log_safe(self, message: str) -> None:
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def clear_log(self) -> None:
        """Clears console log output."""
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.insert("end", "=== Лог очищено ===\n\n")
        self.log_area.configure(state="disabled")

    def set_running_state(self, is_running: bool) -> None:
        """Thread-safe method to update run button state and text."""
        def update() -> None:
            if is_running:
                self.run_btn.configure_state(
                    "disabled",
                    text="⏳ Працюємо...",
                    bg_color="#585b70",
                    hover_color="#585b70",
                )
                self.run_btn.label.configure(fg="#a6adc8")
            else:
                self.run_btn.configure_state(
                    "normal",
                    text="🚀 Запустити сортування",
                    bg_color="#a6e3a1",
                    hover_color="#94e2d5",
                )
                self.run_btn.label.configure(fg="#1e1e2e")

        self.after(0, update)

    def start_sorting(self) -> None:
        """Validates input fields and launches sorting worker thread."""
        src_path = self.src_entry.get().strip()
        if not src_path:
            messagebox.showwarning(
                "Попередження", "Виберіть шлях до вихідної папки!"
            )
            return

        if not Path(src_path).exists():
            messagebox.showerror(
                "Помилка", f"Вихідна папка не існує:\n{src_path}"
            )
            return

        use_target = self.use_target_var.get()
        target_path = self.dest_entry.get().strip() if use_target else ""
        if use_target and not target_path:
            messagebox.showwarning(
                "Попередження",
                "Виберіть папку призначення або вимкніть опцію іншої папки!",
            )
            return

        dry_run = self.dry_run_var.get()
        self.set_running_state(True)

        thread = threading.Thread(
            target=self.run_sorter_worker,
            args=(src_path, target_path, dry_run),
            daemon=True,
        )
        thread.start()

    def run_sorter_worker(
        self, src_path: str, target_path: str, dry_run: bool
    ) -> None:
        """Worker thread body executing CLI discovery, compilation if needed, and process run."""
        cli_path = self.app.get_cli_path()
        if not cli_path:
            compiled = runner.compile_cli(self.app.cli_dir, self.log)
            if not compiled:
                self.log("❌ Не вдалося знайти або скомпілювати CLI інструмент.")
                self.set_running_state(False)
                return
            cli_path = self.app.get_cli_path()
            if not cli_path:
                self.log("❌ Не вдалося знайти бінарний файл після компіляції.")
                self.set_running_state(False)
                return

        runner.run_sorter_process(
            cli_path=cli_path,
            src_path=src_path,
            target_path=target_path if target_path else None,
            dry_run=dry_run,
            log_callback=self.log,
        )
        self.set_running_state(False)
