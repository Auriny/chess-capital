[[EN version]](https://github.com/Auriny/chess-capital/blob/master/README.md)
# ChessCapital
Проект для хакатона, сочетающий в себе компьютерное зрение и валидацию шахматной доски.

Система распознаёт физическую шахматную доску с камеры телефона, считывает позиции фигур в реальном времени, преобразует доску в матричное представление и проверяет корректность ходов по правилам шахмат.

---

## Обзор
Проект работает по архитектуре микросервисов:
- **cv-service** - компьютерное зрение
- **game-service** - backend-логика приложения
- **frontend** - лёгкий клиентский интерфейс
<img width="2400" height="1021" alt="chess2" src="https://github.com/user-attachments/assets/a3775718-4c60-4bd1-97cf-44c869a90aa1" />

---

## Возможности
- Распознавание шахматной доски с камеры в реальном времени
- Определение фигур с использованием YOLO/OpenCV
- Преобразование состояния доски в матрицу 8x8
- Проверка ходов по правилам шахмат
- Обнаружение невозможных ходов
- Микросервисная архитектура
- REST API-взаимодействие между сервисами
- Поддержка стримов VK видео
<img width="500" height="500" alt="chess" src="https://github.com/user-attachments/assets/ba71ffa0-f9b3-48bd-bb9a-4c15468183d4" />

---

## Стек технологий
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

## Установка
### Клонирование репозитория
```bash
git clone <repo-url>
cd ChessCapital
```

### Запуск game-service
https://github.com/Auriny/chess-capital/blob/main/game-service/README_RU.md

### Запуск cv-service
https://github.com/Auriny/chess-capital/blob/main/cv-service/README_RU.md

### Запуск фронтенда 
Чтобы запустить фронтенд, поместите папку на ваш сервер и используйте `nginx`, `python http-server` или любой другой веб-сервер.

Для примера используем `python http-server`:
```bash
cd frontend
python -m http.server 5173
```

---

## Примечание!
Это хакатон-проект, сделанный всего за неделю, поэтому из-за сжатых сроков в разработке могут встречаться нестандартные решения и архитектурные изъяны.

Спасибо за понимание.
