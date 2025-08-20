import tkinter as tk
from tkinter import ttk

from ..ui import theme

class ScrollableFrame(ttk.Frame):
    """A vertically scrollable frame for the category buttons."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self._inner_id, width=e.width),
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.apply_theme()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def apply_theme(self) -> None:
        """Update the canvas background to match the active theme."""
        self.canvas.configure(bg=theme.get_color("background"))
