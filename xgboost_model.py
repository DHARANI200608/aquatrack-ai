import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - XGBOOST MODEL")
print("=" * 60)

# LOAD TRAIN/TEST DATA
print("\nLoading train/test data...")
X_train = pd.read_csv('../data/X_train.csv')
X_test  = pd.read_csv('../data/X_test.csv')
y_train = pd.read_csv('../data/y_train.csv').values.ravel()
y_test  = pd.read_csv('../data/y_test.csv').values.ravel()
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# STEP 1: TRAIN BASIC XGBOOST
print("\nStep 1: Training XGBoost...")
xgb = XGBClassifier(random_state=42, eval_metric='logloss',
                    scale_pos_weight=1.5)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Basic Accuracy: {acc*100:.2f}%")

# STEP 2: HYPERPARAMETER TUNING
print("\nStep 2: Tuning Hyperparameters (takes 2-3 mins)...")
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1],
    'scale_pos_weight': [1.5, 2.0]
}
grid_search = GridSearchCV(
    XGBClassifier(random_state=42, eval_metric='logloss'),
    param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best CV Accuracy: {grid_search.best_score_*100:.2f}%")

# STEP 3: FINAL MODEL EVALUATION
print("\nStep 3: Final Model Evaluation...")
best_xgb    = grid_search.best_estimator_
y_pred_best = best_xgb.predict(X_test)
final_acc   = accuracy_score(y_test, y_pred_best)
print(f"Final Accuracy: {final_acc*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_best,
      target_names=['Unsafe Water', 'Safe Water']))

# STEP 4: CONFUSION MATRIX PLOT
print("\nStep 4: Saving Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Greens')
plt.colorbar()
plt.title('XGBoost Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks([0,1], ['Unsafe','Safe'])
plt.yticks([0,1], ['Unsafe','Safe'])
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha='center', va='center',
                 fontsize=18, color='black')
plt.tight_layout()
plt.savefig('../reports/xgb_confusion_matrix.png', dpi=150)
plt.close()
print("Saved: xgb_confusion_matrix.png")

# STEP 5: FEATURE IMPORTANCE PLOT
print("\nStep 5: Feature Importance Plot...")
importance = pd.Series(best_xgb.feature_importances_, index=X_train.columns)
importance = importance.sort_values(ascending=True)
plt.figure(figsize=(10, 6))
importance.plot(kind='barh', color='steelblue')
plt.title('XGBoost - Feature Importance', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('../reports/xgb_feature_importance.png', dpi=150)
plt.close()
print("Saved: xgb_feature_importance.png")

# STEP 6: SAVE MODEL
print("\nStep 6: Saving Model...")
with open('../models/xgb_model.pkl', 'wb') as f:
    pickle.dump(best_xgb, f)
print("Saved: xgb_model.pkl")

print("\n" + "=" * 60)
print(f"  XGBOOST COMPLETE!")
print(f"  Final Accuracy: {final_acc*100:.2f}%")
print("  Next: Model Evaluation & Comparison")
print("=" * 60)