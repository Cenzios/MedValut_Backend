from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.modules.master_data.services import MasterDataService
from app.utils.response import success_response, not_found, internal_error
from app.modules.master_data.services import MODEL_SCHEMA_MAP  # for validation

router = APIRouter(prefix="/master-data", tags=["Master Data"])


@router.get("/all", summary="Get all master data")
async def get_all_master_data(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all master data at once.
    """
    service = MasterDataService(db)
    response = await service.get_all_master_data()
    return response  # service already returns a HTTP-ready response


@router.get(
    "/{data_type}",
    summary="Get single master data type",
)
async def get_single_master_data(
    data_type: str = Path(
        ...,
        description="Type of master data to retrieve",
        example="genders",
        regex="^[a-zA-Z_]+$",
    ),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Retrieve a single type of master data, e.g., genders, blood_types.
    Input is validated against allowed master data types.
    """
    allowed_types = MODEL_SCHEMA_MAP.keys()
    if data_type.lower() not in allowed_types:
        return not_found(message=f"Master data type '{data_type}' not found.")

    service = MasterDataService(db)
    response = await service.get_master_data_by_type(data_type)
    return response  # service already returns a HTTP-ready response