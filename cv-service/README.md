# Как запускать...
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
### А ни как 
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
## Ладно, расскажу

### Для начала нужно достать модель
```
https://huggingface.co/surawut/chess-move-tracking-yolo11/resolve/main/models/yolo11m_pieces.pt?download=true
```

### Дальше её надо перекинуть в корень папки с сервисом и переименовать в model.pt

### Установи uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Укажи конкретную версию
```text
uv python pin 3.11.14
```

### Установи зависимости

```bash
uv venv
uv sync
```

### Укажи порт сервиса игры
```text
GAME_PORT = 8080
```

### Запускать с помощью команды

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8081 # Тут порт заменить на нужный при необходимости
```

При желании, можно запустить его как сервис если добавить аргумент -D/--daemon в строку запуска

<sub><sup><sub><sup><sub><sup><sub><sup>42 БРАТУХА 42 42 42 42</sub></sup></sub></sup></sub></sup></sub></sup>
