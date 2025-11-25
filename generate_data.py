# generate_data.py (Indian Edition 🇮🇳)
import pandas as pd
import numpy as np

def generate_indian_insurance_data(num_samples=5000):
    np.random.seed(42)
    
    # --- 1. Demographics specific to Indian Low-Income Sector ---
    occupations = [
        'Daily Wage Laborer (MNREGA)', 
        'Auto/Taxi Driver', 
        'Street Vendor (Rehdi)', 
        'Farmer (Kisan)', 
        'Security Guard', 
        'Delivery Partner (Gig Worker)', 
        'Small Shopkeeper'
    ]
    
    data = {
        'age': np.random.randint(18, 60, size=num_samples),
        'bmi': np.random.normal(24, 3.5, size=num_samples).round(1),
        # Daily income between ₹200 and ₹1500
        'daily_income_inr': np.random.randint(200, 1500, size=num_samples), 
        'children': np.random.randint(0, 4, size=num_samples),
        # Tobacco usage is higher in some demographics, critical for insurance
        'smoker_tobacco': np.random.choice(['Yes', 'No'], size=num_samples, p=[0.4, 0.6]),
        'occupation': np.random.choice(occupations, size=num_samples),
        'tier_city': np.random.choice(['Tier-1', 'Tier-2', 'Rural'], size=num_samples)
    }
    
    df = pd.DataFrame(data)

    # --- 2. The Indian Logic (Mapping to Real Schemes) ---
    def assign_indian_policy(row):
        
        # SCHEME 1: Pradhan Mantri Suraksha Bima Yojana (PMSBY)
        # Logic: High risk of accident, very low income.
        if row['occupation'] in ['Daily Wage Laborer (MNREGA)', 'Auto/Taxi Driver', 'Delivery Partner (Gig Worker)']:
            return 'PMSBY (Accidental Cover - ₹20/year)'
        
        # SCHEME 2: Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)
        # Logic: Stable but low income, needs pure life cover.
        if row['daily_income_inr'] < 500 and row['age'] < 50:
            return 'PMJJBY (Life Cover - ₹436/year)'
        
        # SCHEME 3: Saral Jeevan Bima (Standard Term)
        # Logic: Better income (Shopkeepers), can afford standard term insurance.
        if row['daily_income_inr'] > 800:
            return 'Saral Jeevan Bima (Standard Term)'
        
        # SCHEME 4: Rural Postal Life Insurance (RPLI)
        # Logic: Specifically for rural residents/farmers.
        if row['occupation'] == 'Farmer (Kisan)' or row['tier_city'] == 'Rural':
            return 'Gramin Dak Sevak (Rural Postal Life)'
        
        # Default fallback
        return 'Micro-Endowment (Chota Bachat)'

    df['recommended_policy'] = df.apply(assign_indian_policy, axis=1)
    
    df.to_csv('insurance_dataset.csv', index=False)
    print("🇮🇳 Indian Dataset generated: 'insurance_dataset.csv'")

if __name__ == "__main__":
    generate_indian_insurance_data()