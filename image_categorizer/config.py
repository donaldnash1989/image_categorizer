from dataclasses import dataclass
from typing import Tuple

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

@dataclass(frozen=True)
class UiConfig:
    min_window_size: Tuple[int, int] = (900, 700)
    buttons_per_row: int = 5
    button_padx: int = 4
    button_pady: int = 4
    image_bg: str = "#111111"

@dataclass
class AppConfig:
    ui: UiConfig = UiConfig()
    auto_resolve_conflicts: bool = False
