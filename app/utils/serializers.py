from typing import Any
from sqlalchemy.orm import DeclarativeMeta

def model_to_dict(obj: Any) -> dict:
    """
    Convert a SQLAlchemy model instance to a plain dict,
    only including actual column attributes.
    """
    # handle None
    if obj is None:
        return {}

    # for mapped classes
    mapper = getattr(obj.__class__, "__table__", None)
    if mapper is None:
        # fallback: try __dict__ but filter private attrs
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}

    return {col.name: getattr(obj, col.name) for col in obj.__table__.columns}