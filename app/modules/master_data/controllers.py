from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.master_data.services import MasterDataService
from app.utils.response import success_response, not_found, internal_error


router = APIRouter(prefix="/master-data", tags=["Master Data"])


# -------------------------------
# Get all master data
# -------------------------------
@router.get("/", summary="Get all master data")
async def get_all_master_data(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all master data in one call.
    """
    service = MasterDataService(db)
    try:
        data = await service.get_all_master_data()
        return success_response(data=data, message="All master data retrieved successfully.")
    except ValueError:
        return not_found(message="All master data types not found.")
    except Exception:
        return internal_error(message="Failed to fetch master data.")


# -------------------------------
# Get single master data type
# Example: /master-data/genders
# -------------------------------
@router.get("/{data_type}", summary="Get single master data type")
async def get_single_master_data(data_type: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single type of master data, e.g., genders, blood_types.
    The service maps the string to the right model+schema and returns JSON-safe dicts.
    """
    service = MasterDataService(db)
    try:
        data = await service.get_master_data_by_type(data_type)
        print (f"Fetched data for type {data_type}: {data}")
        return success_response(data=data, message=f"{data_type} retrieved successfully.")
    except ValueError:
        return not_found(message=f"Master data type '{data_type}' not found.")
    except Exception as e:
        return internal_error(message="Failed to fetch master data.: " + str(e))