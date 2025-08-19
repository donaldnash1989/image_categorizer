from pathlib import Path
from ..interfaces.services import ICategoryService
from ..interfaces.repositories import ICategoryRepository
from ..interfaces.filesystem import IFileSystem
from ..interfaces.logger import ILogger

class CategoryService(ICategoryService):
    def __init__(self, root: Path, repo: ICategoryRepository, fs: IFileSystem, logger: ILogger):
        self._root = root
        self._repo = repo
        self._fs = fs
        self._logger = logger

    def get_categories(self) -> list[str]:
        return self._repo.list_categories(self._root)

    def add_category(self, name: str) -> None:
        name = name.strip()
        if not name:
            return
        self._repo.add_category(self._root, name)

    def delete_category(self, name: str) -> bool:
        return self._repo.delete_category_if_empty(self._root, name)
