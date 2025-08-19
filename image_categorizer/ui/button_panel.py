import tkinter as tk
from tkinter import ttk
from ..config import AppConfig
from ..utils.tk_helpers import ScrollableFrame

class ButtonPanel(ttk.Frame):
    def __init__(self, parent, on_click, config: AppConfig, on_delete=None):
        super().__init__(parent)
        self._on_click = on_click
        self._on_delete = on_delete
        self._config = config

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._scroll = ScrollableFrame(self)
        self._scroll.grid(row=0, column=0, sticky="nsew")

        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, sticky="ew", pady=(6,0))
        footer.columnconfigure(0, weight=1)
        self._delete_btn = tk.Button(footer, text="Delete", fg="white", bg="#cc0000", activebackground="#990000",
                                     command=lambda: self._on_delete() if self._on_delete else None)
        self._delete_btn.pack(side="right", padx=6, pady=4)

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
        self._delete_btn.config(state="normal" if enabled else "disabled")
