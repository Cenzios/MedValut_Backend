from sqlalchemy import Column, Integer, String, Float, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    action_name = Column(String(255), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class AppVersion(Base):
    __tablename__ = "app_versions"
    id = Column(Integer, primary_key=True)
    app_type = Column(String(50), nullable=False)
    build_number = Column(Integer, nullable=False)


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True)
    plan_name = Column(String(50), nullable=False)
    plan_price_per_month = Column(Float, default=0)
    plan_price_per_annum = Column(Float, default=0)
    annual_plan_discount_percentage = Column(Float, default=0)
    max_document_count = Column(Integer, default=0)
    max_storage_gb = Column(Integer, default=0)


class Gender(Base):
    __tablename__ = "genders"
    id = Column(Integer, primary_key=True)
    gender = Column(String(50), nullable=True)


class UnitType(Base):
    __tablename__ = "unit_types"
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    symbol = Column(String(20))
    name = Column(String(50))


class BloodType(Base):
    __tablename__ = "blood_types"
    id = Column(Integer, primary_key=True)
    type = Column(String(10))


class SmokingLevel(Base):
    __tablename__ = "smoking_levels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(50))


class AlcoholLevel(Base):
    __tablename__ = "alcohol_levels"
    id = Column(Integer, primary_key=True)
    level = Column(String(50))


class ExerciseLevel(Base):
    __tablename__ = "exercise_levels"
    id = Column(Integer, primary_key=True)
    level = Column(String(50))


class MedicalConditionSuggestion(Base):
    __tablename__ = "medical_conditions_suggestions"
    id = Column(Integer, primary_key=True)
    medical_condition = Column(String(255))
    weight_number = Column(Float, default=0)


class Allergy(Base):
    __tablename__ = "allergies"
    id = Column(Integer, primary_key=True)
    allergy_name = Column(String(255))
    weight_number = Column(Float, default=0)


class GeneticCondition(Base):
    __tablename__ = "genetic_conditions"
    id = Column(Integer, primary_key=True)
    condition_name = Column(String(255))
    weight_number = Column(Float, default=0)