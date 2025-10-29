from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import log_info, log_error
import time
import json

class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            body = await request.body()
            response = await call_next(request)
            process_time = time.time() - start_time

            log_info(json.dumps({
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s",
                "request_body": body.decode("utf-8") if body else None,
            }))

            return response

        except Exception as e:
            log_error(f"HTTP Error: {str(e)}")
            raise e