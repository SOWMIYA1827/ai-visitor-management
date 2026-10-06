-- ============================================================
-- PackSmart AI — PostgreSQL Schema
-- Smart India Hackathon 2026 (Problem ID 26236)
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- ENUM TYPE DEFINITIONS
-- ──────────────────────────────────────────────────────────

CREATE TYPE user_type_enum AS ENUM (
    'farmer',
    'food_processor',
    'small_business',
    'packaging_manufacturer',
    'researcher',
    'admin'
);

CREATE TYPE food_category_enum AS ENUM (
    'fruits',
    'vegetables',
    'cereals',
    'pulses',
    'spices',
    'dairy',
    'meat',
    'fish',
    'bakery',
    'snacks',
    'processed_food',
    'beverages',
    'other'
);

CREATE TYPE sensitivity_level_enum AS ENUM (
    'low',
    'medium',
    'high'
);

CREATE TYPE perishability_level_enum AS ENUM (
    'low',
    'medium',
    'high'
);

CREATE TYPE material_category_enum AS ENUM (
    'plastic',
    'paper',
    'metal',
    'glass',
    'biodegradable',
    'multilayer',
    'composite'
);

CREATE TYPE transportation_type_enum AS ENUM (
    'road',
    'rail',
    'air',
    'sea'
);

CREATE TYPE packaging_type_enum AS ENUM (
    'pouch',
    'bag',
    'bottle',
    'tray',
    'box',
    'vacuum_pack',
    'map',
    'flexible',
    'rigid'
);

CREATE TYPE priority_enum AS ENUM (
    'low_cost',
    'max_shelf_life',
    'food_safety',
    'sustainability',
    'balanced'
);

CREATE TYPE eco_preference_enum AS ENUM (
    'no_preference',
    'recyclable',
    'biodegradable',
    'compostable',
    'bio_based'
);


-- ──────────────────────────────────────────────────────────
-- TABLES
-- ──────────────────────────────────────────────────────────

-- 1. Users
CREATE TABLE IF NOT EXISTS users (
    id              VARCHAR(36)         PRIMARY KEY DEFAULT gen_random_uuid()::text,
    email           VARCHAR(255)        NOT NULL UNIQUE,
    hashed_password VARCHAR(255)        NOT NULL,
    full_name       VARCHAR(255)        NOT NULL,
    user_type       user_type_enum      NOT NULL DEFAULT 'farmer',
    organization    VARCHAR(255),
    phone_number    VARCHAR(50),
    is_active       BOOLEAN             NOT NULL DEFAULT TRUE,
    is_admin        BOOLEAN             NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);


-- 2. Packaging materials (knowledge base)
CREATE TABLE IF NOT EXISTS packaging_materials (
    id                      VARCHAR(36)             PRIMARY KEY DEFAULT gen_random_uuid()::text,
    name                    VARCHAR(255)            NOT NULL UNIQUE,
    material_code           VARCHAR(50)             NOT NULL UNIQUE,
    category                material_category_enum  NOT NULL,

    -- Barrier properties (0.0 – 1.0; higher = better barrier)
    moisture_barrier        DOUBLE PRECISION        NOT NULL DEFAULT 0.5,
    oxygen_barrier          DOUBLE PRECISION        NOT NULL DEFAULT 0.5,
    light_barrier           DOUBLE PRECISION        NOT NULL DEFAULT 0.5,
    thermal_resistance      DOUBLE PRECISION        NOT NULL DEFAULT 0.5,
    mechanical_strength     DOUBLE PRECISION        NOT NULL DEFAULT 0.5,

    -- Compliance & sustainability flags
    food_contact_safe       BOOLEAN                 NOT NULL DEFAULT TRUE,
    recyclable              BOOLEAN                 NOT NULL DEFAULT FALSE,
    biodegradable           BOOLEAN                 NOT NULL DEFAULT FALSE,
    compostable             BOOLEAN                 NOT NULL DEFAULT FALSE,
    bio_based               BOOLEAN                 NOT NULL DEFAULT FALSE,

    -- Economics (0 = cheapest, 1 = most expensive)
    cost_index              DOUBLE PRECISION        NOT NULL DEFAULT 0.5,

    -- Physical specs (micrometres)
    typical_thickness_min_um DOUBLE PRECISION,
    typical_thickness_max_um DOUBLE PRECISION,

    -- Metadata
    description             TEXT,
    suitable_for            TEXT,   -- JSON array of food_category strings

    created_at              TIMESTAMPTZ             NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_packaging_materials_material_code ON packaging_materials (material_code);


-- 3. Food profiles
CREATE TABLE IF NOT EXISTS food_profiles (
    id                    VARCHAR(36)             PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id               VARCHAR(36)             NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    food_name             VARCHAR(255)            NOT NULL,
    category              food_category_enum      NOT NULL,

    -- Composition
    moisture_content      DOUBLE PRECISION,       -- %
    ph                    DOUBLE PRECISION,       -- 0-14
    fat_content           DOUBLE PRECISION,       -- %
    protein_content       DOUBLE PRECISION,       -- %
    water_activity        DOUBLE PRECISION,       -- aw 0-1
    respiration_rate      DOUBLE PRECISION,       -- mg CO2/kg/h
    perishability         perishability_level_enum,

    -- Sensitivities
    oxygen_sensitivity    sensitivity_level_enum,
    moisture_sensitivity  sensitivity_level_enum,
    light_sensitivity     sensitivity_level_enum,
    temperature_sensitivity sensitivity_level_enum,
    odor_sensitivity      sensitivity_level_enum,
    microbial_sensitivity sensitivity_level_enum,

    created_at            TIMESTAMPTZ             NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_food_profiles_user_id ON food_profiles (user_id);


-- 4. Storage conditions
CREATE TABLE IF NOT EXISTS storage_conditions (
    id                          VARCHAR(36)             PRIMARY KEY DEFAULT gen_random_uuid()::text,
    storage_temp                DOUBLE PRECISION,       -- °C
    storage_humidity            DOUBLE PRECISION,       -- % RH
    storage_duration_days       INTEGER,
    transportation_duration_days INTEGER,
    transportation_type         transportation_type_enum,
    cold_chain_required         BOOLEAN                 NOT NULL DEFAULT FALSE
);


-- 5. Packaging requirements
CREATE TABLE IF NOT EXISTS packaging_requirements (
    id                      VARCHAR(36)             PRIMARY KEY DEFAULT gen_random_uuid()::text,
    required_shelf_life_days INTEGER,
    package_size            VARCHAR(100),
    package_quantity        INTEGER,
    budget                  DOUBLE PRECISION,
    packaging_type          packaging_type_enum,
    priority                priority_enum                       DEFAULT 'balanced',
    eco_preference          eco_preference_enum                 DEFAULT 'no_preference'
);


-- 6. Recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id                              VARCHAR(36)         PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id                         VARCHAR(36)         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    food_profile_id                 VARCHAR(36)         NOT NULL REFERENCES food_profiles(id) ON DELETE CASCADE,
    storage_conditions_id           VARCHAR(36)         REFERENCES storage_conditions(id),
    packaging_requirements_id       VARCHAR(36)         REFERENCES packaging_requirements(id),

    primary_material_id             VARCHAR(36)         REFERENCES packaging_materials(id),
    alternative_material_ids        TEXT,               -- JSON array of material IDs

    packaging_structure             TEXT,
    barrier_properties              TEXT,               -- JSON object
    recommended_thickness_um        DOUBLE PRECISION,
    storage_conditions_recommended  TEXT,
    shelf_life_min_days             INTEGER,
    shelf_life_max_days             INTEGER,
    risk_factors                    TEXT,               -- JSON array

    sustainability_score            DOUBLE PRECISION,   -- 0-100
    cost_score                      DOUBLE PRECISION,   -- 0-100
    food_safety_score               DOUBLE PRECISION,   -- 0-100
    overall_score                   DOUBLE PRECISION,   -- 0-100

    explanation                     TEXT,

    created_at                      TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_recommendations_user_id ON recommendations (user_id);
CREATE INDEX IF NOT EXISTS ix_recommendations_food_profile_id ON recommendations (food_profile_id);
CREATE INDEX IF NOT EXISTS ix_recommendations_created_at ON recommendations (created_at DESC);
