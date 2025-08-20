import tkinter as tk
from pathlib import Path
from PIL import Image
from image_categorizer.config import AppConfig
from image_categorizer.infrastructure import (
    ConsoleLogger,
    LocalFileSystem,
    PillowImageLoader,
    CategoryRepository,
    ImageRepository,
)
from image_categorizer.services import CategoryService, ImageService
from image_categorizer.ui import MainView, AppController
from image_categorizer.ui import theme

def main():
    cfg = AppConfig()
    root = tk.Tk()
    theme.apply_theme(root)
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
