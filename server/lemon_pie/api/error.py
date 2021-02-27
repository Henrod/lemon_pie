from typing import Dict, NewType, Tuple

ErrorResponse = NewType("ErrorResponse", Tuple[Dict[str, str], int])


def error_response(e: str, status: int) -> ErrorResponse:
    return ErrorResponse(({"error": e}, status))
