import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - SHAP EXPLAINABILITY")
print("=" * 60)

# LOAD DATASET
print("\nLoading dataset and model...")
df = pd.read_csv('../data/waterQuality1.csv')
df = df[df['is_safe'] != '#NUM!']
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna()

X = df.drop('is_safe', axis=1)
y = df['is_safe'].astype(int)

# LOAD SAVED MODEL
with open('../models/xgb_90_model.pkl', 'rb') as f:
    model = pickle.load(f)
print("Model loaded successfully!")

# STEP 1: SHAP EXPLAINER
print("\nStep 1: Creating SHAP explainer...")
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
print("SHAP values calculated!")

# STEP 2: SHAP SUMMARY PLOT
print("\nStep 2: Saving SHAP Summary Plot...")
plt.figure()
shap.summary_plot(shap_values, X, show=False)
plt.title('SHAP Summary - Feature Impact on Water Safety',
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../reports/shap_summary.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: shap_summary.png")

# STEP 3: SHAP BAR PLOT
print("\nStep 3: Saving SHAP Bar Plot...")
plt.figure()
shap.summary_plot(shap_values, X, plot_type='bar', show=False)
plt.title('SHAP Feature Importance - Water Safety',
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../reports/shap_bar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: shap_bar.png")

# STEP 4: TOP FEATURES REPORT
print("\nStep 4: Top Features Driving Unsafe Water...")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'SHAP_Importance': np.abs(shap_values).mean(axis=0)
})
feature_importance = feature_importance.sort_values(
    'SHAP_Importance', ascending=False)

print("\nTop 10 features that determine water safety:")
print(feature_importance.head(10).to_string(index=False))

# SAVE REPORT
feature_importance.to_csv('../reports/shap_feature_importance.csv', index=False)
print("\nSaved: shap_feature_importance.csv")

print("\n" + "=" * 60)
print("  SHAP EXPLAINABILITY COMPLETE!")
print("  Check reports/ folder for shap_summary.png")
print("  Next: LSTM Forecasting")
print("=" * 60)