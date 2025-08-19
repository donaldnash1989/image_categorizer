from pathlib import Path
from typing import Tuple
from PIL import Image
from ..interfaces.image_loader import IImageLoader

class PillowImageLoader(IImageLoader):
    def load_and_fit(self, path: Path, target_size: Tuple[int, int]):
        with Image.open(path) as img:
            img = img.convert("RGBA")
            tw, th = target_size
            if tw <= 0 or th <= 0:
                return img
            iw, ih = img.size
            scale = min(tw/iw, th/ih)
            new_size = (max(1, int(iw*scale)), max(1, int(ih*scale)))
            return img.resize(new_size, Image.LANCZOS)
