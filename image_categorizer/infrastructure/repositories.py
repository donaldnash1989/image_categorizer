from pathlib import Path
from ..interfaces.repositories import ICategoryRepository, IImageRepository
from ..interfaces.filesystem import IFileSystem
from ..interfaces.logger import ILogger
from ..config import SUPPORTED_EXTENSIONS

class CategoryRepository(ICategoryRepository):
    def __init__(self, fs: IFileSystem, logger: ILogger):
        self._fs = fs
        self._logger = logger

    def list_categories(self, root: Path) -> list[str]:
        return [d.name for d in self._fs.list_dirs(root)]

    def add_category(self, root: Path, name: str) -> None:
        self._fs.create_dir(root / name)
        self._logger.info(f"Category created: {name}")

    def delete_category_if_empty(self, root: Path, name: str) -> bool:
        ok = self._fs.delete_dir_if_empty(root / name)
        if ok:
            self._logger.info(f"Category deleted: {name}")
        else:
            self._logger.warn(f"Cannot delete non-empty category: {name}")
        return ok

class ImageRepository(IImageRepository):
    def __init__(self, fs: IFileSystem, logger: ILogger):
        self._fs = fs
        self._logger = logger

    def list_images(self, root: Path) -> list[Path]:
        return [p for p in self._fs.list_files(root) if p.suffix.lower() in SUPPORTED_EXTENSIONS]
