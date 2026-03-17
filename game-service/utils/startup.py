from pathlib import Path

from config import settings


def check_pgn_folder() -> None:
    folder = Path(settings.PGN_FILES_FOLDER)
    if folder.exists():
        return
    folder.mkdir()
