from typing import Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


def model_to_dict(obj: Any) -> dict:
    """
    Convert a SQLAlchemy model instance to a plain dict,
    only including actual column attributes.
    Handles datetime, date, Decimal, and UUID serialization.
    """
    # handle None
    if obj is None:
        return {}

    # for mapped classes
    mapper = getattr(obj.__class__, "__table__", None)
    if mapper is None:
        # fallback: try __dict__ but filter private attrs
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}

    result = {}
    for col in obj.__table__.columns:
        value = getattr(obj, col.name)
        
        # Convert non-JSON-serializable types
        if isinstance(value, datetime):
            result[col.name] = value.isoformat()
        elif isinstance(value, date):
            result[col.name] = value.isoformat()
        elif isinstance(value, Decimal):
            result[col.name] = float(value)
        elif isinstance(value, UUID):
            result[col.name] = str(value)
        elif isinstance(value, bytes):
            result[col.name] = value.hex()  # or base64.b64encode(value).decode()
        else:
            result[col.name] = value
    
    return result