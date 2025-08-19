from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

class IImageLoader(ABC):
    @abstractmethod
    def load_and_fit(self, path: Path, target_size: Tuple[int, int]):
        """Return a PIL.Image resized to fit target_size while preserving aspect ratio."""
        ...
