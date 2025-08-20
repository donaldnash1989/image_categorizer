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
        # Reflow when the inner frame or its canvas changes size
        self._scroll.inner.bind("<Configure>", self._reflow_buttons, add="+")
        self._scroll.canvas.bind("<Configure>", self._reflow_buttons, add="+")

        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, sticky="ew", pady=(6,0))
        footer.columnconfigure(0, weight=1)
        self._delete_btn = ttk.Button(
            footer,
            text="Delete",
            style="Danger.TButton",
            command=lambda: self._on_delete() if self._on_delete else None,
        )
        self._delete_btn.pack(side="right", padx=6, pady=4)

        self._buttons: list[ttk.Button] = []
        self._current_cols: int | None = None

    def set_categories(self, categories: list[str]) -> None:
        for b in self._buttons:
            b.destroy()
        self._buttons.clear()

        if not categories:
            return

        for name in categories:
            btn = ttk.Button(
                self._scroll.inner, text=name, command=lambda n=name: self._on_click(n)
            )
            self._buttons.append(btn)

        self._reflow_buttons()

    def _reflow_buttons(self, event=None) -> None:
        if not self._buttons:
            return

        inner = self._scroll.inner
        width = event.width if event else inner.winfo_width()
        if width <= 0:
            return

        btn_width = max(b.winfo_reqwidth() for b in self._buttons)
        total = btn_width + self._config.ui.button_padx * 2
        cols = max(width // total, 1)

        if cols == self._current_cols:
            return
        self._current_cols = cols

        for idx, btn in enumerate(self._buttons):
            row = idx // cols
            col = idx % cols
            btn.grid(
                row=row,
                column=col,
                padx=self._config.ui.button_padx,
                pady=self._config.ui.button_pady,
                sticky="ew",
            )

        # Reset column weights then apply for the active columns
        for c in range(inner.grid_size()[0]):
            inner.grid_columnconfigure(c, weight=0)
        for c in range(cols):
            inner.grid_columnconfigure(c, weight=1)

    def set_enabled(self, enabled: bool) -> None:
        state = "!disabled" if enabled else "disabled"
        for b in self._buttons:
            b.state([state])
        self._delete_btn.state([state])

    def apply_theme(self) -> None:
        """Update theme-dependent elements."""
        self._scroll.apply_theme()
