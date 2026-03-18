from typing import Any
from ultralytics import YOLO
import cv2, numpy as np


DEBUG_COLOR = (0, 255, 0)
MODEL = YOLO("model.pt")


def recognize(image: np.ndarray, metadata: dict[str, Any]) -> list[list[int]]:
    results = MODEL.predict(image)

    dots_coords = results[0].boxes.xywh
    dots_classes = results[0].boxes.cls

    board = calculate_board(metadata, dots_coords, dots_classes)
    return board


def calculate_board(metadata: dict[str, Any], dots_positions, dots_classes):
    board = [[0 for col in range(0, 8)] for row in range(0, 8)]

    for row in range(0, 8):
        for col in range(0, 8):
            abs_pos = [
                row * metadata["CELL_SIZE"] + metadata["TOP_LEFT"][0],
                col * metadata["CELL_SIZE"] + metadata["TOP_LEFT"][1]
            ]

            for dot_id, dot_position in enumerate(dots_positions):
                dot = [
                    dot_position[0] - metadata["CELL_SIZE"] // 2,
                    dot_position[1] - metadata["CELL_SIZE"] // 2,
                    dot_position[2],
                    dot_position[3]
                ]

                if not is_mostly_overlapped(dot_position, [
                    metadata["TOP_LEFT"][0],
                    metadata["TOP_LEFT"][1],
                    metadata["CELL_SIZE"] * 8,
                    metadata["CELL_SIZE"] * 8
                ], 0.01):
                    continue
                if is_mostly_overlapped(dot, [
                    *abs_pos,
                    metadata["CELL_SIZE"],
                    metadata["CELL_SIZE"]
                ], 0.4):
                    board[col][row] = 1 if dots_classes[dot_id] > 6 else 2

    return board

def is_mostly_overlapped(rect1: list, rect2: list, threshold: float = 0.9) -> bool:
    """
    Определяет, перекрывает ли rect2 более threshold% площади rect1.

    Args:
        rect1: [x, y, width, height] — основной прямоугольник
        rect2: [x, y, width, height] — прямоугольник для сравнения
        threshold: порог перекрытия (по умолчанию 0.9 = 90%)

    Returns:
        True если rect2 покрывает >= threshold% площади rect1
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    r1_xmin, r1_ymin, r1_xmax, r1_ymax = x1, y1, x1 + w1, y1 + h1
    r2_xmin, r2_ymin, r2_xmax, r2_ymax = x2, y2, x2 + w2, y2 + h2

    inter_xmin = max(r1_xmin, r2_xmin)
    inter_ymin = max(r1_ymin, r2_ymin)
    inter_xmax = min(r1_xmax, r2_xmax)
    inter_ymax = min(r1_ymax, r2_ymax)

    inter_width = inter_xmax - inter_xmin
    inter_height = inter_ymax - inter_ymin

    if inter_width <= 0 or inter_height <= 0:
        return False

    intersection_area = inter_width * inter_height
    rect1_area = w1 * h1

    if rect1_area == 0:
        return False

    overlap_ratio = intersection_area / rect1_area

    # print(f"Площадь rect1:        {rect1_area}")
    # print(f"Площадь пересечения:  {intersection_area}")
    # print(f"Процент перекрытия:   {overlap_ratio * 100:.2f}%")

    return overlap_ratio >= threshold
