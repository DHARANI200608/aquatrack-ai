import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - DATA CLEANING")
print("=" * 60)

print("\n Loading datasets...")
water     = pd.read_csv('../data/water_potability.csv')
cholera   = pd.read_csv('../data/cholera.csv')
pollution = pd.read_csv('../data/water_pollution_disease.csv')
print(" All 3 datasets loaded!")

print("\nCLEANING DATASET 1: WATER POTABILITY")
imputer = KNNImputer(n_neighbors=5)
water_cols = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
              'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
water[water_cols] = imputer.fit_transform(water[water_cols])
water = water.drop_duplicates()
print(f" Water clean! Missing values: {water.isnull().sum().sum()}")

print("\nCLEANING DATASET 2: CHOLERA")
cholera.columns = ['Country', 'Year', 'Cases', 'Deaths', 'Fatality_Rate', 'WHO_Region']

# Convert to numeric first (removes commas, text etc)
cholera['Cases']         = pd.to_numeric(cholera['Cases'].astype(str).str.replace(',',''), errors='coerce')
cholera['Deaths']        = pd.to_numeric(cholera['Deaths'].astype(str).str.replace(',',''), errors='coerce')
cholera['Fatality_Rate'] = pd.to_numeric(cholera['Fatality_Rate'].astype(str).str.replace(',',''), errors='coerce')

# Now fill missing with median
cholera['Cases']         = cholera['Cases'].fillna(cholera['Cases'].median())
cholera['Deaths']        = cholera['Deaths'].fillna(cholera['Deaths'].median())
cholera['Fatality_Rate'] = cholera['Fatality_Rate'].fillna(cholera['Fatality_Rate'].median())
cholera = cholera.drop_duplicates()
print(f" Cholera clean! Missing values: {cholera.isnull().sum().sum()}")

print("\nCLEANING DATASET 3: WATER POLLUTION")
mode_val = pollution['Water Treatment Method'].mode()[0]
pollution['Water Treatment Method'] = pollution['Water Treatment Method'].fillna(mode_val)
pollution = pollution.drop_duplicates()
print(f" Pollution clean! Missing values: {pollution.isnull().sum().sum()}")

print("\nSAVING CLEAN FILES...")
water.to_csv('../data/water_potability_clean.csv', index=False)
cholera.to_csv('../data/cholera_clean.csv', index=False)
pollution.to_csv('../data/water_pollution_clean.csv', index=False)

print(" Saved: water_potability_clean.csv")
print(" Saved: cholera_clean.csv")
print(" Saved: water_pollution_clean.csv")
print("\n Data Cleaning COMPLETE!")
print(" Next: EDA - Exploratory Data Analysis")
