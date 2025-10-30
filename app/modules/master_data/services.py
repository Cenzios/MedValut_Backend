# app/modules/master_data/services.py
from typing import List, Dict, Tuple, Type
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.seed.models import (
    Gender,
    BloodType,
    UnitType,
    SmokingLevel,
    AlcoholLevel,
    ExerciseLevel,
    MedicalConditionSuggestion,
    Allergy,
    GeneticCondition,
    AppVersion,
    SubscriptionPlan,
)
from app.modules.master_data.schemas import (
    GenderSchema,
    BloodTypeSchema,
    UnitTypeSchema,
    SmokingLevelSchema,
    AlcoholLevelSchema,
    ExerciseLevelSchema,
    MedicalConditionSuggestionSchema,
    AllergySchema,
    GeneticConditionSchema,
    AppVersionSchema,
    SubscriptionPlanSchema,
)
from app.utils.logger import log_error, log_info
from app.utils.response import success_response, not_found, internal_error


# Mapping: "request path name" -> (ORM model, Pydantic schema)
MODEL_SCHEMA_MAP: Dict[str, Tuple[Type, Type]] = {
    "genders": (Gender, GenderSchema),
    "blood_types": (BloodType, BloodTypeSchema),
    "unit_types": (UnitType, UnitTypeSchema),
    "smoking_levels": (SmokingLevel, SmokingLevelSchema),
    "alcohol_levels": (AlcoholLevel, AlcoholLevelSchema),
    "exercise_levels": (ExerciseLevel, ExerciseLevelSchema),
    "medical_conditions_suggestions": (
        MedicalConditionSuggestion,
        MedicalConditionSuggestionSchema,
    ),
    "allergies": (Allergy, AllergySchema),
    "genetic_conditions": (GeneticCondition, GeneticConditionSchema),
    "app_versions": (AppVersion, AppVersionSchema),
    "subscription_plans": (SubscriptionPlan, SubscriptionPlanSchema),
}


class MasterDataService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_master_data(self) -> Dict[str, any]:
        """
        Fetch all master tables and return a uniform HTTP response.
        """
        output: Dict[str, List[dict]] = {}

        try:
            log_info("Fetching all master data")

            for key, (model_cls, schema_cls) in MODEL_SCHEMA_MAP.items():
                rows = (await self.db.execute(select(model_cls))).scalars().all()
                output[key] = [schema_cls.model_validate(r).model_dump() for r in rows]

            log_info("Fetched all master data successfully")
            return success_response(
                message="All master data retrieved successfully.",
                data=output,
            )

        except Exception as e:
            log_error(f"Failed fetching all master data: {e}")
            return internal_error(
                message=f"Failed fetching all master data: {str(e)}"
            )

    async def get_master_data_by_type(self, data_type: str) -> Dict[str, any]:
        """
        Fetch a single master data type and return a uniform HTTP response.
        Returns 404 if the type is unknown.
        """
        key = data_type.lower()

        try:
            log_info(f"Requested master data for type: {key}")

            if key not in MODEL_SCHEMA_MAP:
                return not_found(
                    message=f"Master data type '{data_type}' not found."
                )

            model_cls, schema_cls = MODEL_SCHEMA_MAP[key]
            rows = (await self.db.execute(select(model_cls))).scalars().all()
            output = [schema_cls.model_validate(r).model_dump() for r in rows]

            log_info(f"Fetched {len(output)} rows for {key}")
            return success_response(
                message=f"Master data for '{data_type}' retrieved successfully.",
                data=output,
            )

        except Exception as e:
            log_error(f"Error fetching master data for {data_type}: {e}")
            return internal_error(
                message=f"Failed fetching master data for '{data_type}': {str(e)}"
            )