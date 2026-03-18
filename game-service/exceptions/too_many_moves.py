from exceptions.base import CapitalChessBaseError


class TooManyMovesError(CapitalChessBaseError):
    """Error class for lot of moves that API cannot process."""
