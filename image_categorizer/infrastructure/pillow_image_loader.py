from pathlib import Path
from typing import Tuple
from PIL import Image
from ..interfaces.image_loader import IImageLoader

# Pillow 10 moved resampling filters under Image.Resampling.  Fall back to the
# old module-level constants when unavailable.
if hasattr(Image, "Resampling"):
    DEFAULT_RESAMPLE = Image.Resampling.BILINEAR
elif hasattr(Image, "BILINEAR"):
    DEFAULT_RESAMPLE = Image.BILINEAR
else:  # numeric value for BILINEAR used by Pillow
    DEFAULT_RESAMPLE = 2


class PillowImageLoader(IImageLoader):
    """Load images and resize them while preserving aspect ratio.

    The loader defaults to :pydata:`PIL.Image.BILINEAR` for a balance between
    quality and performance.  Higher quality filters such as
    :pydata:`PIL.Image.LANCZOS` can be selected at the cost of slower
    processing, while :pydata:`PIL.Image.NEAREST` is faster but produces
    noticeably lower quality results.

    Parameters
    ----------
    resample : int, optional
        Resampling filter from ``PIL.Image``. Defaults to ``Image.BILINEAR``.
    """

    def __init__(self, resample: int = DEFAULT_RESAMPLE):
        self._resample = resample

    def load_and_fit(self, path: Path, target_size: Tuple[int, int]):
        with Image.open(path) as img:
            img = img.convert("RGBA")
            tw, th = target_size
            if tw <= 0 or th <= 0:
                return img
            iw, ih = img.size
            scale = min(tw / iw, th / ih)
            new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
            return img.resize(new_size, self._resample)
