-- ==========================================
-- Table: action_logs
-- ==========================================
CREATE TABLE IF NOT EXISTS `action_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `action_name` VARCHAR(255) NOT NULL,
    `details` JSON,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Table: app_versions
-- ==========================================
CREATE TABLE IF NOT EXISTS `app_versions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `app_type` VARCHAR(50) NOT NULL,
    `build_number` INT NOT NULL
);

-- ==========================================
-- Table: subscription_plans
-- ==========================================
CREATE TABLE IF NOT EXISTS `subscription_plans` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `plan_name` VARCHAR(50) NOT NULL,
    `plan_price_per_month` FLOAT DEFAULT 0,
    `plan_price_per_annum` FLOAT DEFAULT 0,
    `annual_plan_discount_percentage` FLOAT DEFAULT 0,
    `max_document_count` INT DEFAULT 0,
    `max_storage_gb` INT DEFAULT 0
);

-- ==========================================
-- Table: genders
-- ==========================================
CREATE TABLE IF NOT EXISTS `genders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `gender` VARCHAR(50) NULL
);

-- ==========================================
-- Table: unit_types
-- ==========================================
CREATE TABLE IF NOT EXISTS `unit_types` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `type` VARCHAR(50),
    `symbol` VARCHAR(20),
    `name` VARCHAR(50)
);

-- ==========================================
-- Table: blood_types
-- ==========================================
CREATE TABLE IF NOT EXISTS `blood_types` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `type` VARCHAR(10)
);

-- ==========================================
-- Table: smoking_levels
-- ==========================================
CREATE TABLE IF NOT EXISTS `smoking_levels` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `level_name` VARCHAR(50)
);

-- ==========================================
-- Table: alcohol_levels
-- ==========================================
CREATE TABLE IF NOT EXISTS `alcohol_levels` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `level` VARCHAR(50)
);

-- ==========================================
-- Table: exercise_levels
-- ==========================================
CREATE TABLE IF NOT EXISTS `exercise_levels` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `level` VARCHAR(50)
);

-- ==========================================
-- Table: medical_conditions_suggestions
-- ==========================================
CREATE TABLE IF NOT EXISTS `medical_conditions_suggestions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `medical_condition` VARCHAR(255),
    `weight_number` FLOAT DEFAULT 0
);

-- ==========================================
-- Table: allergies
-- ==========================================
CREATE TABLE IF NOT EXISTS `allergies` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `allergy_name` VARCHAR(255),
    `weight_number` FLOAT DEFAULT 0
);

-- ==========================================
-- Table: genetic_conditions
-- ==========================================
CREATE TABLE IF NOT EXISTS `genetic_conditions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `condition_name` VARCHAR(255),
    `weight_number` FLOAT DEFAULT 0
);