import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from pathlib import Path
from typing import Optional
from ..interfaces.image_loader import IImageLoader
from ..config import AppConfig
from ..exceptions import ImageLoadError

class ImageView(ttk.Frame):
    def __init__(self, parent, image_loader: IImageLoader, config: AppConfig):
        super().__init__(parent)
        self._image_loader = image_loader
        self._config = config
        self._canvas = tk.Canvas(self, bg=self._config.ui.image_bg, highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)
        self._current_photo: Optional[ImageTk.PhotoImage] = None
        self._current_path: Optional[Path] = None
        self.bind("<Configure>", lambda e: self._redraw())

    def show_image(self, path: Optional[Path]) -> None:
        self._current_path = path
        self._redraw()

    def _redraw(self) -> None:
        self._canvas.delete("all")
        if not self._current_path:
            return
        w = max(1, self.winfo_width())
        h = max(1, self.winfo_height())
        try:
            pil_img = self._image_loader.load_and_fit(self._current_path, (w, h))
        except Exception as ex:
            raise ImageLoadError(str(ex))
        self._current_photo = ImageTk.PhotoImage(pil_img)
        iw, ih = self._current_photo.width(), self._current_photo.height()
        x = (w - iw) // 2
        y = (h - ih) // 2
        self._canvas.create_image(x, y, anchor="nw", image=self._current_photo)
