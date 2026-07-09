import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - EDA")
print("=" * 60)

# ─────────────────────────────────────────────
# LOAD CLEAN DATASETS
# ─────────────────────────────────────────────
water     = pd.read_csv('../data/water_potability_clean.csv')
cholera   = pd.read_csv('../data/cholera_clean.csv')
pollution = pd.read_csv('../data/water_pollution_clean.csv')
print("✅ Clean datasets loaded!")

# ─────────────────────────────────────────────
# PLOT 1 - HISTOGRAM OF WATER PARAMETERS
# ─────────────────────────────────────────────
print("\n📊 Plot 1: Water Parameter Distributions...")
cols = ['ph','Hardness','Solids','Chloramines','Sulfate',
        'Conductivity','Organic_carbon','Trihalomethanes','Turbidity']
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
fig.suptitle('Water Quality Parameter Distributions', fontsize=16, fontweight='bold')
for i, col in enumerate(cols):
    ax = axes[i//3][i%3]
    water[col].hist(bins=30, ax=ax, color='steelblue', edgecolor='white')
    ax.set_title(col)
    ax.set_xlabel('Value')
    ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('../reports/plot1_water_distributions.png', dpi=150)
plt.close()
print("✅ Saved: plot1_water_distributions.png")

# ─────────────────────────────────────────────
# PLOT 2 - CORRELATION HEATMAP
# ─────────────────────────────────────────────
print("\n📊 Plot 2: Correlation Heatmap...")
plt.figure(figsize=(12, 8))
corr = water.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, square=True)
plt.title('Water Quality Correlation Heatmap', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('../reports/plot2_correlation_heatmap.png', dpi=150)
plt.close()
print("✅ Saved: plot2_correlation_heatmap.png")

# ─────────────────────────────────────────────
# PLOT 3 - BOX PLOTS SAFE VS UNSAFE
# ─────────────────────────────────────────────
print("\n📊 Plot 3: Safe vs Unsafe Water Box Plots...")
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
fig.suptitle('Safe vs Unsafe Water — Parameter Comparison', fontsize=16, fontweight='bold')
for i, col in enumerate(cols):
    ax = axes[i//3][i%3]
    water.boxplot(column=col, by='Potability', ax=ax,
                  boxprops=dict(color='steelblue'),
                  medianprops=dict(color='red'))
    ax.set_title(col)
    ax.set_xlabel('0=Unsafe  1=Safe')
plt.suptitle('Safe vs Unsafe Water — Parameter Comparison', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('../reports/plot3_boxplots_safe_unsafe.png', dpi=150)
plt.close()
print("✅ Saved: plot3_boxplots_safe_unsafe.png")

# ─────────────────────────────────────────────
# PLOT 4 - PIE CHART SAFE VS UNSAFE
# ─────────────────────────────────────────────
print("\n📊 Plot 4: Safe vs Unsafe Pie Chart...")
plt.figure(figsize=(7, 7))
counts = water['Potability'].value_counts()
plt.pie(counts, labels=['Unsafe Water', 'Safe Water'],
        autopct='%1.1f%%', colors=['#e74c3c', '#2ecc71'],
        startangle=90, explode=(0.05, 0.05))
plt.title('Water Safety Distribution', fontsize=16, fontweight='bold')
plt.savefig('../reports/plot4_pie_safe_unsafe.png', dpi=150)
plt.close()
print("✅ Saved: plot4_pie_safe_unsafe.png")

# ─────────────────────────────────────────────
# PLOT 5 - CHOLERA TREND OVER YEARS
# ─────────────────────────────────────────────
print("\n📊 Plot 5: Cholera Cases Over Years...")
yearly = cholera.groupby('Year')['Cases'].sum().reset_index()
plt.figure(figsize=(14, 6))
plt.plot(yearly['Year'], yearly['Cases'], color='#e74c3c', linewidth=2, marker='o', markersize=4)
plt.fill_between(yearly['Year'], yearly['Cases'], alpha=0.2, color='#e74c3c')
plt.title('Global Cholera Cases Over Years', fontsize=16, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Total Cases')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/plot5_cholera_trend.png', dpi=150)
plt.close()
print("✅ Saved: plot5_cholera_trend.png")

# ─────────────────────────────────────────────
# PLOT 6 - TOP 10 AFFECTED COUNTRIES
# ─────────────────────────────────────────────
print("\n📊 Plot 6: Top 10 Most Affected Countries...")
top10 = cholera.groupby('Country')['Cases'].sum().nlargest(10).reset_index()
plt.figure(figsize=(12, 6))
bars = plt.barh(top10['Country'], top10['Cases'], color='steelblue')
plt.title('Top 10 Countries by Cholera Cases', fontsize=16, fontweight='bold')
plt.xlabel('Total Cases')
plt.gca().invert_yaxis()
for bar, val in zip(bars, top10['Cases']):
    plt.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
             f'{int(val):,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('../reports/plot6_top10_countries.png', dpi=150)
plt.close()
print("✅ Saved: plot6_top10_countries.png")

# ─────────────────────────────────────────────
# PLOT 7 - DISEASE CASES BY REGION
# ─────────────────────────────────────────────
print("\n📊 Plot 7: Disease Cases by Region...")
region_data = pollution.groupby('Region')[['Diarrheal Cases per 100,000 people',
                                            'Cholera Cases per 100,000 people',
                                            'Typhoid Cases per 100,000 people']].mean()
region_data.plot(kind='bar', figsize=(12, 6), colormap='Set2', edgecolor='white')
plt.title('Average Disease Cases by Region', fontsize=16, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Cases per 100,000 people')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('../reports/plot7_disease_by_region.png', dpi=150)
plt.close()
print("✅ Saved: plot7_disease_by_region.png")

# ─────────────────────────────────────────────
# PLOT 8 - WATER ACCESS VS DISEASE
# ─────────────────────────────────────────────
print("\n📊 Plot 8: Water Access vs Diarrheal Cases...")
plt.figure(figsize=(10, 6))
plt.scatter(pollution['Access to Clean Water (% of Population)'],
            pollution['Diarrheal Cases per 100,000 people'],
            alpha=0.5, color='steelblue', edgecolors='white', linewidths=0.5)
plt.title('Clean Water Access vs Diarrheal Disease Cases', fontsize=16, fontweight='bold')
plt.xlabel('Access to Clean Water (%)')
plt.ylabel('Diarrheal Cases per 100,000')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/plot8_water_access_vs_disease.png', dpi=150)
plt.close()
print("✅ Saved: plot8_water_access_vs_disease.png")

# ─────────────────────────────────────────────
# PLOT 9 - pH DISTRIBUTION BY POTABILITY
# ─────────────────────────────────────────────
print("\n📊 Plot 9: pH Distribution Safe vs Unsafe...")
plt.figure(figsize=(10, 6))
water[water['Potability']==0]['ph'].hist(bins=30, alpha=0.6, color='#e74c3c', label='Unsafe')
water[water['Potability']==1]['ph'].hist(bins=30, alpha=0.6, color='#2ecc71', label='Safe')
plt.title('pH Level: Safe vs Unsafe Water', fontsize=16, fontweight='bold')
plt.xlabel('pH Level')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/plot9_ph_distribution.png', dpi=150)
plt.close()
print("✅ Saved: plot9_ph_distribution.png")

# ─────────────────────────────────────────────
# PLOT 10 - TURBIDITY VS BACTERIA COUNT
# ─────────────────────────────────────────────
print("\n📊 Plot 10: Turbidity vs Bacteria Count...")
plt.figure(figsize=(10, 6))
plt.scatter(pollution['Turbidity (NTU)'],
            pollution['Bacteria Count (CFU/mL)'],
            alpha=0.4, color='#e67e22', edgecolors='white', linewidths=0.3)
plt.title('Turbidity vs Bacteria Count', fontsize=16, fontweight='bold')
plt.xlabel('Turbidity (NTU)')
plt.ylabel('Bacteria Count (CFU/mL)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/plot10_turbidity_vs_bacteria.png', dpi=150)
plt.close()
print("✅ Saved: plot10_turbidity_vs_bacteria.png")

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  EDA SUMMARY")
print("=" * 60)
print("""
  ✅ Plot 1  - Water Parameter Distributions
  ✅ Plot 2  - Correlation Heatmap
  ✅ Plot 3  - Safe vs Unsafe Box Plots
  ✅ Plot 4  - Safe vs Unsafe Pie Chart
  ✅ Plot 5  - Cholera Trend Over Years
  ✅ Plot 6  - Top 10 Affected Countries
  ✅ Plot 7  - Disease Cases by Region
  ✅ Plot 8  - Water Access vs Disease
  ✅ Plot 9  - pH Distribution
  ✅ Plot 10 - Turbidity vs Bacteria

  All 10 plots saved in reports/ folder!
""")
print("=" * 60)
print("  ✅ EDA COMPLETE!")
print("  📌 Next: Feature Engineering")
print("=" * 60)