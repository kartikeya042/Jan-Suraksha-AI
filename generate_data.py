# generate_data.py
import pandas as pd
import numpy as np
import random

def generate_insurance_data(num_samples=5000):
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 65, size=num_samples),
        'bmi': np.random.normal(25, 4, size=num_samples).round(1),
        'daily_income_inr': np.random.randint(250, 2000, size=num_samples),
        'children': np.random.randint(0, 5, size=num_samples),
        'smoker': np.random.choice(['Yes', 'No'], size=num_samples, p=[0.3, 0.7]),
        'occupation': np.random.choice(
            ['Construction Worker', 'Farmer', 'Street Vendor', 'Driver', 'Factory Worker', 'Shop Assistant'], 
            size=num_samples
        ),
        'medical_history': np.random.choice(['None', 'Diabetes', 'BP', 'Respiratory'], size=num_samples, p=[0.7, 0.1, 0.1, 0.1])
    }
    
    df = pd.DataFrame(data)

    # --- THE LOGIC: Assigning the "Correct" Policy based on rules ---
    def assign_policy(row):
        # Rule 1: High Physical Risk Jobs -> Accidental Death Cover
        if row['occupation'] in ['Construction Worker', 'Driver', 'Factory Worker']:
            return 'Accidental Death & Disability Plan'
        
        # Rule 2: Very Low Income -> Government Subsidized (e.g., PMJJBY type)
        if row['daily_income_inr'] < 500:
            return 'Govt. Subsidized Micro-Term'
        
        # Rule 3: High Dependents -> Family Income Benefit
        if row['children'] >= 3:
            return 'Family Income Protection Plan'
        
        # Rule 4: Smokers or High BMI -> Critical Illness add-on needed
        if row['smoker'] == 'Yes' or row['bmi'] > 30 or row['medical_history'] != 'None':
            return 'High-Risk Critical Illness Plan'
        
        # Default for healthy, moderate income
        return 'Standard Micro-Endowment Plan'

    df['recommended_policy'] = df.apply(assign_policy, axis=1)
    
    # Save to CSV
    df.to_csv('insurance_dataset.csv', index=False)
    print("Dataset generated successfully: 'insurance_dataset.csv'")

if __name__ == "__main__":
    generate_insurance_data()