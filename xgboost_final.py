import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - XGBOOST FINAL MODEL")
print("=" * 60)

# LOAD POLLUTION DATASET
print("\nLoading pollution dataset...")
df = pd.read_csv('../data/water_pollution_clean.csv')
print(f"Shape: {df.shape}")

# STEP 1: CREATE TARGET FROM WATER ACCESS
print("\nStep 1: Creating target column...")
# Predict if a region has Good or Poor water safety
# Based on Access to Clean Water percentage
median_access = df['Access to Clean Water (% of Population)'].median()
df['Water_Safety'] = (df['Access to Clean Water (% of Population)'] >= median_access).astype(int)
print(f"Median water access: {median_access:.2f}%")
print(f"Target distribution:")
print(df['Water_Safety'].value_counts())

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
    'Diarrheal Cases per 100,000 people',
    'Cholera Cases per 100,000 people',
    'Typhoid Cases per 100,000 people',
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
y = df['Water_Safety']

# STEP 3: TRAIN TEST SPLIT
print("\nStep 3: Train/Test Split...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# STEP 4: TRAIN XGBOOST
print("\nStep 4: Training XGBoost...")
xgb = XGBClassifier(
    random_state=42,
    eval_metric='logloss',
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8
)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"Final Accuracy: {acc*100:.2f}%")

# STEP 5: CLASSIFICATION REPORT
print("\nStep 5: Classification Report...")
print(classification_report(y_test, y_pred,
      target_names=['Poor Safety', 'Good Safety']))

# STEP 6: CONFUSION MATRIX
print("\nStep 6: Saving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.title('XGBoost Final - Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1], ['Poor Safety','Good Safety'])
plt.yticks([0,1], ['Poor Safety','Good Safety'])
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=18, color='black')
plt.tight_layout()
plt.savefig('../reports/xgb_final_confusion_matrix.png', dpi=150)
plt.close()
print("Saved: xgb_final_confusion_matrix.png")

# STEP 7: FEATURE IMPORTANCE
print("\nStep 7: Feature Importance Plot...")
importance = pd.Series(xgb.feature_importances_, index=feature_cols)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(12, 8))
importance.plot(kind='barh', color='steelblue')
plt.title('XGBoost Final - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/xgb_final_feature_importance.png', dpi=150)
plt.close()
print("Saved: xgb_final_feature_importance.png")

# STEP 8: SAVE MODEL
print("\nStep 8: Saving Model...")
with open('../models/xgb_final_model.pkl', 'wb') as f:
    pickle.dump(xgb, f)
print("Saved: xgb_final_model.pkl")

print("\n" + "=" * 60)
print("  XGBOOST FINAL MODEL COMPLETE!")
print(f"  Final Accuracy: {acc*100:.2f}%")
print("  Next: SHAP Explainability")
print("=" * 60)