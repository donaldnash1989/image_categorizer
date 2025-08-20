import sys
from pathlib import Path
import types

# Ensure package root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Provide dummy PIL modules so imports succeed without pillow installed
sys.modules.setdefault("PIL", types.ModuleType("PIL"))
sys.modules.setdefault("PIL.Image", types.ModuleType("Image"))
sys.modules.setdefault("PIL.ImageTk", types.ModuleType("ImageTk"))

from image_categorizer.ui.app_controller import AppController
from image_categorizer.config import AppConfig


class DummyImageService:
    def __init__(self):
        self.deleted = False
        self.moved = []

    def current_image(self):
        return Path("src.jpg")

    def delete_current(self):
        self.deleted = True

    def move_current_to_category(self, name):
        self.moved.append((name, None))

    def move_current_to_category_as(self, name, new_name):
        self.moved.append((name, new_name))


class DummyFS:
    def __init__(self, exists_return):
        self.exists_return = exists_return
        self.deleted_files = []

    def exists(self, path):
        return self.exists_return

    def delete_file(self, path):
        self.deleted_files.append(path)


class DummyView:
    def __init__(self):
        self._root = None


def build_controller(fs, cfg, img_svc):
    controller = AppController.__new__(AppController)
    controller._view = DummyView()
    controller._logger = None
    controller._display_loader = None
    controller._fast_loader = None
    controller._cat_svc = None
    controller._img_svc = img_svc
    controller._fs = fs
    controller._cfg = cfg
    controller._root = Path("/root")
    controller._post_load = lambda *args, **kwargs: None
    return controller


def test_auto_resolve_deletes_source(monkeypatch):
    img_svc = DummyImageService()
    fs = DummyFS(exists_return=True)
    cfg = AppConfig(auto_resolve_conflicts=True)
    ctl = build_controller(fs, cfg, img_svc)
    ctl._on_category_clicked("cats")
    assert img_svc.deleted is True
    assert img_svc.moved == []


def test_collision_dialog_invoked_when_disabled(monkeypatch):
    calls = []

    def fake_prompt(parent, loader, src, target):
        calls.append((parent, loader, src, target))

        class D:
            action = "cancel"
            new_name = None

        return D()

    from image_categorizer.ui import app_controller as ac
    monkeypatch.setattr(ac.CollisionDialog, "prompt", fake_prompt)

    img_svc = DummyImageService()
    fs = DummyFS(exists_return=True)
    cfg = AppConfig(auto_resolve_conflicts=False)
    ctl = build_controller(fs, cfg, img_svc)
    ctl._on_category_clicked("cats")
    assert calls
    assert img_svc.deleted is False
