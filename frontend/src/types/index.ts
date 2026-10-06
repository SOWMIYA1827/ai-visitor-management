// ─── Auth ────────────────────────────────────────────────────────────────────

export type UserType = 'farmer' | 'food_processor' | 'small_business' | 'manufacturer' | 'researcher' | 'admin';

export interface User {
  id: string;
  email: string;
  full_name: string;
  user_type: UserType;
  organization?: string;
  phone_number?: string;
  is_admin: boolean;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  full_name: string;
  email: string;
  password: string;
  user_type: UserType;
  organization?: string;
  phone_number?: string;
}

// ─── Food ────────────────────────────────────────────────────────────────────

export type FoodCategory =
  | 'fruits' | 'vegetables' | 'cereals' | 'pulses' | 'spices'
  | 'dairy' | 'meat' | 'fish' | 'bakery' | 'snacks'
  | 'processed_food' | 'beverages' | 'other';

export type SensitivityLevel = 'low' | 'medium' | 'high';
export type PerishabilityLevel = 'low' | 'medium' | 'high';

export interface FoodProfileCreate {
  food_name: string;
  category: FoodCategory;
  moisture_content?: number;
  ph?: number;
  fat_content?: number;
  protein_content?: number;
  water_activity?: number;
  respiration_rate?: number;
  perishability?: PerishabilityLevel;
  oxygen_sensitivity?: SensitivityLevel;
  moisture_sensitivity?: SensitivityLevel;
  light_sensitivity?: SensitivityLevel;
  temperature_sensitivity?: SensitivityLevel;
  odor_sensitivity?: SensitivityLevel;
  microbial_sensitivity?: SensitivityLevel;
}

export interface FoodProfile extends FoodProfileCreate {
  id: string;
  user_id: string;
  created_at: string;
}

// ─── Packaging ───────────────────────────────────────────────────────────────

export type MaterialCategory = 'plastic' | 'paper' | 'metal' | 'glass' | 'biodegradable' | 'multilayer' | 'composite';

export interface PackagingMaterial {
  id: string;
  name: string;
  material_code: string;
  category: MaterialCategory;
  moisture_barrier: number;
  oxygen_barrier: number;
  light_barrier: number;
  thermal_resistance: number;
  mechanical_strength: number;
  food_contact_safe: boolean;
  recyclable: boolean;
  biodegradable: boolean;
  compostable: boolean;
  bio_based: boolean;
  cost_index: number;
  typical_thickness_min_um?: number;
  typical_thickness_max_um?: number;
  description?: string;
  suitable_for?: string[];
  created_at: string;
}

// ─── Recommendation ──────────────────────────────────────────────────────────

export type TransportationType = 'road' | 'rail' | 'air' | 'sea';
export type PackagingType = 'pouch' | 'bag' | 'bottle' | 'tray' | 'box' | 'vacuum_pack' | 'map' | 'flexible' | 'rigid';
export type Priority = 'low_cost' | 'max_shelf_life' | 'food_safety' | 'sustainability' | 'balanced';
export type EcoPreference = 'no_preference' | 'recyclable' | 'biodegradable' | 'compostable' | 'bio_based';

export interface StorageConditionsInput {
  storage_temp?: number;
  storage_humidity?: number;
  storage_duration_days?: number;
  transportation_duration_days?: number;
  transportation_type?: TransportationType;
  cold_chain_required: boolean;
}

export interface PackagingRequirementsInput {
  required_shelf_life_days?: number;
  package_size?: string;
  package_quantity?: number;
  budget?: number;
  packaging_type?: PackagingType;
  priority: Priority;
  eco_preference: EcoPreference;
}

export interface RecommendationRequest {
  food_profile?: FoodProfileCreate;
  food_profile_id?: string;
  storage_conditions: StorageConditionsInput;
  packaging_requirements: PackagingRequirementsInput;
}

export interface BarrierProperties {
  moisture_barrier: number;
  oxygen_barrier: number;
  light_barrier: number;
  thermal_resistance: number;
  mechanical_strength: number;
}

export interface RiskItem {
  type: string;
  level: 'Low' | 'Medium' | 'High';
  mitigation: string;
}

export interface RecommendationResponse {
  id: string;
  user_id: string;
  food_profile_id: string;
  food_name?: string;
  primary_material_id?: string;
  primary_material?: PackagingMaterial;
  alternative_material_ids?: string[];
  alternative_materials?: PackagingMaterial[];
  packaging_structure?: string;
  barrier_properties?: BarrierProperties;
  recommended_thickness_um?: number;
  storage_conditions_recommended?: string;
  shelf_life_min_days?: number;
  shelf_life_max_days?: number;
  risk_factors?: string[];
  sustainability_score?: number;
  cost_score?: number;
  food_safety_score?: number;
  overall_score?: number;
  explanation?: string;
  created_at: string;
}

export interface RecommendationListItem {
  id: string;
  food_profile_id: string;
  food_name?: string;
  primary_material_name?: string;
  shelf_life_min_days?: number;
  shelf_life_max_days?: number;
  overall_score?: number;
  created_at: string;
}

// ─── Multi-step form state ───────────────────────────────────────────────────

export interface RecommendFormState {
  // Step 1
  food_name: string;
  category: FoodCategory;
  moisture_content: string;
  ph: string;
  fat_content: string;
  protein_content: string;
  water_activity: string;
  respiration_rate: string;
  perishability: PerishabilityLevel;
  // Step 2
  oxygen_sensitivity: SensitivityLevel;
  moisture_sensitivity: SensitivityLevel;
  light_sensitivity: SensitivityLevel;
  temperature_sensitivity: SensitivityLevel;
  odor_sensitivity: SensitivityLevel;
  microbial_sensitivity: SensitivityLevel;
  // Step 3
  storage_temp: string;
  storage_humidity: string;
  storage_duration_days: string;
  transportation_duration_days: string;
  transportation_type: TransportationType;
  cold_chain_required: boolean;
  // Step 4
  required_shelf_life_days: string;
  package_size: string;
  package_quantity: string;
  budget: string;
  packaging_type: PackagingType;
  // Step 5
  priority: Priority;
  eco_preference: EcoPreference;
}
