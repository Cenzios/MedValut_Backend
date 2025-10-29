from fastapi import Response
from fastapi.responses import JSONResponse
from typing import Any, Optional

# -----------------------------------
# Standard Success Response
# -----------------------------------
def success_response(
    data: Any = None,
    message: str = "Request successful.",
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data or [],
            "statusCode": status_code,
        },
    )

# -----------------------------------
# Standard Error Response
# -----------------------------------
def error_response(
    message: str = "Something went wrong.",
    status_code: int = 500,
    data: Optional[Any] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": data or [],
            "statusCode": status_code,
        },
    )

# -----------------------------------
# Shortcut methods for common codes
# -----------------------------------
def bad_request(message: str = "Bad Request", data: Optional[Any] = None):
    return error_response(message, 400, data)

def unauthorized(message: str = "Unauthorized", data: Optional[Any] = None):
    return error_response(message, 401, data)

def forbidden(message: str = "Forbidden", data: Optional[Any] = None):
    return error_response(message, 403, data)

def not_found(message: str = "Not Found", data: Optional[Any] = None):
    return error_response(message, 404, data)

def force_update(message: str = "Force update", data: Optional[Any] = None):
    return error_response(message, 426, data)

def internal_error(message: str = "Internal Server Error", data: Optional[Any] = None):
    return error_response(message, 500, data)