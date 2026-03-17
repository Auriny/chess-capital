import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from fastapi.testclient import TestClient
from anyio import Path

from main import app
from config import settings


def test_lifespan_creates_pgn_folder(tmp_path, monkeypatch):
    """
    При старте приложения lifespan должен создать settings.PGN_FILES_FOLDER,
    если папки нет.
    """
    test_folder = tmp_path / "pgn_files"
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(test_folder))

    assert not test_folder.exists()

    with TestClient(app) as client:
        # Во время жизни приложения папка должна появиться
        assert test_folder.exists()
        assert test_folder.is_dir()

    assert test_folder.exists()
