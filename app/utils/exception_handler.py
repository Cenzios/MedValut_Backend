from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import error_response, internal_error, not_found, bad_request

async def all_exception_handler(request: Request, exc: Exception):
    """
    Catch all unhandled exceptions
    """
    return internal_error(message=str(exc))

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Catch all HTTP exceptions
    """
    status = exc.status_code
    detail = exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "Error")
    
    if status == 404:
        return not_found(message=detail)
    elif status == 400:
        return bad_request(message=detail)
    else:
        return error_response(message=detail, status_code=status)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors
    """
    errors = exc.errors()
    return bad_request(message="Validation error", data=errors)