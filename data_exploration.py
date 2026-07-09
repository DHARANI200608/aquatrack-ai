import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - DATA EXPLORATION")
print("=" * 60)

print("\n Loading datasets...")
water     = pd.read_csv('../data/water_potability.csv')
cholera   = pd.read_csv('../data/cholera.csv')
pollution = pd.read_csv('../data/water_pollution_disease.csv')
print("All 3 datasets loaded!")

print("\nDATASET 1: WATER POTABILITY")
print(f"Shape: {water.shape}")
print(f"Columns: {list(water.columns)}")
print(f"Missing Values:\n{water.isnull().sum()}")
print(f"Statistics:\n{water.describe()}")
print(f"Target Values:\n{water['Potability'].value_counts()}")

print("\nDATASET 2: CHOLERA")
print(f"Shape: {cholera.shape}")
print(f"Columns: {list(cholera.columns)}")
print(f"Missing Values:\n{cholera.isnull().sum()}")
print(f"First 5 rows:\n{cholera.head()}")

print("\nDATASET 3: WATER POLLUTION")
print(f"Shape: {pollution.shape}")
print(f"Columns: {list(pollution.columns)}")
print(f"Missing Values:\n{pollution.isnull().sum()}")
print(f"First 5 rows:\n{pollution.head()}")

print("\nDone! Data Exploration Complete!")