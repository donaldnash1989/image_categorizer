import tkinter as tk
from tkinter import ttk
from ..config import AppConfig
from ..utils.tk_helpers import ScrollableFrame

class ButtonPanel(ttk.Frame):
    def __init__(self, parent, on_click, config: AppConfig):
        super().__init__(parent)
        self._on_click = on_click
        self._config = config
        self._scroll = ScrollableFrame(self)
        self._scroll.pack(fill="both", expand=True)
        self._buttons: list[ttk.Button] = []

    def set_categories(self, categories: list[str]) -> None:
        for b in self._buttons:
            b.destroy()
        self._buttons.clear()

        if not categories:
            return

        row = 0; col = 0
        for name in categories:
            btn = ttk.Button(self._scroll.inner, text=name, command=lambda n=name: self._on_click(n))
            btn.grid(row=row, column=col, padx=self._config.ui.button_padx, pady=self._config.ui.button_pady, sticky="ew")
            self._buttons.append(btn)
            col += 1
            if col >= self._config.ui.buttons_per_row:
                col = 0; row += 1

        for c in range(self._config.ui.buttons_per_row):
            self._scroll.inner.grid_columnconfigure(c, weight=1)

    def set_enabled(self, enabled: bool) -> None:
        state = "!disabled" if enabled else "disabled"
        for b in self._buttons:
            b.state([state])
