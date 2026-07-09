import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - XGBOOST POLLUTION V2 (BALANCED)")
print("=" * 60)

# LOAD POLLUTION DATASET
print("\nLoading pollution dataset...")
df = pd.read_csv('../data/water_pollution_clean.csv')
print(f"Shape: {df.shape}")

# STEP 1: CREATE BETTER TARGET COLUMN
print("\nStep 1: Creating balanced Risk Level target...")

# Use percentile based splitting for balanced classes
cholera  = df['Cholera Cases per 100,000 people']
typhoid  = df['Typhoid Cases per 100,000 people']
diarrhea = df['Diarrheal Cases per 100,000 people']

# Combined disease score
df['Disease_Score'] = (cholera + typhoid + diarrhea) / 3

# Split into 3 equal thirds using percentiles
low_thresh  = df['Disease_Score'].quantile(0.33)
high_thresh = df['Disease_Score'].quantile(0.66)

def assign_risk(score):
    if score <= low_thresh:
        return 0   # Low Risk
    elif score <= high_thresh:
        return 1   # Medium Risk
    else:
        return 2   # High Risk

df['Risk_Level'] = df['Disease_Score'].apply(assign_risk)
print(f"Risk Level distribution (balanced):")
print(df['Risk_Level'].value_counts())

# STEP 2: PREPARE FEATURES
print("\nStep 2: Preparing features...")
le = LabelEncoder()
df['Water_Source_Encoded'] = le.fit_transform(df['Water Source Type'])
df['Treatment_Encoded']    = le.fit_transform(df['Water Treatment Method'])
df['Region_Encoded']       = le.fit_transform(df['Region'])

feature_cols = [
    'Contaminant Level (ppm)',
    'pH Level',
    'Turbidity (NTU)',
    'Dissolved Oxygen (mg/L)',
    'Nitrate Level (mg/L)',
    'Lead Concentration (µg/L)',
    'Bacteria Count (CFU/mL)',
    'Access to Clean Water (% of Population)',
    'GDP per Capita (USD)',
    'Healthcare Access Index (0-100)',
    'Urbanization Rate (%)',
    'Sanitation Coverage (% of Population)',
    'Rainfall (mm per year)',
    'Temperature (°C)',
    'Population Density (people per km²)',
    'Water_Source_Encoded',
    'Treatment_Encoded',
    'Region_Encoded'
]

X = df[feature_cols]
y = df['Risk_Level']

# STEP 3: TRAIN TEST SPLIT
print("\nStep 3: Train/Test Split...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# STEP 4: TRAIN XGBOOST WITH CLASS WEIGHTS
print("\nStep 4: Training XGBoost with balanced classes...")
xgb = XGBClassifier(
    random_state=42,
    eval_metric='mlogloss',
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False
)
xgb.fit(X_train, y_train)
y_pred  = xgb.predict(X_test)
acc     = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc*100:.2f}%")

# STEP 5: FINAL EVALUATION
print("\nStep 5: Final Evaluation...")
print(f"Final Accuracy: {acc*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred,
      target_names=['Low Risk', 'Medium Risk', 'High Risk']))

# STEP 6: CONFUSION MATRIX
print("\nStep 6: Saving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.title('XGBoost V2 - Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1,2], ['Low','Medium','High'])
plt.yticks([0,1,2], ['Low','Medium','High'])
for i in range(3):
    for j in range(3):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=14, color='black')
plt.tight_layout()
plt.savefig('../reports/xgb_v2_confusion_matrix.png', dpi=150)
plt.close()
print("Saved: xgb_v2_confusion_matrix.png")

# STEP 7: FEATURE IMPORTANCE
print("\nStep 7: Feature Importance Plot...")
importance = pd.Series(xgb.feature_importances_, index=feature_cols)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(12, 8))
importance.plot(kind='barh', color='steelblue')
plt.title('XGBoost V2 - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/xgb_v2_feature_importance.png', dpi=150)
plt.close()
print("Saved: xgb_v2_feature_importance.png")

# STEP 8: SAVE MODEL
print("\nStep 8: Saving Model...")
with open('../models/xgb_pollution_v2_model.pkl', 'wb') as f:
    pickle.dump(xgb, f)
print("Saved: xgb_pollution_v2_model.pkl")

print("\n" + "=" * 60)
print("  XGBOOST V2 COMPLETE!")
print(f"  Final Accuracy: {acc*100:.2f}%")
print("  Next: LSTM Forecasting")
print("=" * 60)