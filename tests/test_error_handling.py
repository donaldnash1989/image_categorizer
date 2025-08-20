from pathlib import Path
import sys
import types

# Provide dummy PIL modules so imports succeed without pillow installed
sys.modules.setdefault("PIL", types.ModuleType("PIL"))
sys.modules.setdefault("PIL.Image", types.ModuleType("Image"))
sys.modules.setdefault("PIL.ImageTk", types.ModuleType("ImageTk"))

from image_categorizer.ui.app_controller import AppController
from image_categorizer.exceptions import ImageLoadError

class DummyImageView:
    def show_image(self, path):
        raise ImageLoadError("boom")

class DummyButtonPanel:
    def __init__(self):
        self.enabled = None
    def set_enabled(self, value):
        self.enabled = value

class DummyView:
    def __init__(self):
        self.image_view = DummyImageView()
        self.button_panel = DummyButtonPanel()
        self.error_called = []
        self.status = None
        self.remaining = None
    def set_status(self, text):
        self.status = text
    def error(self, title, message):
        self.error_called.append((title, message))
    def set_remaining_count(self, n):
        self.remaining = n

class DummyImageService:
    def advance_to_first(self):
        pass
    def current_image(self):
        return Path("foo.jpg")
    def count_images(self):
        return 0

class DummyLogger:
    def __init__(self):
        self.messages = []
    def error(self, msg):
        self.messages.append(msg)


def test_post_load_shows_error_dialog():
    controller = AppController.__new__(AppController)
    controller._view = DummyView()
    controller._logger = DummyLogger()
    controller._img_svc = DummyImageService()
    controller._cat_svc = None
    controller._image_loader = None
    controller._fs = None
    controller._cfg = None
    controller._root = None
    controller._post_load()
    assert controller._view.button_panel.enabled is False
    assert controller._view.error_called == [("Image Load Error", "boom")]
    assert controller._view.status == "Failed to load image; buttons disabled."
