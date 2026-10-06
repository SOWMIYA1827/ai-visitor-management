-- ============================================================
-- PackSmart AI — Seed Data (PostgreSQL)
-- Smart India Hackathon 2026 (Problem ID 26236)
-- ============================================================
-- Run AFTER schema.sql.
-- Uses INSERT ... ON CONFLICT DO NOTHING for idempotency.
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- 1. Default admin user
--    Password hash below corresponds to: Admin@123
--    (bcrypt round 12 — regenerate with get_password_hash() in production)
-- ──────────────────────────────────────────────────────────
INSERT INTO users (
    id, email, hashed_password, full_name, user_type, organization, is_active, is_admin
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    'admin@packsmart.ai',
    '$2b$12$KIXAzZa3Z9CZ4P8Tz1H1SulLDlLO6V5fWbIxL1Lr2S5YWJzOiCFqm',
    'PackSmart Admin',
    'admin',
    'MoFPI / SIH 2026',
    TRUE,
    TRUE
) ON CONFLICT (email) DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 2. Demo farmer user (for dashboard examples)
-- ──────────────────────────────────────────────────────────
INSERT INTO users (
    id, email, hashed_password, full_name, user_type, organization, is_active, is_admin
) VALUES (
    '00000000-0000-0000-0000-000000000002',
    'demo@packsmart.ai',
    '$2b$12$KIXAzZa3Z9CZ4P8Tz1H1SulLDlLO6V5fWbIxL1Lr2S5YWJzOiCFqm',
    'Demo Farmer',
    'farmer',
    'Demo Farm, Pune',
    TRUE,
    FALSE
) ON CONFLICT (email) DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 3. Packaging materials (20 materials)
-- ──────────────────────────────────────────────────────────

INSERT INTO packaging_materials (
    id, name, material_code, category,
    moisture_barrier, oxygen_barrier, light_barrier, thermal_resistance, mechanical_strength,
    food_contact_safe, recyclable, biodegradable, compostable, bio_based,
    cost_index, typical_thickness_min_um, typical_thickness_max_um,
    description, suitable_for
) VALUES
-- 1
('10000000-0000-0000-0000-000000000001',
 'Low-Density Polyethylene (LDPE)', 'LDPE', 'plastic',
 0.75, 0.30, 0.20, 0.35, 0.40,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.25, 20.0, 100.0,
 'Flexible, moisture-resistant film suitable for fresh produce, bread, and frozen foods.',
 '["vegetables","fruits","bakery","cereals"]'),

-- 2
('10000000-0000-0000-0000-000000000002',
 'High-Density Polyethylene (HDPE)', 'HDPE', 'plastic',
 0.85, 0.35, 0.25, 0.50, 0.70,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.30, 25.0, 200.0,
 'Rigid or semi-rigid plastic with good moisture barrier. Used for milk jugs and cereal box liners.',
 '["dairy","beverages","cereals","pulses"]'),

-- 3
('10000000-0000-0000-0000-000000000003',
 'Polypropylene (PP)', 'PP', 'plastic',
 0.80, 0.40, 0.20, 0.65, 0.65,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.30, 20.0, 80.0,
 'Good moisture barrier with excellent heat resistance. Suitable for snack wrappers and dairy containers.',
 '["snacks","dairy","processed_food","bakery"]'),

-- 4
('10000000-0000-0000-0000-000000000004',
 'Biaxially Oriented Polypropylene (BOPP)', 'BOPP', 'plastic',
 0.82, 0.42, 0.22, 0.55, 0.72,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.35, 15.0, 60.0,
 'Oriented PP film with superior clarity and moisture barrier. Used for biscuit packaging and cereal bags.',
 '["snacks","cereals","bakery","pulses"]'),

-- 5
('10000000-0000-0000-0000-000000000005',
 'Polyethylene Terephthalate (PET)', 'PET', 'plastic',
 0.78, 0.60, 0.20, 0.60, 0.80,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.40, 12.0, 350.0,
 'High-clarity film with good gas barrier. Used for beverage bottles and deli trays.',
 '["beverages","processed_food","dairy","snacks"]'),

-- 6
('10000000-0000-0000-0000-000000000006',
 'Metallized PET', 'MET-PET', 'multilayer',
 0.92, 0.90, 0.95, 0.60, 0.80,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.55, 12.0, 25.0,
 'PET film vacuum-coated with aluminium giving excellent barrier. Used for crisps, nuts, and spices.',
 '["snacks","spices","cereals","pulses"]'),

-- 7
('10000000-0000-0000-0000-000000000007',
 'Aluminium Foil', 'ALU-FOIL', 'metal',
 0.99, 0.99, 1.00, 0.85, 0.50,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.65, 6.0, 150.0,
 'Complete barrier against moisture, oxygen, and light. Used in retort pouches and blister packs.',
 '["dairy","processed_food","meat","fish","beverages"]'),

-- 8
('10000000-0000-0000-0000-000000000008',
 'Paperboard', 'PAPERBOARD', 'paper',
 0.30, 0.25, 0.60, 0.30, 0.65,
 TRUE, TRUE, TRUE, TRUE, TRUE,
 0.30, 200.0, 800.0,
 'Lightweight rigid board used for cereal boxes and frozen food cartons.',
 '["cereals","bakery","beverages","processed_food"]'),

-- 9
('10000000-0000-0000-0000-000000000009',
 'Kraft Paper', 'KRAFT', 'paper',
 0.20, 0.15, 0.55, 0.20, 0.60,
 TRUE, TRUE, TRUE, TRUE, TRUE,
 0.20, 40.0, 120.0,
 'Strong, natural brown paper for flour bags, sugar sacks, and dry goods.',
 '["cereals","pulses","spices","other"]'),

-- 10
('10000000-0000-0000-0000-000000000010',
 'Glass Jar/Bottle', 'GLASS', 'glass',
 1.00, 1.00, 0.50, 0.70, 0.55,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.70, 1500.0, 5000.0,
 'Inert, impermeable container ideal for pickles, jams, sauces, and premium products.',
 '["dairy","beverages","processed_food","spices"]'),

-- 11
('10000000-0000-0000-0000-000000000011',
 'PET Bottle', 'PET-BOTTLE', 'plastic',
 0.80, 0.62, 0.20, 0.58, 0.78,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.42, 200.0, 500.0,
 'Blow-moulded PET bottle with good clarity and moderate gas barrier.',
 '["beverages","dairy","processed_food"]'),

-- 12
('10000000-0000-0000-0000-000000000012',
 'HDPE Bottle', 'HDPE-BOTTLE', 'plastic',
 0.87, 0.38, 0.30, 0.52, 0.72,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.33, 300.0, 600.0,
 'Rigid HDPE bottle with excellent moisture barrier used for milk and juice.',
 '["dairy","beverages","processed_food"]'),

-- 13
('10000000-0000-0000-0000-000000000013',
 'Polylactic Acid (PLA)', 'PLA', 'biodegradable',
 0.55, 0.50, 0.20, 0.30, 0.55,
 TRUE, FALSE, TRUE, TRUE, TRUE,
 0.60, 20.0, 60.0,
 'Bio-based and compostable film from corn/sugarcane starch. For fresh produce and bakery.',
 '["fruits","vegetables","bakery","other"]'),

-- 14
('10000000-0000-0000-0000-000000000014',
 'Biodegradable Film', 'BIO-FILM', 'biodegradable',
 0.50, 0.45, 0.20, 0.25, 0.45,
 TRUE, FALSE, TRUE, TRUE, TRUE,
 0.65, 15.0, 50.0,
 'PBAT/starch blend film that degrades in composting conditions.',
 '["fruits","vegetables","bakery","other"]'),

-- 15
('10000000-0000-0000-0000-000000000015',
 'EVOH Barrier Film', 'EVOH', 'multilayer',
 0.60, 0.97, 0.30, 0.55, 0.70,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.70, 3.0, 15.0,
 'Exceptional oxygen barrier as core layer in multilayer films. For meat, cheese, and processed foods.',
 '["meat","fish","dairy","processed_food"]'),

-- 16
('10000000-0000-0000-0000-000000000016',
 'Nylon (Polyamide / PA)', 'PA', 'plastic',
 0.55, 0.70, 0.20, 0.75, 0.85,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.55, 15.0, 50.0,
 'Strong film with good oxygen and puncture resistance for vacuum pouches.',
 '["meat","fish","dairy","processed_food"]'),

-- 17
('10000000-0000-0000-0000-000000000017',
 'Perforated LDPE Film', 'PERF-LDPE', 'plastic',
 0.40, 0.10, 0.10, 0.35, 0.35,
 TRUE, TRUE, FALSE, FALSE, FALSE,
 0.20, 20.0, 50.0,
 'LDPE film with micro-perforations for gas exchange controlling respiration of fresh produce.',
 '["vegetables","fruits"]'),

-- 18
('10000000-0000-0000-0000-000000000018',
 'BOPP + PE Laminate', 'BOPP-PE', 'multilayer',
 0.85, 0.45, 0.25, 0.55, 0.75,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.40, 30.0, 80.0,
 'Two-layer laminate combining BOPP stiffness with PE heat-sealability. Common for rice and cereals.',
 '["cereals","pulses","spices","snacks"]'),

-- 19
('10000000-0000-0000-0000-000000000019',
 'Metallized PET + PE Laminate', 'MET-PET-PE', 'multilayer',
 0.93, 0.91, 0.96, 0.60, 0.82,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.58, 30.0, 70.0,
 'High-barrier laminate for moisture, oxygen, and light. Used for potato chips and premium snacks.',
 '["snacks","spices","cereals","pulses"]'),

-- 20
('10000000-0000-0000-0000-000000000020',
 'Retort Pouch (Alu Foil Laminate)', 'RETORT-POUCH', 'multilayer',
 0.99, 0.99, 1.00, 0.90, 0.80,
 TRUE, FALSE, FALSE, FALSE, FALSE,
 0.80, 80.0, 150.0,
 'PET/Alu/PP multilayer pouch withstanding retort sterilisation (121°C) for ready-to-eat meals.',
 '["meat","fish","processed_food","dairy"]')

ON CONFLICT (material_code) DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 4. Demo food profiles for dashboard examples
-- ──────────────────────────────────────────────────────────

INSERT INTO food_profiles (
    id, user_id, food_name, category,
    moisture_content, ph, fat_content, protein_content, water_activity,
    perishability, oxygen_sensitivity, moisture_sensitivity, light_sensitivity
) VALUES
-- Rice
('20000000-0000-0000-0000-000000000001',
 '00000000-0000-0000-0000-000000000002',
 'Basmati Rice', 'cereals',
 12.0, 6.5, 0.5, 7.0, 0.60,
 'low', 'low', 'medium', 'low'),
-- Tomato
('20000000-0000-0000-0000-000000000002',
 '00000000-0000-0000-0000-000000000002',
 'Tomato', 'vegetables',
 94.0, 4.2, 0.2, 0.9, 0.98,
 'high', 'medium', 'high', 'low'),
-- Potato Chips
('20000000-0000-0000-0000-000000000003',
 '00000000-0000-0000-0000-000000000002',
 'Potato Chips', 'snacks',
 2.0, 6.0, 35.0, 6.0, 0.30,
 'low', 'high', 'high', 'high')
ON CONFLICT DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 5. Demo storage conditions
-- ──────────────────────────────────────────────────────────

INSERT INTO storage_conditions (
    id, storage_temp, storage_humidity, storage_duration_days, transportation_type, cold_chain_required
) VALUES
('30000000-0000-0000-0000-000000000001', 25.0, 65.0, 270, 'road', FALSE),
('30000000-0000-0000-0000-000000000002',  4.0, 90.0,  14, 'road', FALSE),
('30000000-0000-0000-0000-000000000003', 25.0, 50.0, 180, 'road', FALSE)
ON CONFLICT DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 6. Demo packaging requirements
-- ──────────────────────────────────────────────────────────

INSERT INTO packaging_requirements (
    id, required_shelf_life_days, package_size, package_quantity, budget,
    packaging_type, priority, eco_preference
) VALUES
('40000000-0000-0000-0000-000000000001', 270, '5 kg bag',    500, 5000.0, 'bag',   'balanced',       'no_preference'),
('40000000-0000-0000-0000-000000000002',  14, '500 g punnet', 200,  500.0, 'tray',  'food_safety',    'no_preference'),
('40000000-0000-0000-0000-000000000003', 180, '50 g pouch',  1000, 8000.0, 'pouch', 'max_shelf_life', 'no_preference')
ON CONFLICT DO NOTHING;


-- ──────────────────────────────────────────────────────────
-- 7. Demo recommendations (matching dashboard examples)
-- ──────────────────────────────────────────────────────────

INSERT INTO recommendations (
    id, user_id, food_profile_id,
    storage_conditions_id, packaging_requirements_id,
    primary_material_id, alternative_material_ids,
    packaging_structure,
    barrier_properties,
    recommended_thickness_um,
    storage_conditions_recommended,
    shelf_life_min_days, shelf_life_max_days,
    risk_factors,
    sustainability_score, cost_score, food_safety_score, overall_score,
    explanation
) VALUES
-- Rice → BOPP + PE
('50000000-0000-0000-0000-000000000001',
 '00000000-0000-0000-0000-000000000002',
 '20000000-0000-0000-0000-000000000001',
 '30000000-0000-0000-0000-000000000001',
 '40000000-0000-0000-0000-000000000001',
 '10000000-0000-0000-0000-000000000018',  -- BOPP-PE
 '["10000000-0000-0000-0000-000000000004","10000000-0000-0000-0000-000000000003"]',
 'Bag — BOPP + PE Laminate 55 µm',
 '{"moisture_barrier":0.85,"oxygen_barrier":0.45,"light_barrier":0.25,"thermal_resistance":0.55,"mechanical_strength":0.75}',
 55.0,
 'Store in cool, dry conditions at 15-25°C and <65% RH.',
 182, 243,
 '["Laminate is not recyclable — consider mono-material PE when shelf life allows","Oxygen barrier is moderate; ensure hermetic seal to prevent rancidity","Store away from strong odours — BOPP can absorb aromas"]',
 62.0, 78.0, 84.0, 91.0,
 'BOPP + PE Laminate is recommended for Basmati Rice because it provides excellent moisture barrier (0.85) and good mechanical strength (0.75) critical for protecting this low-perishability cereal during long-term ambient storage. The heat-sealable PE inner layer ensures a hermetic seal that prevents moisture ingress, the primary risk for dry cereals. The moderate oxygen barrier is adequate given rice''s low oxygen sensitivity. Cost efficiency (index 0.40) makes it economical for bulk packaging at 500 bags.'),

-- Tomato → Perforated LDPE
('50000000-0000-0000-0000-000000000002',
 '00000000-0000-0000-0000-000000000002',
 '20000000-0000-0000-0000-000000000002',
 '30000000-0000-0000-0000-000000000002',
 '40000000-0000-0000-0000-000000000002',
 '10000000-0000-0000-0000-000000000017',  -- PERF-LDPE
 '["10000000-0000-0000-0000-000000000001","10000000-0000-0000-0000-000000000013"]',
 'Tray — Perforated LDPE Film 35 µm',
 '{"moisture_barrier":0.40,"oxygen_barrier":0.10,"light_barrier":0.10,"thermal_resistance":0.35,"mechanical_strength":0.35}',
 35.0,
 'Store at 0-5°C with relative humidity 90-95%.',
 7, 15,
 '["Very high perishability — cold chain must be maintained at all times","Perforations increase exposure to pathogens if cold chain is broken","Short shelf life of 7-15 days; plan distribution accordingly"]',
 70.0, 82.0, 79.0, 88.0,
 'Perforated LDPE Film is recommended for Tomato because this highly perishable fruit requires active gas exchange to control its high respiration rate. The micro-perforations in LDPE allow CO2 to escape while admitting O2, slowing ethylene accumulation and delaying ripening. Its recyclability supports sustainability goals. The low-cost index (0.20) minimises packaging expenditure for a high-volume, short-shelf-life product.'),

-- Potato Chips → Metallized PET + PE
('50000000-0000-0000-0000-000000000003',
 '00000000-0000-0000-0000-000000000002',
 '20000000-0000-0000-0000-000000000003',
 '30000000-0000-0000-0000-000000000003',
 '40000000-0000-0000-0000-000000000003',
 '10000000-0000-0000-0000-000000000019',  -- MET-PET-PE
 '["10000000-0000-0000-0000-000000000006","10000000-0000-0000-0000-000000000007"]',
 'Pouch — Metallized PET + PE Laminate 58 µm',
 '{"moisture_barrier":0.93,"oxygen_barrier":0.91,"light_barrier":0.96,"thermal_resistance":0.60,"mechanical_strength":0.82}',
 58.0,
 'Store at ambient temperature away from direct sunlight.',
 240, 360,
 '["Not recyclable — premium performance comes at an environmental cost","Nitrogen flush required to maintain crispness inside pouch","Seal integrity is critical; any pinhole causes rapid staling"]',
 45.0, 68.0, 92.0, 94.0,
 'Metallized PET + PE Laminate is recommended for Potato Chips because the product has high fat content (35%), high oxygen and light sensitivity, and a target shelf life of 6 months. The metallized PET layer provides near-total barrier to oxygen (0.91), moisture (0.93), and light (0.96), protecting fat from oxidative rancidity. The PE inner layer provides heat-sealability and food-contact compliance. This is the industry-standard choice for premium snack packaging globally.')

ON CONFLICT DO NOTHING;
