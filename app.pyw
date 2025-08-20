import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image
from image_categorizer.config import AppConfig
from image_categorizer.preferences import load_preferences, Preferences
from image_categorizer.infrastructure import (
    ConsoleLogger,
    LocalFileSystem,
    PillowImageLoader,
    CategoryRepository,
    ImageRepository,
)
from image_categorizer.services import CategoryService, ImageService
from image_categorizer.ui import MainView, AppController

def _apply_theme(root: tk.Tk, theme: str) -> None:
    style = ttk.Style(root)
    if theme == "dark":
        style.theme_use("clam")
        style.configure(".", background="#333333", foreground="white")
        root.configure(bg="#333333")
    elif theme == "light":
        style.theme_use("clam")
        style.configure(".", background="#f0f0f0", foreground="black")
        root.configure(bg="#f0f0f0")


def main():
    prefs: Preferences = load_preferences()
    cfg = AppConfig(theme=prefs.theme)
    root = tk.Tk()
    _apply_theme(root, cfg.theme)
    view = MainView(root, cfg)

    chosen = view.ask_root_dir()
    if not chosen:
        root.destroy()
        return
    root_dir = Path(chosen)

    logger = ConsoleLogger()
    fs = LocalFileSystem()
    display_loader = PillowImageLoader(resample=Image.LANCZOS)
    fast_loader = PillowImageLoader(resample=Image.NEAREST)
    cat_repo = CategoryRepository(fs, logger)
    img_repo = ImageRepository(fs, logger)
    cat_svc = CategoryService(root_dir, cat_repo, fs, logger)
    img_svc = ImageService(root_dir, img_repo, fs, logger)

    AppController(view, logger, display_loader, fast_loader, cat_svc, img_svc, fs, cfg, root_dir)
    root.mainloop()

if __name__ == "__main__":
    main()
