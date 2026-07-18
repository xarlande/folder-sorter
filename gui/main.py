import os
import sys
import platform
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tomllib

# Default fallback rules matching the CLI's default config
DEFAULT_RULES = {
    "Зображення": ["jpg", "png", "jpeg", "gif", "svg"],
    "Відео": ["mp4", "mkv", "mov", "avi"],
    "Музика": ["mp3", "wav", "flac"],
    "Документи": ["pdf", "doc", "docx", "txt"],
    "Архіви": ["zip", "rar", "7z", "tar"],
    "Програми": ["exe", "msi", "deb"]
}

def load_rules(config_path):
    """Loads configuration rules from TOML config file."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("rules", {})
        except Exception as e:
            print(f"Помилка при зчитуванні TOML: {e}")
    return DEFAULT_RULES.copy()

def save_rules(config_path, rules):
    """Saves rules to TOML config file in the correct format."""
    try:
        # Ensure parent directories exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("[rules]\n")
            for cat, exts in rules.items():
                ext_list_str = ", ".join(f'"{x.strip().lower()}"' for x in exts if x.strip())
                f.write(f'"{cat}" = [{ext_list_str}]\n')
        return True
    except Exception as e:
        print(f"Помилка при збереженні TOML: {e}")
        return False

class CustomButton(tk.Frame):
    """A cross-platform flat button using tk.Frame & tk.Label for flawless custom styling on macOS & Windows."""
    def __init__(self, parent, text, command, bg_color, hover_color, fg_color="#1e1e2e", font=("Helvetica", 10, "bold"), padx=15, pady=8, state="normal"):
        super().__init__(parent, bg=bg_color, cursor="hand2")
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.state = state
        
        self.label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=font,
            padx=padx,
            pady=pady
        )
        self.label.pack(fill="both", expand=True)
        
        for widget in (self, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        if self.state == "normal":
            self.configure(bg=self.hover_color)
            self.label.configure(bg=self.hover_color)

    def _on_leave(self, event):
        if self.state == "normal":
            self.configure(bg=self.bg_color)
            self.label.configure(bg=self.bg_color)

    def _on_click(self, event):
        if self.state == "normal" and self.command:
            self.command()

    def configure_state(self, state, text=None, bg_color=None, hover_color=None):
        self.state = state
        if text is not None:
            self.label.configure(text=text)
        if bg_color is not None:
            self.bg_color = bg_color
            self.configure(bg=bg_color)
            self.label.configure(bg=bg_color)
        if hover_color is not None:
            self.hover_color = hover_color
        
        if state == "disabled":
            self.configure(cursor="arrow")
            self.label.configure(cursor="arrow")
        else:
            self.configure(cursor="hand2")
            self.label.configure(cursor="hand2")

class ScrollableFrame(tk.Frame):
    """A custom scrollable frame wrapper using Canvas for config forms."""
    def __init__(self, container, bg="#1e1e2e", *args, **kwargs):
        super().__init__(container, bg=bg, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=bg)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 5:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        else:
            if event.delta:
                direction = -1 if event.delta > 0 else 1
                self.canvas.yview_scroll(direction, "units")

class RulesTab(tk.Frame):
    """Tab 2: Edit rules and categories for cleaner_config.toml."""
    def __init__(self, parent, config_path):
        super().__init__(parent, bg="#1e1e2e")
        self.config_path = config_path
        self.rule_rows = []

        # Info Header
        info_lbl = tk.Label(
            self,
            text="⚙️ Налаштуйте категорії сортування та їхні розширення",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Helvetica", 12, "bold"),
            pady=15
        )
        info_lbl.pack(fill="x")

        # Rules container (scrollable)
        self.scroll_frame = ScrollableFrame(self, bg="#1e1e2e")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Control Bar
        ctrl_frame = tk.Frame(self, bg="#1e1e2e", pady=15)
        ctrl_frame.pack(fill="x", padx=20)

        self.add_btn = CustomButton(
            ctrl_frame, "➕ Додати категорію", self.add_empty_rule,
            bg_color="#cba6f7", hover_color="#b4befe", fg_color="#1e1e2e"
        )
        self.add_btn.pack(side="left", padx=5)

        self.save_btn = CustomButton(
            ctrl_frame, "💾 Зберегти конфігурацію", self.save_changes,
            bg_color="#a6e3a1", hover_color="#94e2d5", fg_color="#1e1e2e"
        )
        self.save_btn.pack(side="right", padx=5)

        self.reload_btn = CustomButton(
            ctrl_frame, "🔄 Скасувати зміни", self.load_rules_ui,
            bg_color="#f38ba8", hover_color="#f5c2e7", fg_color="#1e1e2e"
        )
        self.reload_btn.pack(side="right", padx=5)

        self.load_rules_ui()

    def load_rules_ui(self):
        # Clear existing rows
        for row in self.rule_rows:
            row["frame"].destroy()
        self.rule_rows.clear()

        rules = load_rules(self.config_path)
        for cat, exts in rules.items():
            self.create_rule_row(cat, exts)

    def create_rule_row(self, category="", extensions=[]):
        row_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg="#252538", pady=8, padx=12)
        row_frame.pack(fill="x", pady=5, padx=5)

        # Category text field
        cat_lbl = tk.Label(row_frame, text="Категорія:", bg="#252538", fg="#a6adc8", font=("Helvetica", 9, "bold"))
        cat_lbl.pack(side="left", padx=(0, 5))

        cat_entry = tk.Entry(row_frame, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", relief="flat", bd=4, width=16, font=("Helvetica", 10))
        cat_entry.insert(0, category)
        cat_entry.pack(side="left", padx=(0, 15))

        # Extensions text field
        exts_lbl = tk.Label(row_frame, text="Розширення:", bg="#252538", fg="#a6adc8", font=("Helvetica", 9, "bold"))
        exts_lbl.pack(side="left", padx=(0, 5))

        ext_str = ", ".join(extensions)
        exts_entry = tk.Entry(row_frame, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", relief="flat", bd=4, font=("Helvetica", 10))
        exts_entry.insert(0, ext_str)
        exts_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        # Row delete button
        del_btn = CustomButton(
            row_frame, "Видалити", lambda f=row_frame: self.delete_rule_row(f),
            bg_color="#f38ba8", hover_color="#f2cdcd", fg_color="#1e1e2e", padx=8, pady=4, font=("Helvetica", 8, "bold")
        )
        del_btn.pack(side="right")

        self.rule_rows.append({
            "category_entry": cat_entry,
            "exts_entry": exts_entry,
            "frame": row_frame
        })

    def delete_rule_row(self, frame):
        for idx, row in enumerate(self.rule_rows):
            if row["frame"] == frame:
                row["frame"].destroy()
                self.rule_rows.pop(idx)
                break

    def add_empty_rule(self):
        self.create_rule_row("", [])

    def save_changes(self):
        rules = {}
        for row in self.rule_rows:
            cat = row["category_entry"].get().strip()
            exts_raw = row["exts_entry"].get()
            if not cat:
                continue
            # Parse commas and spaces
            exts = [x.strip().lower() for x in exts_raw.replace(",", " ").split() if x.strip()]
            rules[cat] = exts
            
        success = save_rules(self.config_path, rules)
        if success:
            messagebox.showinfo("Збережено", "Конфігурацію успішно збережено!")
        else:
            messagebox.showerror("Помилка", "Не вдалося зберегти конфігурацію.")

class Application(tk.Tk):
    """Main Application GUI Window."""
    def __init__(self):
        super().__init__()
        
        self.title("Folder Sorter GUI")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)
        
        # Center window with default dimensions
        self.center_window(850, 680)

        # Paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.cli_dir = os.path.abspath(os.path.join(script_dir, "..", "cli"))
        self.config_path = os.path.join(self.cli_dir, "cleaner_config.toml")
        
        # Setup styles
        self.setup_styles()
        
        # Create Main layout container
        self.create_widgets()
        
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        # Dark styling for tabs
        self.style.configure('TNotebook', background='#1e1e2e', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#252538', foreground='#cdd6f4', padding=[15, 6], font=('Helvetica', 10, 'bold'), borderwidth=0)
        self.style.map('TNotebook.Tab', 
                       background=[('selected', '#1e1e2e'), ('active', '#313244')], 
                       foreground=[('selected', '#cba6f7'), ('active', '#cdd6f4')])

    def create_widgets(self):
        # Header block
        header_frame = tk.Frame(self, bg="#1e1e2e", pady=15)
        header_frame.pack(fill="x")
        
        app_title = tk.Label(
            header_frame,
            text="📁 FOLDER SORTER",
            bg="#1e1e2e",
            fg="#cba6f7",
            font=("Helvetica", 16, "bold")
        )
        app_title.pack()
        
        # Main Tab container
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # TAB 1: Sorter
        self.sorter_tab = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.sorter_tab, text=" Сортування ")
        self.build_sorter_tab()

        # TAB 2: Rules Settings
        self.rules_tab = RulesTab(self.notebook, self.config_path)
        self.notebook.add(self.rules_tab, text=" Налаштування правил ")

    def build_sorter_tab(self):
        # Main Panel
        panel = tk.Frame(self.sorter_tab, bg="#1e1e2e", padx=20, pady=10)
        panel.pack(fill="both", expand=True)

        # 1. Source Dir Row
        src_frame = tk.Frame(panel, bg="#1e1e2e")
        src_frame.pack(fill="x", pady=6)
        
        src_lbl = tk.Label(src_frame, text="Шлях до вихідної папки:", bg="#1e1e2e", fg="#a6adc8", font=("Helvetica", 10, "bold"), width=22, anchor="w")
        src_lbl.pack(side="left")
        
        self.src_entry = tk.Entry(src_frame, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", relief="flat", bd=5, font=("Helvetica", 10))
        self.src_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        src_browse = CustomButton(
            src_frame, "Огляд...", self.browse_src,
            bg_color="#313244", hover_color="#45475a", fg_color="#cdd6f4", padx=10, pady=5
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
            font=("Helvetica", 9, "bold")
        )
        self.target_cb.pack(side="left")

        self.dest_frame = tk.Frame(panel, bg="#1e1e2e")
        self.dest_frame.pack(fill="x", pady=4)
        
        self.dest_lbl = tk.Label(self.dest_frame, text="Папка призначення:", bg="#1e1e2e", fg="#585b70", font=("Helvetica", 10, "bold"), width=22, anchor="w")
        self.dest_lbl.pack(side="left")
        
        self.dest_entry = tk.Entry(self.dest_frame, bg="#181825", fg="#585b70", insertbackground="#cdd6f4", relief="flat", bd=5, font=("Helvetica", 10), state="disabled")
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        self.dest_browse = CustomButton(
            self.dest_frame, "Огляд...", self.browse_dest,
            bg_color="#181825", hover_color="#181825", fg_color="#585b70", padx=10, pady=5, state="disabled"
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
            font=("Helvetica", 10, "bold")
        )
        self.dry_cb.pack(side="left")

        # 4. Action buttons frame
        actions_frame = tk.Frame(panel, bg="#1e1e2e", pady=10)
        actions_frame.pack(fill="x")
        
        self.run_btn = CustomButton(
            actions_frame, "🚀 Запустити сортування", self.start_sorting,
            bg_color="#a6e3a1", hover_color="#94e2d5", fg_color="#1e1e2e", font=("Helvetica", 11, "bold"), padx=25, pady=10
        )
        self.run_btn.pack(side="left")

        self.clear_btn = CustomButton(
            actions_frame, "🧹 Очистити лог", self.clear_log,
            bg_color="#313244", hover_color="#45475a", fg_color="#cdd6f4", font=("Helvetica", 10), padx=15, pady=8
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
            yscrollcommand=log_scrollbar.set
        )
        self.log_area.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        log_scrollbar.config(command=self.log_area.yview)
        
        # Initial greeting in the log
        self.log_area.insert("end", "=== Folder Sorter GUI Console ===\n")
        self.log_area.insert("end", "Для початку роботи виберіть папку для сортування та натисніть кнопку Запуску.\n\n")
        self.log_area.configure(state="disabled")

    def toggle_target_fields(self):
        use_target = self.use_target_var.get()
        if use_target:
            self.dest_lbl.configure(fg="#a6adc8")
            self.dest_entry.configure(state="normal", bg="#313244", fg="#cdd6f4")
            self.dest_browse.configure_state("normal", bg_color="#313244", hover_color="#45475a")
            self.dest_browse.label.configure(fg="#cdd6f4")
        else:
            self.dest_lbl.configure(fg="#585b70")
            self.dest_entry.configure(state="disabled", bg="#181825", fg="#585b70")
            self.dest_browse.configure_state("disabled", bg_color="#181825", hover_color="#181825")
            self.dest_browse.label.configure(fg="#585b70")

    def browse_src(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, "end")
            self.src_entry.insert(0, os.path.normpath(folder))

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, os.path.normpath(folder))

    def log(self, message):
        self.after(0, self._log_safe, message)

    def _log_safe(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def clear_log(self):
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.insert("end", "=== Лог очищено ===\n\n")
        self.log_area.configure(state="disabled")

    def set_running_state(self, is_running):
        def update():
            if is_running:
                self.run_btn.configure_state("disabled", text="⏳ Працюємо...", bg_color="#585b70", hover_color="#585b70")
                self.run_btn.label.configure(fg="#a6adc8")
            else:
                self.run_btn.configure_state("normal", text="🚀 Запустити сортування", bg_color="#a6e3a1", hover_color="#94e2d5")
                self.run_btn.label.configure(fg="#1e1e2e")
        self.after(0, update)

    def get_cli_path(self):
        is_windows = platform.system() == "Windows"
        binary_name = "folder-sorter.exe" if is_windows else "folder-sorter"
        
        # Paths relative to gui/main.py
        release_path = os.path.abspath(os.path.join(self.cli_dir, "target", "release", binary_name))
        debug_path = os.path.abspath(os.path.join(self.cli_dir, "target", "debug", binary_name))
        
        if os.path.exists(release_path):
            return release_path
        if os.path.exists(debug_path):
            return debug_path
            
        # Check system path
        sys_path = shutil.which("folder-sorter")
        if sys_path:
            return sys_path
            
        return None

    def compile_cli(self):
        self.log("🔧 CLI бінарник не знайдено. Починаю компіляцію з Cargo...")
        if not os.path.exists(self.cli_dir):
            self.log("❌ Помилка: Папка CLI не знайдена у проекті.")
            return False
            
        try:
            process = subprocess.Popen(
                ["cargo", "build", "--release"],
                cwd=self.cli_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                self.log(line.strip())
                
            process.wait()
            if process.returncode == 0:
                self.log("✅ Компіляція завершена успішно!")
                return True
            else:
                self.log(f"❌ Помилка компіляції: cargo build повернув код {process.returncode}")
                return False
                
        except FileNotFoundError:
            self.log("❌ Помилка: інструмент 'cargo' не встановлено або не додано в PATH.")
            self.log("Встановіть Rust/Cargo з https://rustup.rs/ для автоматичної компіляції.")
            return False
        except Exception as e:
            self.log(f"❌ Помилка при компіляції: {str(e)}")
            return False

    def start_sorting(self):
        src_path = self.src_entry.get().strip()
        if not src_path:
            messagebox.showwarning("Попередження", "Виберіть шлях до вихідної папки!")
            return
            
        if not os.path.exists(src_path):
            messagebox.showerror("Помилка", f"Вихідна папка не існує:\n{src_path}")
            return

        use_target = self.use_target_var.get()
        target_path = self.dest_entry.get().strip() if use_target else ""
        if use_target and not target_path:
            messagebox.showwarning("Попередження", "Виберіть папку призначення або вимкніть опцію іншої папки!")
            return
            
        dry_run = self.dry_run_var.get()

        # Disable run button
        self.set_running_state(True)
        
        # Start worker thread
        thread = threading.Thread(
            target=self.run_sorter,
            args=(src_path, target_path, dry_run),
            daemon=True
        )
        thread.start()

    def run_sorter(self, src_path, target_path, dry_run):
        cli_path = self.get_cli_path()
        if not cli_path:
            compiled = self.compile_cli()
            if not compiled:
                self.log("❌ Не вдалося знайти або скомпілювати CLI інструмент.")
                self.set_running_state(False)
                return
            cli_path = self.get_cli_path()
            if not cli_path:
                self.log("❌ Не вдалося знайти бінарний файл після компіляції.")
                self.set_running_state(False)
                return
                
        self.log(f"📁 Використовую CLI: {cli_path}")
        self.log(f"📂 Вихідна папка: {src_path}")
        self.log(f"📥 Папка призначення: {target_path if target_path else '[та сама]'}")
        self.log(f"🔍 Режим перевірки (Dry Run): {'Так' if dry_run else 'Ні'}")
        self.log("-" * 60)

        # Assemble CLI command
        cmd = [cli_path, "-p", src_path]
        if target_path:
            cmd.extend(["-o", target_path])
        if dry_run:
            cmd.append("-d")

        try:
            # We execute it in the CLI directory so cleaner_config.toml is found
            process = subprocess.Popen(
                cmd,
                cwd=self.cli_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                self.log(line.strip())

            process.wait()
            self.log("-" * 60)
            if process.returncode == 0:
                self.log("🎉 Сортування успішно завершено!")
            else:
                self.log(f"⚠️ CLI повернув помилку з кодом: {process.returncode}")
        except Exception as e:
            self.log(f"❌ Помилка при виконанні: {str(e)}")

        self.set_running_state(False)

if __name__ == "__main__":
    app = Application()
    app.mainloop()