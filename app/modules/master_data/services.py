# app/modules/master_data/services.py
from typing import List, Dict, Tuple, Type
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.seed.models import (
    Gender, BloodType, UnitType, SmokingLevel, AlcoholLevel, ExerciseLevel,
    MedicalConditionSuggestion, Allergy, GeneticCondition, AppVersion, SubscriptionPlan
)
from app.modules.master_data.schemas import (
    GenderSchema, BloodTypeSchema, UnitTypeSchema, SmokingLevelSchema, AlcoholLevelSchema,
    ExerciseLevelSchema, MedicalConditionSuggestionSchema, AllergySchema, GeneticConditionSchema,
    AppVersionSchema, SubscriptionPlanSchema
)
from app.utils.logger import log_error, log_info

# mapping: "request path name" -> (ORM model, Pydantic schema)
MODEL_SCHEMA_MAP: Dict[str, Tuple[Type, Type]] = {
    "genders": (Gender, GenderSchema),
    "blood_types": (BloodType, BloodTypeSchema),
    "unit_types": (UnitType, UnitTypeSchema),
    "smoking_levels": (SmokingLevel, SmokingLevelSchema),
    "alcohol_levels": (AlcoholLevel, AlcoholLevelSchema),
    "exercise_levels": (ExerciseLevel, ExerciseLevelSchema),
    "medical_conditions_suggestions": (MedicalConditionSuggestion, MedicalConditionSuggestionSchema),
    "allergies": (Allergy, AllergySchema),
    "genetic_conditions": (GeneticCondition, GeneticConditionSchema),
    "app_versions": (AppVersion, AppVersionSchema),
    "subscription_plans": (SubscriptionPlan, SubscriptionPlanSchema),
}


class MasterDataService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_master_data(self) -> Dict[str, List[dict]]:
        """
        Fetch all master tables and return JSON-safe dicts.
        """
        out: Dict[str, List[dict]] = {}
        try:
            log_info("Fetching all master data")
            for key, (model_cls, schema_cls) in MODEL_SCHEMA_MAP.items():
                rows = (await self.db.execute(select(model_cls))).scalars().all()
                # from_orm + model_dump -> pydantic v2 serialization
                out[key] = [schema_cls.from_orm(r).model_dump() for r in rows]
            log_info("Fetched all master data successfully")
            return out
        except Exception as e:
            log_error(f"Failed fetching all master data: {e}")
            raise

    async def get_master_data_by_type(self, data_type: str) -> List[dict]:
        """
        data_type: e.g. 'genders', 'blood_types'
        Returns JSON-serializable list of dicts.
        Raises ValueError if unknown data_type.
        """
        key = data_type.lower()
        try:
            log_info(f"Requested master data for type: {key}")

            if key not in MODEL_SCHEMA_MAP:
                raise ValueError(f"Unsupported master data type: '{data_type}'")

            model_cls, schema_cls = MODEL_SCHEMA_MAP[key]
            rows = (await self.db.execute(select(model_cls))).scalars().all()
            result = [schema_cls.from_orm(r).model_dump() for r in rows]
            log_info(f"Fetched {len(result)} rows for {key}")
            return result

        except ValueError:
            # re-raise to let controller map to 404/not_found
            raise
        except Exception as e:
            log_error(f"Error fetching master data for {data_type}: {e}")
            raise