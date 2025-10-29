from datetime import datetime, timezone
from sqlalchemy import insert
from app.core.database import get_sessionmaker
from app.seed.models import ActionLog
from app.utils.logger import log_info, log_error

async def log_action(user_id: int, action: str, details: dict = None):
    """
    Logs user action to file and database table 'action_logs'
    """
    timestamp = datetime.now(timezone.utc)
    entry = {
        "timestamp": timestamp.isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details or {}
    }

    # Log to file
    log_info(f"ACTION: {entry}")

    # Log to database
    try:
        Session = get_sessionmaker()
        async with Session() as session:
            async with session.begin():
                stmt = insert(ActionLog).values(
                    user_id=user_id,
                    action_name=action,
                    details=details or {},
                    created_at=timestamp
                )
                await session.execute(stmt)

    except Exception as e:
        log_error(f"Failed to log action for user_id={user_id}, action={action}: {e}")