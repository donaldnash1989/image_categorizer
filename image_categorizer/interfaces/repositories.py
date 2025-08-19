from abc import ABC, abstractmethod
from pathlib import Path

class ICategoryRepository(ABC):
    @abstractmethod
    def list_categories(self, root: Path) -> list[str]: ...
    @abstractmethod
    def add_category(self, root: Path, name: str) -> None: ...
    @abstractmethod
    def delete_category_if_empty(self, root: Path, name: str) -> bool: ...

class IImageRepository(ABC):
    @abstractmethod
    def list_images(self, root: Path) -> list[Path]: ...
