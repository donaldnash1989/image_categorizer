import sys
from pathlib import Path

# Ensure the package root is on the path when running tests directly.
sys.path.append(str(Path(__file__).resolve().parents[1]))

import types
sys.modules.setdefault("PIL", types.ModuleType("PIL"))
sys.modules.setdefault("PIL.Image", types.ModuleType("Image"))
sys.modules.setdefault("PIL.ImageTk", types.ModuleType("ImageTk"))

from image_categorizer.infrastructure import LocalFileSystem, CategoryRepository, ConsoleLogger
from image_categorizer.services import CategoryService


def test_delete_nonexistent_category_returns_false(tmp_path, capsys):
    logger = ConsoleLogger()
    fs = LocalFileSystem()
    repo = CategoryRepository(fs, logger)
    svc = CategoryService(tmp_path, repo, fs, logger)

    result = svc.delete_category("missing")

    out = capsys.readouterr().out
    assert "Category not found: missing" in out
    assert result is False
