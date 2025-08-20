import tkinter as tk
from tkinter import ttk

from ..config import AppConfig
from ..preferences import save_preferences, Preferences


class UserSettingsView(ttk.Frame):
    def __init__(self, parent, config: AppConfig, on_theme_changed):
        super().__init__(parent)
        self._config = config
        self._on_theme_changed = on_theme_changed

        self.columnconfigure(0, weight=1)

        self._theme_var = tk.StringVar(value=self._config.theme)
        options = [("Light", "light"), ("System", "system"), ("Dark", "dark")]
        for idx, (label, value) in enumerate(options):
            rb = ttk.Radiobutton(
                self,
                text=label,
                value=value,
                variable=self._theme_var,
                command=self._theme_selected,
            )
            rb.grid(row=0, column=idx, padx=6, pady=6, sticky="w")

    def _theme_selected(self) -> None:
        self._config.theme = self._theme_var.get()
        save_preferences(Preferences(theme=self._config.theme))
        self._on_theme_changed(self._config.theme)
