import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - FEATURE ENGINEERING")
print("=" * 60)

# ─────────────────────────────────────────────
# LOAD CLEAN DATASETS
# ─────────────────────────────────────────────
water     = pd.read_csv('../data/water_potability_clean.csv')
cholera   = pd.read_csv('../data/cholera_clean.csv')
pollution = pd.read_csv('../data/water_pollution_clean.csv')
print("✅ Clean datasets loaded!")

# ─────────────────────────────────────────────
# STEP 1: CONTAMINATION RISK SCORE
# Formula: weighted combo of pH + Turbidity + Solids
# ─────────────────────────────────────────────
print("\n📌 Step 1: Creating Contamination Risk Score...")

# Normalize pH deviation from safe range (6.5-8.5)
water['ph_risk'] = abs(water['ph'] - 7.0) / 7.0

# Normalize turbidity (higher = more risky)
water['turbidity_risk'] = water['Turbidity'] / water['Turbidity'].max()

# Normalize solids (higher = more risky)
water['solids_risk'] = water['Solids'] / water['Solids'].max()

# Weighted Risk Score
water['Contamination_Risk_Score'] = (
    0.4 * water['ph_risk'] +
    0.3 * water['turbidity_risk'] +
    0.3 * water['solids_risk']
)

print(f"✅ Contamination Risk Score created!")
print(f"   Min: {water['Contamination_Risk_Score'].min():.4f}")
print(f"   Max: {water['Contamination_Risk_Score'].max():.4f}")
print(f"   Mean: {water['Contamination_Risk_Score'].mean():.4f}")

# ─────────────────────────────────────────────
# STEP 2: RISK LEVEL LABEL (Low/Medium/High)
# ─────────────────────────────────────────────
print("\n📌 Step 2: Creating Risk Level Labels...")

def assign_risk(score):
    if score < 0.15:
        return 'Low'
    elif score < 0.25:
        return 'Medium'
    else:
        return 'High'

water['Risk_Level'] = water['Contamination_Risk_Score'].apply(assign_risk)
print(f"✅ Risk Level distribution:")
print(water['Risk_Level'].value_counts())

# ─────────────────────────────────────────────
# STEP 3: ENCODE CATEGORICAL COLUMNS
# ─────────────────────────────────────────────
print("\n📌 Step 3: Encoding Categorical Columns...")

# Encode Risk Level
le = LabelEncoder()
water['Risk_Level_Encoded'] = le.fit_transform(water['Risk_Level'])
print(f"✅ Risk_Level encoded: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Encode Water Treatment Method in pollution dataset
pollution['Treatment_Encoded'] = le.fit_transform(pollution['Water Treatment Method'])
print(f"✅ Water Treatment Method encoded!")

# Encode Region in pollution dataset
pollution['Region_Encoded'] = le.fit_transform(pollution['Region'])
print(f"✅ Region encoded!")

# ─────────────────────────────────────────────
# STEP 4: NORMALIZE NUMERIC FEATURES
# ─────────────────────────────────────────────
print("\n📌 Step 4: Normalizing Numeric Features...")

scaler = MinMaxScaler()

# Normalize water potability features
water_num_cols = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                  'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
water[water_num_cols] = scaler.fit_transform(water[water_num_cols])
print(f"✅ Water potability features normalized!")

# Normalize pollution features
pollution_num_cols = ['Contaminant Level (ppm)', 'pH Level', 'Turbidity (NTU)',
                      'Dissolved Oxygen (mg/L)', 'Nitrate Level (mg/L)',
                      'Bacteria Count (CFU/mL)', 'Diarrheal Cases per 100,000 people',
                      'Cholera Cases per 100,000 people', 'Typhoid Cases per 100,000 people']
pollution[pollution_num_cols] = scaler.fit_transform(pollution[pollution_num_cols])
print(f"✅ Pollution features normalized!")

# ─────────────────────────────────────────────
# STEP 5: LAG FEATURES FOR CHOLERA (LSTM)
# ─────────────────────────────────────────────
print("\n📌 Step 5: Creating Lag Features for LSTM...")

# Sort by year
cholera = cholera.sort_values('Year')
yearly  = cholera.groupby('Year')['Cases'].sum().reset_index()

# Create lag features
yearly['Cases_Lag1'] = yearly['Cases'].shift(1)
yearly['Cases_Lag2'] = yearly['Cases'].shift(2)
yearly['Cases_Lag3'] = yearly['Cases'].shift(3)
yearly['Rolling_3yr_Mean'] = yearly['Cases'].rolling(3).mean()
yearly['Rolling_5yr_Mean'] = yearly['Cases'].rolling(5).mean()
yearly = yearly.dropna()

print(f"✅ Lag features created!")
print(f"   Shape: {yearly.shape}")
print(yearly.head())

# ─────────────────────────────────────────────
# STEP 6: TRAIN / TEST SPLIT
# ─────────────────────────────────────────────
print("\n📌 Step 6: Train/Test Split (80/20)...")

# Features and target for water potability
X = water.drop(['Potability', 'Risk_Level', 'ph_risk',
                'turbidity_risk', 'solids_risk'], axis=1)
y = water['Potability']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print(f"✅ Train set : {X_train.shape[0]} samples")
print(f"✅ Test set  : {X_test.shape[0]} samples")
print(f"✅ Features  : {X_train.shape[1]} columns")

# ─────────────────────────────────────────────
# STEP 7: SAVE ALL FEATURED DATASETS
# ─────────────────────────────────────────────
print("\n📌 Step 7: Saving Featured Datasets...")

water.to_csv('../data/water_featured.csv', index=False)
pollution.to_csv('../data/pollution_featured.csv', index=False)
yearly.to_csv('../data/cholera_timeseries.csv', index=False)

X_train.to_csv('../data/X_train.csv', index=False)
X_test.to_csv('../data/X_test.csv', index=False)
y_train.to_csv('../data/y_train.csv', index=False)
y_test.to_csv('../data/y_test.csv', index=False)

print("✅ Saved: water_featured.csv")
print("✅ Saved: pollution_featured.csv")
print("✅ Saved: cholera_timeseries.csv")
print("✅ Saved: X_train.csv, X_test.csv, y_train.csv, y_test.csv")

print("\n" + "=" * 60)
print("  ✅ Feature Engineering COMPLETE!")
print("  📌 Next: Week 2 - Model Building!")
print("=" * 60)