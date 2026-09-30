import os
import numpy as np
import pandas as pd

def generate_crop_data():
    np.random.seed(42)
    
    # Define States and their Districts
    state_districts = {
        'Gujarat': [
            'Ahmedabad', 'Amreli', 'Anand', 'Banaskantha', 'Bharuch', 'Bhavnagar',
            'Gandhinagar', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mehsana',
            'Narmada', 'Navsari', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha',
            'Surat', 'Surendranagar', 'Vadodara', 'Valsad'
        ],
        'Uttar Pradesh': [
            'Agra', 'Aligarh', 'Allahabad', 'Bareilly', 'Gorakhpur', 'Kanpur', 
            'Lucknow', 'Varanasi', 'Meerut', 'Mathura', 'Moradabad'
        ],
        'Punjab': ['Amritsar', 'Bhatinda', 'Firozepur', 'Jalandhar', 'Ludhiana', 'Patiala', 'Sangrur'],
        'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Jalgaon', 'Nashik', 'Pune', 'Solapur', 'Nagpur'],
        'Madhya Pradesh': ['Bhopal', 'Gwalior', 'Indore', 'Jabalpur', 'Ujjain', 'Sagar', 'Vidisha', 'Rewa'],
        'West Bengal': ['Burdwan', 'Hooghly', 'Murshidabad', 'Nadia', 'Bankura', 'Birbhum', 'Midnapore'],
        'Rajasthan': ['Bikaner', 'Jaipur', 'Jodhpur', 'Kota', 'Sri Ganganagar', 'Udaipur', 'Alwar', 'Barmer'],
        'Tamil Nadu': ['Coimbatore', 'Madurai', 'Salem', 'Thanjavur', 'Tiruchirappalli', 'Erode', 'Vellore'],
        'Karnataka': ['Belgaum', 'Bellary', 'Dharwad', 'Mysore', 'Shimoga', 'Gulbarga', 'Hassan'],
        'Andhra Pradesh': ['Guntur', 'Krishna', 'Kurnool', 'West Godavari', 'East Godavari', 'Anantapur'],
        'Haryana': ['Ambala', 'Hisar', 'Karnal', 'Rohtak', 'Sirsa', 'Sonipat'],
        'Bihar': ['Gaya', 'Muzaffarpur', 'Patna', 'Purnia', 'Rohtas', 'Bhagalpur'],
        'Assam': ['Cachar', 'Dibrugarh', 'Kamrup', 'Nagaon', 'Tinsukia'],
        'Odisha': ['Balasore', 'Cuttack', 'Ganjam', 'Puri', 'Sambalpur'],
        'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Palakkad', 'Thiruvananthapuram']
    }

    # State specific crop probability preferences
    state_crop_prefs = {
        'Gujarat': ['Groundnut', 'Cotton(lint)', 'Bajra', 'Wheat', 'Castor seed', 'Sesame', 'Tobacco', 'Cumin', 'Jowar', 'Sugarcane', 'Rice', 'Maize'],
        'Uttar Pradesh': ['Sugarcane', 'Wheat', 'Rice', 'Potato', 'Maize', 'Mustard', 'Gram', 'Arhar/Tur', 'Barley'],
        'Punjab': ['Wheat', 'Rice', 'Cotton(lint)', 'Maize', 'Sugarcane', 'Potato', 'Mustard'],
        'Maharashtra': ['Sugarcane', 'Cotton(lint)', 'Soyabean', 'Jowar', 'Bajra', 'Arhar/Tur', 'Gram', 'Rice', 'Onion'],
        'Madhya Pradesh': ['Soyabean', 'Wheat', 'Gram', 'Mustard', 'Maize', 'Arhar/Tur', 'Cotton(lint)'],
        'West Bengal': ['Rice', 'Jute', 'Potato', 'Sugarcane', 'Maize', 'Mustard', 'Sesame'],
        'Rajasthan': ['Bajra', 'Mustard', 'Wheat', 'Gram', 'Guar seed', 'Cumin', 'Coriander'],
        'Tamil Nadu': ['Rice', 'Sugarcane', 'Coconut', 'Groundnut', 'Maize', 'Cotton(lint)', 'Banana'],
        'Karnataka': ['Sugarcane', 'Rice', 'Maize', 'Cotton(lint)', 'Jowar', 'Groundnut', 'Ragi', 'Sunflower'],
        'Andhra Pradesh': ['Rice', 'Groundnut', 'Cotton(lint)', 'Maize', 'Sugarcane', 'Chillies', 'Tobacco']
    }
    
    default_crops = ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Pulses', 'Oilseeds', 'Potato', 'Onion']

    # Crop parameters: base yield (tonnes/hectare), yield std, base area range (ha), season options
    crop_info = {
        'Sugarcane': {'yield_mean': 72.0, 'yield_std': 12.0, 'area_min': 500, 'area_max': 45000, 'seasons': ['Whole Year']},
        'Potato': {'yield_mean': 22.0, 'yield_std': 4.0, 'area_min': 200, 'area_max': 15000, 'seasons': ['Winter', 'Rabi']},
        'Onion': {'yield_mean': 17.0, 'yield_std': 3.5, 'area_min': 150, 'area_max': 12000, 'seasons': ['Rabi', 'Kharif']},
        'Rice': {'yield_mean': 3.2, 'yield_std': 0.6, 'area_min': 1000, 'area_max': 60000, 'seasons': ['Kharif', 'Winter', 'Summer']},
        'Wheat': {'yield_mean': 3.8, 'yield_std': 0.7, 'area_min': 1200, 'area_max': 55000, 'seasons': ['Rabi']},
        'Maize': {'yield_mean': 2.8, 'yield_std': 0.5, 'area_min': 400, 'area_max': 25000, 'seasons': ['Kharif', 'Rabi']},
        'Groundnut': {'yield_mean': 1.9, 'yield_std': 0.4, 'area_min': 500, 'area_max': 35000, 'seasons': ['Kharif', 'Summer']},
        'Cotton(lint)': {'yield_mean': 1.6, 'yield_std': 0.35, 'area_min': 800, 'area_max': 48000, 'seasons': ['Kharif']},
        'Bajra': {'yield_mean': 1.4, 'yield_std': 0.3, 'area_min': 600, 'area_max': 30000, 'seasons': ['Kharif']},
        'Castor seed': {'yield_mean': 1.8, 'yield_std': 0.35, 'area_min': 300, 'area_max': 20000, 'seasons': ['Kharif', 'Whole Year']},
        'Sesame': {'yield_mean': 0.55, 'yield_std': 0.12, 'area_min': 100, 'area_max': 10000, 'seasons': ['Kharif', 'Summer']},
        'Tobacco': {'yield_mean': 1.7, 'yield_std': 0.3, 'area_min': 150, 'area_max': 8000, 'seasons': ['Rabi', 'Whole Year']},
        'Cumin': {'yield_mean': 0.65, 'yield_std': 0.15, 'area_min': 200, 'area_max': 14000, 'seasons': ['Rabi']},
        'Jowar': {'yield_mean': 1.2, 'yield_std': 0.25, 'area_min': 500, 'area_max': 28000, 'seasons': ['Kharif', 'Rabi']},
        'Soyabean': {'yield_mean': 1.5, 'yield_std': 0.3, 'area_min': 800, 'area_max': 40000, 'seasons': ['Kharif']},
        'Gram': {'yield_mean': 1.1, 'yield_std': 0.2, 'area_min': 300, 'area_max': 22000, 'seasons': ['Rabi']},
        'Arhar/Tur': {'yield_mean': 0.95, 'yield_std': 0.18, 'area_min': 250, 'area_max': 18000, 'seasons': ['Kharif']},
        'Mustard': {'yield_mean': 1.35, 'yield_std': 0.25, 'area_min': 400, 'area_max': 25000, 'seasons': ['Rabi']},
        'Jute': {'yield_mean': 2.4, 'yield_std': 0.4, 'area_min': 500, 'area_max': 30000, 'seasons': ['Kharif']},
        'Coconut': {'yield_mean': 9.5, 'yield_std': 1.8, 'area_min': 300, 'area_max': 20000, 'seasons': ['Whole Year']},
        'Guar seed': {'yield_mean': 0.7, 'yield_std': 0.15, 'area_min': 500, 'area_max': 30000, 'seasons': ['Kharif']},
        'Chillies': {'yield_mean': 1.8, 'yield_std': 0.35, 'area_min': 100, 'area_max': 9000, 'seasons': ['Kharif', 'Rabi']},
        'Barley': {'yield_mean': 2.1, 'yield_std': 0.4, 'area_min': 200, 'area_max': 12000, 'seasons': ['Rabi']},
        'Ragi': {'yield_mean': 1.6, 'yield_std': 0.3, 'area_min': 300, 'area_max': 15000, 'seasons': ['Kharif']},
        'Sunflower': {'yield_mean': 0.9, 'yield_std': 0.2, 'area_min': 200, 'area_max': 10000, 'seasons': ['Kharif', 'Rabi']},
        'Banana': {'yield_mean': 42.0, 'yield_std': 8.0, 'area_min': 150, 'area_max': 10000, 'seasons': ['Whole Year']}
    }

    years = list(range(1997, 2021))
    records = []

    for year in years:
        # Technological progress multiplier (1.0 in 1997 to ~1.35 in 2020)
        tech_multiplier = 1.0 + (year - 1997) * 0.015
        
        for state, districts in state_districts.items():
            crops = state_crop_prefs.get(state, default_crops)
            
            # Pick a subset of crops for each district each year
            for dist in districts:
                # District active crops
                dist_crops = np.random.choice(crops, size=np.random.randint(3, min(8, len(crops)+1)), replace=False)
                
                for crop in dist_crops:
                    info = crop_info.get(crop, {'yield_mean': 1.5, 'yield_std': 0.3, 'area_min': 300, 'area_max': 15000, 'seasons': ['Kharif', 'Rabi']})
                    season = np.random.choice(info['seasons'])
                    
                    # Generate Area
                    area = np.random.uniform(info['area_min'], info['area_max'])
                    
                    # Gujarat boost for Groundnut, Cotton, Castor, Sesame, Tobacco
                    gujarat_boost = 1.0
                    if state == 'Gujarat' and crop in ['Groundnut', 'Cotton(lint)', 'Castor seed', 'Sesame', 'Tobacco', 'Cumin', 'Bajra']:
                        gujarat_boost = 1.25 + np.random.uniform(-0.05, 0.15)
                        area *= 1.3
                    
                    # Yield calculation with noise & tech trend
                    actual_yield = max(0.1, np.random.normal(info['yield_mean'], info['yield_std']) * tech_multiplier * gujarat_boost)
                    production = area * actual_yield
                    
                    records.append({
                        'State_Name': state,
                        'District_Name': dist,
                        'Crop_Year': year,
                        'Season': season,
                        'Crop': crop,
                        'Area': round(area, 2),
                        'Production': round(production, 2)
                    })

    df = pd.DataFrame(records)
    
    # Introduce small realistic data anomalies for cleaning phase demonstration
    # 1. ~1.5% missing production values (as noted in project prompt)
    missing_indices = np.random.choice(df.index, size=int(len(df) * 0.015), replace=False)
    df.loc[missing_indices, 'Production'] = np.nan
    
    # 2. Add column header space/case variations as in Kaggle dataset
    # Standard column names: 'State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Area', 'Production'
    
    os.makedirs('data', exist_ok=True)
    csv_path = os.path.join('data', 'crop_production.csv')
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated successfully at {csv_path} with {len(df)} rows.")

if __name__ == '__main__':
    generate_crop_data()
