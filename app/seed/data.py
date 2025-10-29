# ----------------------
# App Versions
# ----------------------
app_versions = [
    {"id": 1, "app_type": "android", "build_number": 1},
    {"id": 2, "app_type": "ios", "build_number": 1},
    {"id": 3, "app_type": "web", "build_number": 1},
]

# ----------------------
# Subscription Plans
# ----------------------
subscription_plans = [
    {"id": 1, "plan_name": "Free", "plan_price_per_month": 0, "plan_price_per_annum": 0,
     "annual_plan_discount_percentage": 0, "max_document_count": 10, "max_storage_gb": 1},
    {"id": 2, "plan_name": "Standard", "plan_price_per_month": 6, "plan_price_per_annum": 60,
     "annual_plan_discount_percentage": 20, "max_document_count": 100, "max_storage_gb": 3},
    {"id": 3, "plan_name": "Premium", "plan_price_per_month": 12, "plan_price_per_annum": 120,
     "annual_plan_discount_percentage": 20, "max_document_count": 200, "max_storage_gb": 5},
]

# ----------------------
# Genders
# ----------------------
genders = [
    {"id": 1, "gender": "male"},
    {"id": 2, "gender": "female"},
]

# ----------------------
# Unit Types
# ----------------------
unit_types = [
    {"id": 1, "type": "height", "symbol": "cm", "name": "centimeter"},
    {"id": 2, "type": "height", "symbol": "m", "name": "meter"},
    {"id": 3, "type": "height", "symbol": "in", "name": "inches"},
    {"id": 4, "type": "weight", "symbol": "kg", "name": "kilogram"},
]

# ----------------------
# Blood Types
# ----------------------
blood_types = [
    {"id": 1, "type": "A+"}, {"id": 2, "type": "A-"}, {"id": 3, "type": "B+"}, {"id": 4, "type": "B-"},
    {"id": 5, "type": "AB+"}, {"id": 6, "type": "AB-"}, {"id": 7, "type": "O+"}, {"id": 8, "type": "O-"},
]

# ----------------------
# Smoking Levels
# ----------------------
smoking_levels = [
    {"id": 1, "level_name": "Non-smoker"},
    {"id": 2, "level_name": "Occasional"},
    {"id": 3, "level_name": "Regular"},
]

# ----------------------
# Alcohol Levels
# ----------------------
alcohol_levels = [
    {"id": 1, "level": "Never"},
    {"id": 2, "level": "Occasional"},
    {"id": 3, "level": "Regular"},
]

# ----------------------
# Exercise Levels
# ----------------------
exercise_levels = [
    {"id": 1, "level": "None"},
    {"id": 2, "level": "Low"},
    {"id": 3, "level": "Moderate"},
    {"id": 4, "level": "High"},
]

# ----------------------
# Medical Conditions Suggestions
# ----------------------
medical_conditions_suggestions = [
    {"id": 1, "medical_condition": "Diabetes", "weight_number": 1},
    {"id": 2, "medical_condition": "Hypertension", "weight_number": 1},
]

# ----------------------
# Allergies
# ----------------------
allergies = [
    {"id": 1, "allergy_name": "Pollen", "weight_number": 1},
    {"id": 2, "allergy_name": "Dust", "weight_number": 1},
    {"id": 3, "allergy_name": "Other", "weight_number": 0},
]

# ----------------------
# Genetic Conditions
# ----------------------
genetic_conditions = [
    {"id": 1, "condition_name": "Heart Disease", "weight_number": 1},
    {"id": 2, "condition_name": "Cancer", "weight_number": 1},
]