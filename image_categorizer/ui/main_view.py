import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional
from ..config import AppConfig
from .image_view import ImageView
from .button_panel import ButtonPanel

class MainView(ttk.Frame):
    def __init__(self, root, config: AppConfig):
        super().__init__(root)
        self._root = root
        self._config = config

        self.pack(fill="both", expand=True)
        self._root.title("Photo Categorizer")
        self._root.minsize(*self._config.ui.min_window_size)

        self._nb = ttk.Notebook(self)
        self._page_main = ttk.Frame(self._nb)
        self._page_settings = ttk.Frame(self._nb)
        self._nb.add(self._page_main, text="Categorize")
        self._nb.add(self._page_settings, text="Settings")
        self._nb.pack(fill="both", expand=True)

        self._page_main.rowconfigure(0, weight=1)
        self._page_main.rowconfigure(1, weight=0)
        self._page_main.columnconfigure(0, weight=1)

        self.image_view = None
        self.button_panel = None

        self._status = ttk.Label(self, text="Ready", anchor="w")
        self._status.pack(fill="x", side="bottom")

    def build_main(self, image_view: ImageView, button_panel: ButtonPanel) -> None:
        self.image_view = image_view
        self.button_panel = button_panel
        image_view.grid(row=0, column=0, sticky="nsew", in_=self._page_main)
        button_panel.grid(row=1, column=0, sticky="nsew", in_=self._page_main)

    def place_settings(self, widget: tk.Widget) -> None:
        widget.pack(fill="both", expand=True, in_=self._page_settings)

    def ask_root_dir(self) -> Optional[Path]:
        path = filedialog.askdirectory(title="Select Root Directory (images in root; subfolders = categories)")
        return Path(path) if path else None

    def set_status(self, text: str) -> None:
        self._status.configure(text=text)

    def error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message)
