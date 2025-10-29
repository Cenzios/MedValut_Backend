from fastapi import HTTPException

class AppException(HTTPException):
    """Custom application exception for consistent error handling."""
    def __init__(self, status_code: int = 400, message: str = "Something went wrong", data: dict = None):
        super().__init__(status_code=status_code, detail={"message": message, "data": data or {}})