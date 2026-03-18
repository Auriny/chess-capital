import base64

class FrameException(Exception):
    def __init__(self, message):
        super().__init__(f"Frame Exception: {message}")

def decode_frame(frame: str) -> tuple[str, bytes]:
    lhr = frame.find(":", 0, len(frame))

    if lhr < 0 or lhr == len(frame) - 1:
        raise FrameException("Отсутствует тип изображения")

    rhs = frame.find(";", lhr + 1, len(frame))

    if rhs < 0:
        raise FrameException("Отсутствует тип изображения")

    image_type = frame[lhr + 1:rhs]

    oi = frame.find(",", 0, len(frame))
    if oi < 0:
        raise FrameException("Отсутствуют данные")

    result = base64.b64decode(frame[oi + 1:])

    return image_type, result

if __name__ == "__main__":
    test_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
    result = ('image/png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82')
    assert decode_frame(test_data) == result
