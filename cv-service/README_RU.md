[[EN version]](README.md)

# Computer Vision Service

## Цель

Анализ позиции на доске и отправка и отправка для дальнейшей обработки

## Предварительные требования

Установите uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Закрепите версию python 3.11.14 и установите зависимости
```bash
uv python pin 3.11.14
uv venv
uv sync
```

Скачайте модель с HuggingFace в эту директорию
```bash
wget -O model.pt "https://huggingface.co/surawut/chess-move-tracking-yolo11/resolve/main/models/yolo11m_pieces.pt"
```

Задайте порт сервиса игры. Пример:
```
GAME_PORT = 8080
```

## Запуск сервиса

Просто запустите эту команду
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8081 # change port if necessary
```

Если хотите запустить процесс в фоне - просто добавьте флаг `-D` либо `--daemon` в команду
