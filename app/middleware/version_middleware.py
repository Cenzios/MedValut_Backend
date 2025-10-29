from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.future import select
from app.core.database import get_sessionmaker
from app.seed.models import AppVersion
from app.utils.response import error_response, force_update, not_found

class VersionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check app version headers: 'app_type' and 'build_number'.
    Skips specific paths like '/', '/health_check', '/api/v1/', '/api/v1/health_check'.
    """

    SKIP_PATHS = [
        "/",
        "/health_check",
        "/api/v1/",
        "/api/v1/health_check",
        "/api/health/check",
        "/master_data",
    ]

    async def dispatch(self, request: Request, call_next):
            # Skip version check for certain routes
            if request.url.path in self.SKIP_PATHS:
                return await call_next(request)

            app_type = request.headers.get("app_type")
            build_number = request.headers.get("build_number")

            if not app_type or not build_number:
                return error_response(
                    message="Missing app_type or build_number headers",
                    status_code=400
                )

            try:
                build_number = int(build_number)
            except ValueError:
                return error_response(
                    message="Invalid build_number header, must be integer",
                    status_code=400
                )

            # Check DB for current active version
            Session = get_sessionmaker()
            async with Session() as session:
                stmt = select(AppVersion).where(AppVersion.app_type == app_type)
                result = await session.execute(stmt)
                app_version = result.scalars().first()

                if not app_version:
                    return force_update(
                        message=f"No version info found for app_type '{app_type}'",
                        status_code=426
                    )

                if build_number < app_version.build_number:
                    # Force update
                    return force_update(
                        message=f"Please update your {app_type} app to the latest version",
                        status_code=426
                    )

            # Proceed to next middleware / route
            return await call_next(request)
