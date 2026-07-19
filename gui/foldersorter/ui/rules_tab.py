"""Rules settings tab component for editing category extensions."""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Any

from foldersorter.config import load_rules, save_rules
from foldersorter.ui.components import CustomButton, ScrollableFrame


class RulesTab(tk.Frame):
    """Tab 2: Edit rules and categories for cleaner_config.toml."""

    def __init__(self, parent: tk.Widget, config_path: Path | str) -> None:
        super().__init__(parent, bg="#1e1e2e")
        self.config_path = Path(config_path)
        self.rule_rows: list[dict[str, Any]] = []

        # Info Header
        info_lbl = tk.Label(
            self,
            text="⚙️ Налаштуйте категорії сортування та їхні розширення",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Helvetica", 12, "bold"),
            pady=15,
        )
        info_lbl.pack(fill="x")

        # Rules container (scrollable)
        self.scroll_frame = ScrollableFrame(self, bg="#1e1e2e")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Control Bar
        ctrl_frame = tk.Frame(self, bg="#1e1e2e", pady=15)
        ctrl_frame.pack(fill="x", padx=20)

        self.add_btn = CustomButton(
            ctrl_frame,
            "➕ Додати категорію",
            self.add_empty_rule,
            bg_color="#cba6f7",
            hover_color="#b4befe",
            fg_color="#1e1e2e",
        )
        self.add_btn.pack(side="left", padx=5)

        self.save_btn = CustomButton(
            ctrl_frame,
            "💾 Зберегти конфігурацію",
            self.save_changes,
            bg_color="#a6e3a1",
            hover_color="#94e2d5",
            fg_color="#1e1e2e",
        )
        self.save_btn.pack(side="right", padx=5)

        self.reload_btn = CustomButton(
            ctrl_frame,
            "🔄 Скасувати зміни",
            self.load_rules_ui,
            bg_color="#f38ba8",
            hover_color="#f5c2e7",
            fg_color="#1e1e2e",
        )
        self.reload_btn.pack(side="right", padx=5)

        self.load_rules_ui()

    def load_rules_ui(self) -> None:
        """Clears existing rows and loads rules from config file."""
        for row in self.rule_rows:
            row["frame"].destroy()
        self.rule_rows.clear()

        rules = load_rules(self.config_path)
        for cat, exts in rules.items():
            self.create_rule_row(cat, exts)

    def create_rule_row(
        self, category: str = "", extensions: list[str] | None = None
    ) -> None:
        """Creates a single category and extension row in the scrollable frame."""
        ext_list = extensions if extensions is not None else []
        row_frame = tk.Frame(
            self.scroll_frame.scrollable_frame, bg="#252538", pady=8, padx=12
        )
        row_frame.pack(fill="x", pady=5, padx=5)

        # Category text field
        cat_lbl = tk.Label(
            row_frame,
            text="Категорія:",
            bg="#252538",
            fg="#a6adc8",
            font=("Helvetica", 9, "bold"),
        )
        cat_lbl.pack(side="left", padx=(0, 5))

        cat_entry = tk.Entry(
            row_frame,
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            bd=4,
            width=16,
            font=("Helvetica", 10),
        )
        cat_entry.insert(0, category)
        cat_entry.pack(side="left", padx=(0, 15))

        # Extensions text field
        exts_lbl = tk.Label(
            row_frame,
            text="Розширення:",
            bg="#252538",
            fg="#a6adc8",
            font=("Helvetica", 9, "bold"),
        )
        exts_lbl.pack(side="left", padx=(0, 5))

        ext_str = ", ".join(ext_list)
        exts_entry = tk.Entry(
            row_frame,
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            bd=4,
            font=("Helvetica", 10),
        )
        exts_entry.insert(0, ext_str)
        exts_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        # Row delete button
        del_btn = CustomButton(
            row_frame,
            "Видалити",
            lambda f=row_frame: self.delete_rule_row(f),
            bg_color="#f38ba8",
            hover_color="#f2cdcd",
            fg_color="#1e1e2e",
            padx=8,
            pady=4,
            font=("Helvetica", 8, "bold"),
        )
        del_btn.pack(side="right")

        self.rule_rows.append(
            {
                "category_entry": cat_entry,
                "exts_entry": exts_entry,
                "frame": row_frame,
            }
        )

    def delete_rule_row(self, frame: tk.Frame) -> None:
        """Deletes specified rule row frame."""
        for idx, row in enumerate(self.rule_rows):
            if row["frame"] == frame:
                row["frame"].destroy()
                self.rule_rows.pop(idx)
                break

    def add_empty_rule(self) -> None:
        """Adds a new blank rule row."""
        self.create_rule_row("", [])

    def save_changes(self) -> None:
        """Parses UI inputs and saves updated rules to TOML config file."""
        rules: dict[str, list[str]] = {}
        for row in self.rule_rows:
            cat = row["category_entry"].get().strip()
            exts_raw = row["exts_entry"].get()
            if not cat:
                continue
            exts = [
                x.strip().lower()
                for x in exts_raw.replace(",", " ").split()
                if x.strip()
            ]
            rules[cat] = exts

        success = save_rules(self.config_path, rules)
        if success:
            messagebox.showinfo("Збережено", "Конфігурацію успішно збережено!")
        else:
            messagebox.showerror("Помилка", "Не вдалося зберегти конфігурацію.")
