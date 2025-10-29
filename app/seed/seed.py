from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.seed.models import (
    AppVersion, SubscriptionPlan, Gender, UnitType, BloodType, SmokingLevel,
    AlcoholLevel, ExerciseLevel, MedicalConditionSuggestion, Allergy, GeneticCondition
)
from app.seed.data import (
    app_versions, subscription_plans, genders, unit_types, blood_types,
    smoking_levels, alcohol_levels, exercise_levels,
    medical_conditions_suggestions, allergies, genetic_conditions
)


async def seed_table(session: AsyncSession, model, default_data: list[dict]):
    result = await session.execute(select(model))
    existing = result.scalars().first()
    if not existing:
        print(f"Seeding {model.__tablename__}...")
        objs = [model(**item) for item in default_data]
        session.add_all(objs)
        await session.commit()
        print(f"{model.__tablename__} seeded successfully!")


async def run_seeds(session: AsyncSession):
    await seed_table(session, AppVersion, app_versions)
    await seed_table(session, SubscriptionPlan, subscription_plans)
    await seed_table(session, Gender, genders)
    await seed_table(session, UnitType, unit_types)
    await seed_table(session, BloodType, blood_types)
    await seed_table(session, SmokingLevel, smoking_levels)
    await seed_table(session, AlcoholLevel, alcohol_levels)
    await seed_table(session, ExerciseLevel, exercise_levels)
    await seed_table(session, MedicalConditionSuggestion, medical_conditions_suggestions)
    await seed_table(session, Allergy, allergies)
    await seed_table(session, GeneticCondition, genetic_conditions)