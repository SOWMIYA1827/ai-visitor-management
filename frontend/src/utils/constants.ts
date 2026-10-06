export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'PackSmart AI';
export const APP_SUBTITLE = 'AI-Powered Food Packaging Recommendation System';

export const FOOD_CATEGORIES = [
  { value: 'fruits', label: 'Fruits' },
  { value: 'vegetables', label: 'Vegetables' },
  { value: 'cereals', label: 'Cereals & Grains' },
  { value: 'pulses', label: 'Pulses & Legumes' },
  { value: 'spices', label: 'Spices & Herbs' },
  { value: 'dairy', label: 'Dairy Products' },
  { value: 'meat', label: 'Meat & Poultry' },
  { value: 'fish', label: 'Fish & Seafood' },
  { value: 'bakery', label: 'Bakery Products' },
  { value: 'snacks', label: 'Snacks & Namkeen' },
  { value: 'processed_food', label: 'Processed Food' },
  { value: 'beverages', label: 'Beverages' },
  { value: 'other', label: 'Other' },
];

export const SENSITIVITY_OPTIONS = [
  { value: 'low', label: 'Low', color: 'green' },
  { value: 'medium', label: 'Medium', color: 'yellow' },
  { value: 'high', label: 'High', color: 'red' },
];

export const PERISHABILITY_OPTIONS = [
  { value: 'low', label: 'Low (months)' },
  { value: 'medium', label: 'Medium (weeks)' },
  { value: 'high', label: 'High (days)' },
];

export const TRANSPORTATION_TYPES = [
  { value: 'road', label: 'Road' },
  { value: 'rail', label: 'Rail' },
  { value: 'air', label: 'Air' },
  { value: 'sea', label: 'Sea' },
];

export const PACKAGING_TYPES = [
  { value: 'pouch', label: 'Pouch' },
  { value: 'bag', label: 'Bag' },
  { value: 'bottle', label: 'Bottle' },
  { value: 'tray', label: 'Tray' },
  { value: 'box', label: 'Box' },
  { value: 'vacuum_pack', label: 'Vacuum Pack' },
  { value: 'map', label: 'Modified Atmosphere (MAP)' },
  { value: 'flexible', label: 'Flexible Packaging' },
  { value: 'rigid', label: 'Rigid Packaging' },
];

export const PRIORITY_OPTIONS = [
  { value: 'balanced', label: '⚖️ Balanced' },
  { value: 'low_cost', label: '💰 Low Cost' },
  { value: 'max_shelf_life', label: '📅 Maximum Shelf Life' },
  { value: 'food_safety', label: '🛡️ Food Safety' },
  { value: 'sustainability', label: '🌿 Sustainability' },
];

export const ECO_PREFERENCES = [
  { value: 'no_preference', label: 'No Preference' },
  { value: 'recyclable', label: '♻️ Recyclable' },
  { value: 'biodegradable', label: '🌱 Biodegradable' },
  { value: 'compostable', label: '🍃 Compostable' },
  { value: 'bio_based', label: '🌾 Bio-based' },
];

export const USER_TYPES = [
  { value: 'farmer', label: 'Farmer' },
  { value: 'food_processor', label: 'Food Processor' },
  { value: 'small_business', label: 'Small Food Business' },
  { value: 'manufacturer', label: 'Packaging Manufacturer' },
  { value: 'researcher', label: 'Researcher' },
];

export const PACKAGE_SIZES = [
  { value: 'small', label: 'Small (< 100g)' },
  { value: 'medium', label: 'Medium (100g – 500g)' },
  { value: 'large', label: 'Large (500g – 2kg)' },
  { value: 'bulk', label: 'Bulk (> 2kg)' },
];

export const DISCLAIMER = 
  'PackSmart AI provides preliminary packaging recommendations based on the provided information and available model/knowledge-base data. ' +
  'Recommendations are not a substitute for laboratory testing, regulatory compliance, food-contact certification, shelf-life studies, or expert packaging validation.';
