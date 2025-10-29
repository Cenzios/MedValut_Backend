from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------------------
# ActionLog
# -------------------------------
class ActionLogSchema(BaseModel):
    id: int
    user_id: int
    action_name: str
    details: Optional[dict]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

# -------------------------------
# AppVersion
# -------------------------------
class AppVersionSchema(BaseModel):
    id: int
    app_type: str
    build_number: int

    model_config = {"from_attributes": True}

# -------------------------------
# SubscriptionPlan
# -------------------------------
class SubscriptionPlanSchema(BaseModel):
    id: int
    plan_name: str
    plan_price_per_month: float
    plan_price_per_annum: float
    annual_plan_discount_percentage: float
    max_document_count: int
    max_storage_gb: int

    model_config = {"from_attributes": True}

# -------------------------------
# Gender
# -------------------------------
class GenderSchema(BaseModel):
    id: int
    gender: Optional[str]

    model_config = {"from_attributes": True}

# -------------------------------
# UnitType
# -------------------------------
class UnitTypeSchema(BaseModel):
    id: int
    type: str
    symbol: Optional[str]
    name: Optional[str]

    model_config = {"from_attributes": True}

# -------------------------------
# BloodType
# -------------------------------
class BloodTypeSchema(BaseModel):
    id: int
    type: str

    model_config = {"from_attributes": True}

# -------------------------------
# SmokingLevel
# -------------------------------
class SmokingLevelSchema(BaseModel):
    id: int
    level_name: str

    model_config = {"from_attributes": True}

# -------------------------------
# AlcoholLevel
# -------------------------------
class AlcoholLevelSchema(BaseModel):
    id: int
    level: str

    model_config = {"from_attributes": True}

# -------------------------------
# ExerciseLevel
# -------------------------------
class ExerciseLevelSchema(BaseModel):
    id: int
    level: str

    model_config = {"from_attributes": True}

# -------------------------------
# MedicalConditionSuggestion
# -------------------------------
class MedicalConditionSuggestionSchema(BaseModel):
    id: int
    medical_condition: str
    weight_number: float

    model_config = {"from_attributes": True}

# -------------------------------
# Allergy
# -------------------------------
class AllergySchema(BaseModel):
    id: int
    allergy_name: str
    weight_number: float

    model_config = {"from_attributes": True}

# -------------------------------
# GeneticCondition
# -------------------------------
class GeneticConditionSchema(BaseModel):
    id: int
    condition_name: str
    weight_number: float

    model_config = {"from_attributes": True}