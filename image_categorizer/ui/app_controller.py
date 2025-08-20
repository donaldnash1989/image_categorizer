from pathlib import Path
from tkinter import messagebox
from ..interfaces.logger import ILogger
from ..interfaces.image_loader import IImageLoader
from ..interfaces.services import ICategoryService, IImageService
from ..interfaces.filesystem import IFileSystem
from ..commands import MoveImageCommand
from ..config import AppConfig
from ..exceptions import ImageLoadError
from .main_view import MainView
from .image_view import ImageView
from .button_panel import ButtonPanel
from .settings_view import SettingsView
from .collision_dialog import CollisionDialog
from . import theme


class AppController:
    def __init__(
        self,
        view: MainView,
        logger: ILogger,
        display_loader: IImageLoader,
        fast_loader: IImageLoader,
        cat_svc: ICategoryService,
        img_svc: IImageService,
        fs: IFileSystem,
        config: AppConfig,
        root_dir: Path,
    ):
        self._view = view
        self._logger = logger
        self._display_loader = display_loader
        self._fast_loader = fast_loader
        self._cat_svc = cat_svc
        self._img_svc = img_svc
        self._fs = fs
        self._cfg = config
        self._root = root_dir

        # Pre-Load
        img_view = ImageView(view._page_main, display_loader, config)
        btn_panel = ButtonPanel(
            view._page_main, self._on_category_clicked, config, on_delete=self._on_delete_clicked
        )
        view.build_main(img_view, btn_panel)

        # Settings
        settings = SettingsView(view._page_settings, self._cat_svc, self._cfg, on_changed=self._refresh_categories)
        view.place_settings(settings)

        self._apply_theme()

        # On Load
        self._refresh_categories()
        self._post_load(initial=True)

    def _apply_theme(self, name: str | None = None) -> None:
        """Apply the global theme and update child widgets."""
        theme.apply_theme(self._view._root, name)
        self._view.button_panel.apply_theme()

    def _on_delete_clicked(self):
        path = self._img_svc.current_image()
        if not path:
            return
        if messagebox.askyesno("Delete image", f"Are you sure you would like to delete the image named <{path.name}>?"):
            self._img_svc.delete_current()
            self._post_load()

    def _on_category_clicked(self, name: str) -> None:
        src = self._img_svc.current_image()
        if not src:
            return
        target = self._root / name / src.name
        if self._fs.exists(target):
            if self._cfg.auto_resolve_conflicts:
                self._img_svc.delete_current()
            else:
                decision = CollisionDialog.prompt(self._view._root, self._fast_loader, src, target)
                if decision.action == "keep_source":
                    self._fs.delete_file(target)
                    self._img_svc.move_current_to_category(name)
                elif decision.action == "keep_target":
                    self._img_svc.delete_current()
                elif decision.action == "rename":
                    self._img_svc.move_current_to_category_as(name, decision.new_name)
                else:
                    return
        else:
            cmd = MoveImageCommand(self._img_svc, name)
            cmd.execute()
        self._post_load()

    def _refresh_categories(self) -> None:
        cats = self._cat_svc.get_categories()
        self._view.button_panel.set_categories(cats)

    def _post_load(self, initial: bool = False) -> None:
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
            self._view.error("Image Load Error", str(ex))

        self._view.set_remaining_count(self._img_svc.count_images())
