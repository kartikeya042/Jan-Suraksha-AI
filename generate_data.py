# generate_data.py (Realistic Noise Edition 📉)
import pandas as pd
import numpy as np

def generate_indian_insurance_data(num_samples=5000):
    np.random.seed(42)
    
    occupations = [
        'Daily Wage Laborer (MNREGA)', 'Auto/Taxi Driver', 'Street Vendor (Rehdi)', 
        'Farmer (Kisan)', 'Security Guard', 'Delivery Partner (Gig Worker)', 'Small Shopkeeper'
    ]
    
    # 1. Generate Base Data
    data = {
        'age': np.random.randint(18, 60, size=num_samples),
        'bmi': np.random.normal(24, 3.5, size=num_samples).round(1),
        'daily_income_inr': np.random.randint(200, 1500, size=num_samples), 
        'children': np.random.randint(0, 4, size=num_samples),
        'smoker_tobacco': np.random.choice(['Yes', 'No'], size=num_samples, p=[0.4, 0.6]),
        'occupation': np.random.choice(occupations, size=num_samples),
        'tier_city': np.random.choice(['Tier-1', 'Tier-2', 'Rural'], size=num_samples)
    }
    
    df = pd.DataFrame(data)

    # 2. Assign "Logical" Policy (The Perfect World)
    def assign_policy_logic(row):
        # PMSBY for high risk
        if row['occupation'] in ['Daily Wage Laborer (MNREGA)', 'Auto/Taxi Driver', 'Delivery Partner (Gig Worker)']:
            return 'PMSBY (Accidental Cover - ₹20/year)'
        # PMJJBY for low income/young
        if row['daily_income_inr'] < 500 and row['age'] < 50:
            return 'PMJJBY (Life Cover - ₹436/year)'
        # Saral Jeevan for higher income
        if row['daily_income_inr'] > 800:
            return 'Saral Jeevan Bima (Standard Term)'
        # Postal Life for Rural/Farmers
        if row['occupation'] == 'Farmer (Kisan)' or row['tier_city'] == 'Rural':
            return 'Gramin Dak Sevak (Rural Postal Life)'
        # Fallback
        return 'Micro-Endowment (Chota Bachat)'

    df['recommended_policy'] = df.apply(assign_policy_logic, axis=1)

    # --- 3. THE NOISE INJECTION (Making it Human) ---
    # We will randomly change 15% of the answers to simulate human error/preference
    
    all_policies = [
        'PMSBY (Accidental Cover - ₹20/year)', 
        'PMJJBY (Life Cover - ₹436/year)', 
        'Saral Jeevan Bima (Standard Term)', 
        'Gramin Dak Sevak (Rural Postal Life)', 
        'Micro-Endowment (Chota Bachat)'
    ]
    
    # Select 7% of valid indices to randomize
    num_noise = int(0.07 * num_samples)
    noise_indices = np.random.choice(df.index, size=num_noise, replace=False)
    
    # For these people, force a random policy choice
    df.loc[noise_indices, 'recommended_policy'] = np.random.choice(all_policies, size=num_noise)

    # Save
    df.to_csv('insurance_dataset.csv', index=False)
    print(f"🇮🇳 Realistic Dataset Generated with 15% Noise: 'insurance_dataset.csv'")

if __name__ == "__main__":
    generate_indian_insurance_data()