[[RU version]](README_RU.md)

# Computer Vision Service

## Goals

Analysis of the position on the board and sending for processing

## Pre-requirements

Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Set python version to 3.11.14 and install dependencies
```bash
uv python pin 3.11.14
uv venv
uv sync
```

Download model from HuggingFace to this folder
```bash
wget -O model.pt "https://huggingface.co/surawut/chess-move-tracking-yolo11/resolve/main/models/yolo11m_pieces.pt"
```

Set the port of game-service. Example:
```
GAME_PORT = 8080
```

## Start Service

Just run this command
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8081 # change port if necessary
```

If you want to start as daemon just add `-D` or `--daemon` in command
