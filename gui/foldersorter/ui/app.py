"""Main application window for FolderSorter GUI."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from foldersorter import runner
from foldersorter.config import get_config_dir
from foldersorter.ui.rules_tab import RulesTab
from foldersorter.ui.scheduler_tab import SchedulerTab
from foldersorter.ui.sorter_tab import SorterTab


class FolderSorterApp(tk.Tk):
    """Main Application Window containing header branding and tab notebook."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Folder Sorter GUI")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        self.center_window(850, 680)

        # Paths resolution
        package_dir = Path(__file__).resolve().parent.parent
        self.cli_dir = (package_dir.parent / "cli").resolve()
        self.config_path = get_config_dir() / "cleaner_config.toml"

        self.setup_styles()
        self.create_widgets()

    def center_window(self, width: int, height: int) -> None:
        """Centers window on primary display screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self) -> None:
        """Configures ttk dark styling for tabs and notebook."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background="#252538",
            foreground="#cdd6f4",
            padding=[15, 6],
            font=("Helvetica", 10, "bold"),
            borderwidth=0,
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "#1e1e2e"), ("active", "#313244")],
            foreground=[("selected", "#cba6f7"), ("active", "#cdd6f4")],
        )

    def create_widgets(self) -> None:
        """Creates top header banner and main tab navigation notebook."""
        # Header block
        header_frame = tk.Frame(self, bg="#1e1e2e", pady=15)
        header_frame.pack(fill="x")

        app_title = tk.Label(
            header_frame,
            text="📁 FOLDER SORTER",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Helvetica", 16, "bold"),
        )
        app_title.pack()

        # Main Tab container
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # TAB 1: Sorter
        self.sorter_tab = SorterTab(self.notebook, self)
        self.notebook.add(self.sorter_tab, text=" Сортування ")

        # TAB 2: Rules Settings
        self.rules_tab = RulesTab(self.notebook, self.config_path)
        self.notebook.add(self.rules_tab, text=" Налаштування правил ")

        # TAB 3: Scheduler settings
        self.scheduler_tab = SchedulerTab(self.notebook, self)
        self.notebook.add(self.scheduler_tab, text=" Планувальник ")

        # Update scheduler tab status when user changes tabs
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event: tk.Event) -> None:
        """Handles tab switch event to refresh scheduler status."""
        selected_index = self.notebook.index(self.notebook.select())
        if selected_index == 2:  # Scheduler tab index
            self.scheduler_tab.update_status()

    def get_cli_path(self) -> Path | None:
        """Helper method resolving executable CLI path."""
        return runner.get_cli_path(self.cli_dir)
