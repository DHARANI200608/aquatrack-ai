import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - XGBOOST ON POLLUTION DATASET")
print("=" * 60)

# LOAD POLLUTION DATASET
print("\nLoading pollution dataset...")
df = pd.read_csv('../data/water_pollution_clean.csv')
print(f"Shape: {df.shape}")

# STEP 1: CREATE TARGET COLUMN
print("\nStep 1: Creating Risk Level target column...")
def assign_risk(row):
    score = (
        row['Cholera Cases per 100,000 people'] * 0.4 +
        row['Typhoid Cases per 100,000 people'] * 0.3 +
        row['Diarrheal Cases per 100,000 people'] * 0.3
    )
    if score < 50:
        return 0   # Low Risk
    elif score < 150:
        return 1   # Medium Risk
    else:
        return 2   # High Risk

df['Risk_Level'] = df.apply(assign_risk, axis=1)
print(f"Risk Level distribution:")
print(df['Risk_Level'].value_counts())

# STEP 2: PREPARE FEATURES
print("\nStep 2: Preparing features...")
le = LabelEncoder()
df['Water_Source_Encoded']    = le.fit_transform(df['Water Source Type'])
df['Treatment_Encoded']       = le.fit_transform(df['Water Treatment Method'])
df['Region_Encoded']          = le.fit_transform(df['Region'])

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

# STEP 4: TRAIN BASIC XGBOOST
print("\nStep 4: Training XGBoost...")
xgb = XGBClassifier(random_state=42, eval_metric='mlogloss')
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Basic Accuracy: {acc*100:.2f}%")

# STEP 5: HYPERPARAMETER TUNING
print("\nStep 5: Tuning Hyperparameters (takes 2-3 mins)...")
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1, 0.2],
}
grid_search = GridSearchCV(
    XGBClassifier(random_state=42, eval_metric='mlogloss'),
    param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best CV Accuracy: {grid_search.best_score_*100:.2f}%")

# STEP 6: FINAL EVALUATION
print("\nStep 6: Final Evaluation...")
best_xgb    = grid_search.best_estimator_
y_pred_best = best_xgb.predict(X_test)
final_acc   = accuracy_score(y_test, y_pred_best)
print(f"Final Accuracy: {final_acc*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_best,
      target_names=['Low Risk', 'Medium Risk', 'High Risk']))

# STEP 7: CONFUSION MATRIX
print("\nStep 7: Saving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.title('XGBoost Pollution - Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1,2], ['Low','Medium','High'])
plt.yticks([0,1,2], ['Low','Medium','High'])
for i in range(3):
    for j in range(3):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=14, color='black')
plt.tight_layout()
plt.savefig('../reports/xgb_pollution_confusion_matrix.png', dpi=150)
plt.close()
print("Saved: xgb_pollution_confusion_matrix.png")

# STEP 8: FEATURE IMPORTANCE
print("\nStep 8: Feature Importance Plot...")
importance = pd.Series(best_xgb.feature_importances_, index=feature_cols)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(12, 8))
importance.plot(kind='barh', color='steelblue')
plt.title('XGBoost Pollution - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/xgb_pollution_feature_importance.png', dpi=150)
plt.close()
print("Saved: xgb_pollution_feature_importance.png")

# STEP 9: SAVE MODEL
print("\nStep 9: Saving Model...")
with open('../models/xgb_pollution_model.pkl', 'wb') as f:
    pickle.dump(best_xgb, f)
print("Saved: xgb_pollution_model.pkl")

print("\n" + "=" * 60)
print("  XGBOOST POLLUTION MODEL COMPLETE!")
print(f"  Final Accuracy: {final_acc*100:.2f}%")
print("  Next: LSTM Forecasting")
print("=" * 60)