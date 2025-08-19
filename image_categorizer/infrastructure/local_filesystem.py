from pathlib import Path
import shutil
from ..interfaces.filesystem import IFileSystem

class LocalFileSystem(IFileSystem):
    def list_dirs(self, root: Path) -> list[Path]:
        return sorted([p for p in root.iterdir() if p.is_dir()])
    def list_files(self, root: Path) -> list[Path]:
        return sorted([p for p in root.iterdir() if p.is_file()])
    def create_dir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
    def delete_dir_if_empty(self, path: Path) -> bool:
        try:
            if not path.exists(): 
                return True
            if any(path.iterdir()):
                return False
            path.rmdir()
            return True
        except Exception:
            return False
    def move(self, src: Path, dst: Path) -> None:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    def exists(self, path: Path) -> bool:
        return path.exists()
