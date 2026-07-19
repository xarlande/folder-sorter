"""Reusable custom Tkinter UI components for FolderSorter GUI."""

import tkinter as tk
from collections.abc import Callable


class CustomButton(tk.Frame):
    """A cross-platform flat button using tk.Frame & tk.Label for custom styling."""

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Callable[[], None] | None = None,
        bg_color: str = "#313244",
        hover_color: str = "#45475a",
        fg_color: str = "#1e1e2e",
        font: tuple[str, int] | tuple[str, int, str] = ("Helvetica", 10, "bold"),
        padx: int = 15,
        pady: int = 8,
        state: str = "normal",
    ) -> None:
        super().__init__(parent, bg=bg_color, cursor="hand2" if state == "normal" else "arrow")
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
            pady=pady,
            cursor="hand2" if state == "normal" else "arrow",
        )
        self.label.pack(fill="both", expand=True)

        for widget in (self, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event: tk.Event) -> None:
        if self.state == "normal":
            self.configure(bg=self.hover_color)
            self.label.configure(bg=self.hover_color)

    def _on_leave(self, event: tk.Event) -> None:
        if self.state == "normal":
            self.configure(bg=self.bg_color)
            self.label.configure(bg=self.bg_color)

    def _on_click(self, event: tk.Event) -> None:
        if self.state == "normal" and self.command:
            self.command()

    def configure_state(
        self,
        state: str,
        text: str | None = None,
        bg_color: str | None = None,
        hover_color: str | None = None,
    ) -> None:
        """Updates widget state (normal/disabled) and optional styling properties."""
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
    """A custom scrollable frame wrapper using Canvas for dynamic forms."""

    def __init__(
        self, container: tk.Widget, bg: str = "#1e1e2e", *args: object, **kwargs: object
    ) -> None:
        super().__init__(container, bg=bg, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=bg)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        if getattr(event, "num", None) == 5:
            self.canvas.yview_scroll(1, "units")
        elif getattr(event, "num", None) == 4:
            self.canvas.yview_scroll(-1, "units")
        else:
            delta = getattr(event, "delta", 0)
            if delta:
                direction = -1 if delta > 0 else 1
                self.canvas.yview_scroll(direction, "units")
