import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - RANDOM FOREST MODEL")
print("=" * 60)

# ─────────────────────────────────────────────
# LOAD TRAIN/TEST DATA
# ─────────────────────────────────────────────
print("\n📂 Loading train/test data...")
X_train = pd.read_csv('../data/X_train.csv')
X_test  = pd.read_csv('../data/X_test.csv')
y_train = pd.read_csv('../data/y_train.csv').values.ravel()
y_test  = pd.read_csv('../data/y_test.csv').values.ravel()
print(f"✅ Train: {X_train.shape}, Test: {X_test.shape}")

# ─────────────────────────────────────────────
# STEP 1: TRAIN BASIC RANDOM FOREST
# ─────────────────────────────────────────────
print("\n📌 Step 1: Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Basic Accuracy: {acc*100:.2f}%")

# ─────────────────────────────────────────────
# STEP 2: HYPERPARAMETER TUNING
# ─────────────────────────────────────────────
print("\n📌 Step 2: Tuning Hyperparameters...")
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)
print(f"✅ Best Parameters: {grid_search.best_params_}")
print(f"✅ Best CV Accuracy: {grid_search.best_score_*100:.2f}%")

# ─────────────────────────────────────────────
# STEP 3: FINAL MODEL EVALUATION
# ─────────────────────────────────────────────
print("\n📌 Step 3: Final Model Evaluation...")
best_rf = grid_search.best_estimator_
y_pred_best = best_rf.predict(X_test)
final_acc = accuracy_score(y_test, y_pred_best)

print(f"\n✅ Final Accuracy : {final_acc*100:.2f}%")
print(f"\n📊 Classification Report:")
print(classification_report(y_test, y_pred_best,
      target_names=['Unsafe Water', 'Safe Water']))

# ─────────────────────────────────────────────
# STEP 4: CONFUSION MATRIX PLOT
# ─────────────────────────────────────────────
print("\n📌 Step 4: Saving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.title('Random Forest Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1], ['Unsafe','Safe'])
plt.yticks([0,1], ['Unsafe','Safe'])
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=18, color='black')
plt.tight_layout()
plt.savefig('../reports/rf_confusion_matrix.png', dpi=150)
plt.close()
print("✅ Saved: rf_confusion_matrix.png")

# ─────────────────────────────────────────────
# STEP 5: FEATURE IMPORTANCE PLOT
# ─────────────────────────────────────────────
print("\n📌 Step 5: Feature Importance Plot...")
importance = pd.Series(best_rf.feature_importances_, index=X_train.columns)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(10, 6))
importance.plot(kind='barh', color='steelblue')
plt.title('Random Forest - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/rf_feature_importance.png', dpi=150)
plt.close()
print("✅ Saved: rf_feature_importance.png")

# ─────────────────────────────────────────────
# STEP 6: SAVE MODEL
# ─────────────────────────────────────────────
print("\n📌 Step 6: Saving Model...")
with open('../models/rf_model.pkl', 'wb') as f:
    pickle.dump(best_rf, f)
print("✅ Saved: rf_model.pkl")

print("\n" + "=" * 60)
print(f"  ✅ RANDOM FOREST COMPLETE!")
print(f"  🎯 Final Accuracy: {final_acc*100:.2f}%")
print("  📌 Next: XGBoost Model")
print("=" * 60)