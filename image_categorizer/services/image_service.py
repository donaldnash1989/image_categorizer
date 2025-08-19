from pathlib import Path
from typing import Optional
from ..interfaces.services import IImageService
from ..interfaces.repositories import IImageRepository
from ..interfaces.filesystem import IFileSystem
from ..interfaces.logger import ILogger

class ImageService(IImageService):
    def __init__(self, root: Path, repo: IImageRepository, fs: IFileSystem, logger: ILogger):
        self._root = root
        self._repo = repo
        self._fs = fs
        self._logger = logger
        self._current: Optional[Path] = None

    def _refresh_current(self):
        images = self._repo.list_images(self._root)
        self._current = images[0] if images else None

    def has_images(self) -> bool:
        self._refresh_current()
        return self._current is not None

    def current_image(self) -> Optional[Path]:
        self._refresh_current()
        return self._current

    def advance_to_first(self) -> None:
        self._refresh_current()

    def move_current_to_category(self, category: str) -> None:
        self._refresh_current()
        if not self._current:
            return
        target = self._root / category / self._current.name
        self._fs.move(self._current, target)
        self._logger.info(f"Moved {self._current.name} -> {category}")
        self._refresh_current()
