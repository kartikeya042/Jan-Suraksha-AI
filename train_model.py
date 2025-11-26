# train_model.py (Indian Edition 🇮🇳) - WITH DETAILED RESULTS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
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

# 3. Features
X = df[['age', 'bmi', 'daily_income_inr', 'children', 'smoker_tobacco', 'occupation', 'tier_city']]
y = df['recommended_policy']

# 4. Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Model... (This might take a second)")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. DETAILED EVALUATION ON TEST DATA
print("\n" + "="*40)
print("🔎 MODEL TEST RESULTS")
print("="*40)

# Make predictions on the test set (The 1000 hidden users)
y_pred = model.predict(X_test)

# Get the actual names of the policies (not just numbers 0, 1, 2)
class_names = target_le.classes_

# Print the full report
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=class_names))

print("-" * 60)

# Print Accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Overall Model Accuracy: {accuracy * 100:.2f}%")
print("-" * 60)

# 6. Save
joblib.dump(model, 'policy_model.pkl')
joblib.dump(encoders, 'encoders.pkl')
print("\n💾 Model saved to 'policy_model.pkl'")