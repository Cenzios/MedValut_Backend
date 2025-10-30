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
-- Table: users
-- ==========================================
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL,
    `phone_number` VARCHAR(20) NULL,
    `country_code` VARCHAR(20) NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `nic` VARCHAR(20) NOT NULL,
    `sign_up_method` INT NOT NULL,
    `social_id` VARCHAR(255) NULL,
    `full_name` VARCHAR(255) NOT NULL,
    `date_of_birth` DATETIME NULL,
    `gender_id` INT NULL,
    `gender` VARCHAR(50) NULL,
    `address` TEXT NULL,
    `city` VARCHAR(100) NULL,
    `province` VARCHAR(100) NULL,
    `emergency_contact_name` VARCHAR(100) NULL,
    `emergency_contact_phone` VARCHAR(20) NULL,
    `emergency_contact_relationship` VARCHAR(50) NULL,
    `profile_picture_url` VARCHAR(500) NULL,
    `bio` TEXT NULL,
    `is_profile_completed` BOOLEAN DEFAULT FALSE NOT NULL,
    `is_email_verified` BOOLEAN DEFAULT FALSE NOT NULL,
    `is_emergency_contact_added` BOOLEAN DEFAULT FALSE NOT NULL,
    `login_attempts` INT DEFAULT 0 NOT NULL,
    `locked_until` DATETIME NULL,
    `last_login` DATETIME NULL,
    `subscription_plan_id` INT DEFAULT 1 NULL,
    `subscription_start_date` DATETIME NULL,
    `subscription_end_date` DATETIME NULL,
    `height` FLOAT NULL,
    `height_unit_id` INT NULL,
    `weight` FLOAT NULL,
    `weight_unit_id` INT NULL,
    `blood_type_id` INT NULL,
    `smoking_level_id` INT NULL,
    `alcohol_level_id` INT NULL,
    `exercise_level_id` INT NULL,
    `pre_medical_conditions` TEXT NULL,
    `chronical_diseases` TEXT NULL,
    `allergies` TEXT NULL,
    `medicones_currently_taking` TEXT NULL,
    `surgeries_history` TEXT NULL,
    `has_heart_disease_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `has_diabetes_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `has_hypertension_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `has_cancer_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `has_asthma_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `has_other_family_history` TEXT NULL,
    `other_family_medical_history` TEXT NULL,
    `has_genetic_disorders_family_history` BOOLEAN DEFAULT FALSE NOT NULL,
    `family_genetic_disorders_details` TEXT NULL,
    `is_active` BOOLEAN DEFAULT TRUE NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    INDEX `ix_users_email_is_active` (`email`, `is_active`),
    INDEX `ix_users_nic_is_active` (`nic`, `is_active`)
);

-- ==========================================
-- Table: otp_verifications
-- ==========================================
CREATE TABLE IF NOT EXISTS `otp_verifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL,
    `otp_code` VARCHAR(10) NOT NULL,
    `otp_type` INT DEFAULT 1 NOT NULL,
    `otp_reference` VARCHAR(100) NULL,
    `is_used` BOOLEAN DEFAULT FALSE NOT NULL,
    `expires_at` DATETIME NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `used_at` DATETIME NULL,
    INDEX `ix_otp_verifications_email` (`email`)
);

-- ==========================================
-- Table: refresh_tokens
-- ==========================================
CREATE TABLE IF NOT EXISTS `refresh_tokens` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `token` VARCHAR(500) NOT NULL UNIQUE,
    `is_active` BOOLEAN DEFAULT TRUE NOT NULL,
    `expires_at` DATETIME NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `last_used_at` DATETIME NULL,
    `user_agent` VARCHAR(500) NULL,
    `ip_address` VARCHAR(45) NULL,
    INDEX `ix_refresh_tokens_user_id_is_active` (`user_id`, `is_active`)
);

-- ==========================================
-- Table: password_reset_tokens
-- ==========================================
CREATE TABLE IF NOT EXISTS `password_reset_tokens` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `token` VARCHAR(500) NOT NULL UNIQUE,
    `is_used` BOOLEAN DEFAULT FALSE NOT NULL,
    `expires_at` DATETIME NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `used_at` DATETIME NULL,
    INDEX `ix_password_reset_tokens_user_id` (`user_id`)
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
