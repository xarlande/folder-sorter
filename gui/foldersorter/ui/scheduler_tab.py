"""Scheduler settings tab component for background automated task control."""

import platform
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from foldersorter import scheduler
from foldersorter.config import INTERVALS
from foldersorter.ui.components import CustomButton

if TYPE_CHECKING:
    from foldersorter.ui.app import FolderSorterApp


class SchedulerTab(tk.Frame):
    """Tab 3: Configure platform-specific background scheduler."""

    def __init__(self, parent: tk.Widget, app: "FolderSorterApp") -> None:
        super().__init__(parent, bg="#1e1e2e")
        self.app = app
        self.system = platform.system()

        # Info Header
        info_lbl = tk.Label(
            self,
            text="⏰ Налаштування автоматичного сортування за розкладом",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Helvetica", 12, "bold"),
            pady=15,
        )
        info_lbl.pack(fill="x")

        # Scheduler Status Card
        status_card = tk.Frame(self, bg="#252538", pady=15, padx=20)
        status_card.pack(fill="x", padx=20, pady=10)

        status_title = tk.Label(
            status_card,
            text="Поточний статус планувальника:",
            bg="#252538",
            fg="#a6adc8",
            font=("Helvetica", 10, "bold"),
        )
        status_title.pack(side="left")

        self.status_lbl = tk.Label(
            status_card,
            text="ВИМКНЕНИЙ 🔴",
            bg="#252538",
            fg="#f38ba8",
            font=("Helvetica", 11, "bold"),
            padx=10,
        )
        self.status_lbl.pack(side="left")

        # Scheduler Name description
        self.status_desc_lbl = tk.Label(
            self,
            text=f"Використовується системний планувальник: {scheduler.get_system_scheduler_name(self.system)}",
            bg="#1e1e2e",
            fg="#7f849c",
            font=("Helvetica", 9, "italic"),
        )
        self.status_desc_lbl.pack(fill="x", padx=20, pady=(0, 15))

        # Configuration Settings Card
        settings_card = tk.Frame(self, bg="#252538", pady=15, padx=20)
        settings_card.pack(fill="x", padx=20, pady=5)

        # Interval selection
        int_frame = tk.Frame(settings_card, bg="#252538")
        int_frame.pack(fill="x", pady=5)

        int_lbl = tk.Label(
            int_frame,
            text="Інтервал виконання:",
            bg="#252538",
            fg="#cdd6f4",
            font=("Helvetica", 10, "bold"),
            width=20,
            anchor="w",
        )
        int_lbl.pack(side="left")

        self.interval_var = tk.StringVar(value="Кожну годину")
        self.interval_menu = ttk.Combobox(
            int_frame,
            textvariable=self.interval_var,
            values=list(INTERVALS.keys()),
            state="readonly",
            width=20,
        )
        self.interval_menu.pack(side="left", padx=10)

        # Prefill explanation
        prefill_lbl = tk.Label(
            settings_card,
            text="*Планувальник автоматично використовуватиме шляхи та режим 'Dry Run', налаштовані на першій вкладці.",
            bg="#252538",
            fg="#a6adc8",
            font=("Helvetica", 9, "italic"),
            pady=10,
        )
        prefill_lbl.pack(fill="x", anchor="w")

        # Control Buttons
        btn_frame = tk.Frame(self, bg="#1e1e2e", pady=20)
        btn_frame.pack(fill="x", padx=20)

        self.enable_btn = CustomButton(
            btn_frame,
            "💾 Увімкнути планувальник",
            self.enable_schedule,
            bg_color="#a6e3a1",
            hover_color="#94e2d5",
            fg_color="#1e1e2e",
        )
        self.enable_btn.pack(side="left", padx=5)

        self.disable_btn = CustomButton(
            btn_frame,
            "❌ Вимкнути планувальник",
            self.disable_schedule,
            bg_color="#f38ba8",
            hover_color="#f5c2e7",
            fg_color="#1e1e2e",
        )
        self.disable_btn.pack(side="left", padx=5)

        # Load initial status
        self.update_status()

    def update_status(self) -> None:
        """Queries OS scheduler status and updates UI card."""
        active = scheduler.is_scheduler_active(self.system)
        if active:
            self.status_lbl.configure(text="АКТИВНИЙ 🟢", fg="#a6e3a1")
        else:
            self.status_lbl.configure(text="ВИМКНЕНИЙ 🔴", fg="#f38ba8")

    def enable_schedule(self) -> None:
        """Enables automated background task via OS scheduler."""
        bin_path = self.app.get_cli_path()
        if not bin_path:
            messagebox.showwarning(
                "Помилка",
                "Не знайдено бінарний файл CLI. Спробуйте запустити сортування хоча б один раз на першій вкладці для автоматичної компіляції CLI.",
            )
            return

        src_path = self.app.sorter_tab.src_entry.get().strip()
        if not src_path:
            messagebox.showwarning(
                "Попередження",
                "Вкажіть шлях до вихідної папки на першій вкладці!",
            )
            return

        use_target = self.app.sorter_tab.use_target_var.get()
        dest_path = (
            self.app.sorter_tab.dest_entry.get().strip() if use_target else ""
        )
        dry_run = self.app.sorter_tab.dry_run_var.get()

        interval_key = self.interval_var.get()
        spec = INTERVALS.get(interval_key, INTERVALS["Кожну годину"])

        success, message = scheduler.enable_schedule(
            bin_path=bin_path,
            src_path=src_path,
            dest_path=dest_path,
            dry_run=dry_run,
            macos_seconds=spec.macos_seconds,
            windows_minutes=spec.windows_minutes,
            linux_cron=spec.linux_cron,
            system=self.system,
        )

        self.update_status()
        if success:
            messagebox.showinfo(
                "Планувальник", f"Планувальник успішно активовано!\n\nДеталі: {message}"
            )
        else:
            messagebox.showerror(
                "Помилка", f"Не вдалося активувати планувальник:\n\n{message}"
            )

    def disable_schedule(self) -> None:
        """Disables background automated task."""
        success, message = scheduler.disable_schedule(self.system)
        self.update_status()
        if success:
            messagebox.showinfo(
                "Планувальник", f"Планувальник вимкнено.\n\nДеталі: {message}"
            )
        else:
            messagebox.showerror(
                "Помилка", f"Не вдалося вимкнути планувальник:\n\n{message}"
            )
