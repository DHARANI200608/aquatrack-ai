import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - XGBOOST 90% MODEL")
print("=" * 60)

# LOAD DATASET
print("\nLoading waterQuality1 dataset...")
df = pd.read_csv('../data/waterQuality1.csv')
print(f"Shape before cleaning: {df.shape}")

# FIX 1 - Remove #NUM! rows
df = df[df['is_safe'] != '#NUM!']

# FIX 2 - Convert ALL columns to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# FIX 3 - Drop any remaining nulls
df = df.dropna()

print(f"Shape after cleaning: {df.shape}")
print(f"Target distribution:")
print(df['is_safe'].value_counts())

# FEATURES AND TARGET
X = df.drop('is_safe', axis=1)
y = df['is_safe'].astype(int)

# TRAIN TEST SPLIT
print("\nTrain/Test Split 80/20...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# TRAIN XGBOOST
print("\nTraining XGBoost...")
xgb = XGBClassifier(
    random_state=42,
    eval_metric='logloss',
    n_estimators=500,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=1,
    gamma=0
)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"\nFinal Accuracy: {acc*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred,
      target_names=['Not Safe', 'Safe']))

# CONFUSION MATRIX
print("\nSaving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.title('XGBoost 90% - Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1], ['Not Safe','Safe'])
plt.yticks([0,1], ['Not Safe','Safe'])
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=18, color='black')
plt.tight_layout()
plt.savefig('../reports/xgb_90_confusion_matrix.png', dpi=150)
plt.close()
print("Saved: xgb_90_confusion_matrix.png")

# FEATURE IMPORTANCE
print("\nFeature Importance Plot...")
importance = pd.Series(xgb.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(12, 8))
importance.plot(kind='barh', color='steelblue')
plt.title('XGBoost 90% - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/xgb_90_feature_importance.png', dpi=150)
plt.close()
print("Saved: xgb_90_feature_importance.png")

# SAVE MODEL
print("\nSaving Model...")
with open('../models/xgb_90_model.pkl', 'wb') as f:
    pickle.dump(xgb, f)
print("Saved: xgb_90_model.pkl")

print("\n" + "=" * 60)
print("  XGBOOST 90% MODEL COMPLETE!")
print(f"  Final Accuracy: {acc*100:.2f}%")
print("  Next: SHAP Explainability")
print("=" * 60)