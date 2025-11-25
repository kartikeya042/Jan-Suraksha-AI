# train_model.py (Indian Edition 🇮🇳)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load Data
df = pd.read_csv('insurance_dataset.csv')

# 2. Preprocessing
encoders = {}
categorical_cols = ['smoker_tobacco', 'occupation', 'tier_city']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Target Variable
target_le = LabelEncoder()
df['recommended_policy'] = target_le.fit_transform(df['recommended_policy'])
encoders['target'] = target_le

# 3. Features (Ensure these match the app.py input order!)
X = df[['age', 'bmi', 'daily_income_inr', 'children', 'smoker_tobacco', 'occupation', 'tier_city']]
y = df['recommended_policy']

# 4. Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Save
joblib.dump(model, 'policy_model.pkl')
joblib.dump(encoders, 'encoders.pkl')
print(f"🇮🇳 Indian Model Trained. Accuracy: {model.score(X_test, y_test):.2f}")