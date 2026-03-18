import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from pydantic_settings import BaseSettings, SettingsConfigDict
from config import Settings


def test_settings_reads_env(monkeypatch, tmp_path):
    """
    Проверяем, что Settings читает PGN_FILES_FOLDER из .env.
    """
    # Создаём временный .env
    env_file = tmp_path / ".env"
    env_file.write_text("PGN_FILES_FOLDER=/tmp/pgn_from_env\n", encoding="utf-8")

    # Инстанциируем Settings, указав _env_file ЯВНО [web:206][web:212]
    test_settings = Settings(_env_file=str(env_file), _env_file_encoding="utf-8")

    assert test_settings.PGN_FILES_FOLDER == "/tmp/pgn_from_env"


def test_settings_reads_os_environ(monkeypatch):
    """
    Проверяем, что переменные окружения перекрывают .env.
    """
    # Подменяем переменную окружения
    monkeypatch.setenv("PGN_FILES_FOLDER", "/tmp/pgn_from_env_var")

    test_settings = Settings()  # использует env + .env, env важнее [web:206][web:208]

    assert test_settings.PGN_FILES_FOLDER == "/tmp/pgn_from_env_var"