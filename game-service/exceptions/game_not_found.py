from exceptions.base import CapitalChessBaseError


class GameNotFoundError(CapitalChessBaseError):
    """Exception raised when game is not found."""

    def __init__(self, active: bool, msg: str):  # noqa: ANN204 FBT001
        self.active = active
        self.message = msg
