[[RU version]](https://github.com/Auriny/chess-capital/blob/master/README_RU.md)
# ChessCapital
A hackathon project that combines computer vision and chess game validation.

The system detects a physical chessboard from a phone camera, recognizes piece positions in real time, converts the board into a matrix representation, and validates moves using chess rules.

---

## Overview
The project works as a multi-service application:
- **cv-service** - computer-vision
- **game-service** - backend logic of the app
- **frontend** - lightweight client interface
<img width="2400" height="1021" alt="chess2" src="https://github.com/user-attachments/assets/a3775718-4c60-4bd1-97cf-44c869a90aa1" />

---

## Features
- Chessboard recognition from camera frames
- Piece detection using YOLO/OpenCV
- Conversion of board state into an 8x8 matrix
- Move validation based on chess rules
- Illegal move detection
- Multi-service architecture
- REST API communication between services
- Vk video streams support
<img width="500" height="500" alt="chess" src="https://github.com/user-attachments/assets/ba71ffa0-f9b3-48bd-bb9a-4c15468183d4" />

---

## Tech Stack
### CV Service
- Python
- FastAPI
- OpenCV
- Ultralytics YOLOv11
- NumPy
### Game Service
- Python
- FastAPI
- python-chess
### Frontend
- HTML/CSS/JavaScript
- Tailwind
- chess.js

<img width="1001" height="318" alt="image" src="https://github.com/user-attachments/assets/7076ba73-8b3f-4899-a3b3-68406c19b70e" />

---

## Installation
### Clone repository
```bash
git clone <repo-url>
cd ChessCapital
```

### Start game-service
https://github.com/Auriny/chess-capital/blob/main/game-service/README.md

### Start cv-service
https://github.com/Auriny/chess-capital/blob/main/cv-service/README.md

### Start frontend
To start frontend, put the `frontend` folder on your server and use nginx, python htpp-server or anything else.

For example, we're using Python http-server here: 
```bash
cd frontend
python -m http.server 5173
```

---

## Note!
This is a hackaton project, so there might be some interesting solutions and architectury strangenesses due to lack of time for developing. 

Thanks for understanding.
