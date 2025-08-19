from pathlib import Path
from ..interfaces.logger import ILogger
from ..interfaces.image_loader import IImageLoader
from ..interfaces.services import ICategoryService, IImageService
from ..commands import MoveImageCommand
from ..config import AppConfig
from ..exceptions import ImageLoadError
from .main_view import MainView
from .image_view import ImageView
from .button_panel import ButtonPanel
from .settings_view import SettingsView

class AppController:
    def __init__(self, view: MainView, logger: ILogger, image_loader: IImageLoader,
                 cat_svc: ICategoryService, img_svc: IImageService, config: AppConfig, root_dir: Path):
        self._view = view
        self._logger = logger
        self._image_loader = image_loader
        self._cat_svc = cat_svc
        self._img_svc = img_svc
        self._cfg = config
        self._root = root_dir

        # Pre-Load: Build UI scaffold
        img_view = ImageView(view._page_main, image_loader, config)
        btn_panel = ButtonPanel(view._page_main, self._on_category_clicked, config)
        view.build_main(img_view, btn_panel)

        # Settings tab
        settings = SettingsView(view._page_settings, self._cat_svc, self._cfg, on_changed=self._refresh_categories)
        view.place_settings(settings)

        # On Load
        self._refresh_categories()
        self._post_load()

    def _on_category_clicked(self, name: str) -> None:
        cmd = MoveImageCommand(self._img_svc, name)
        cmd.execute()
        self._post_load()

    def _refresh_categories(self) -> None:
        cats = self._cat_svc.get_categories()
        self._view.button_panel.set_categories(cats)

    def _post_load(self) -> None:
        self._img_svc.advance_to_first()
        path = self._img_svc.current_image()
        has_img = path is not None
        try:
            self._view.image_view.show_image(path)
            self._view.button_panel.set_enabled(has_img)
            if has_img:
                self._view.set_status(f"Loaded: {path.name}")
            else:
                self._view.set_status("No images in root directory.")
        except ImageLoadError as ex:
            self._logger.error(str(ex))
            self._view.set_status("Failed to load image; buttons disabled.")
            self._view.button_panel.set_enabled(False)
