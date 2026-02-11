"""
VIH Data Analysis Project - Democratic Republic of Congo
=========================================================
Author: Bienvenu Mwenyemali
Date: February 2026
Description: Comprehensive HIV/AIDS data analysis showcasing Python skills
             with data extraction, cleaning, exploration, visualization, and statistical analysis
"""

# ============================================================================
# SECTION 1: IMPORT LIBRARIES
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import zscore, pearsonr, spearmanr, shapiro, normaltest
import warnings
warnings.filterwarnings('ignore')

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 100)

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("=" * 80)
print("VIH DATA ANALYSIS PROJECT - DEMOCRATIC REPUBLIC OF CONGO")
print("=" * 80)

# ============================================================================
# SECTION 2: DATA EXTRACTION FROM EXCEL
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DATA EXTRACTION")
print("=" * 80)

def load_data(filepath):
    """
    Function to load data from Excel file
    Parameters:
        filepath (str): Path to the Excel file
    Returns:
        DataFrame: Pandas DataFrame containing the data
    """
    try:
        df = pd.read_excel(filepath)
        print(f"Data successfully loaded from: {filepath}")
        print(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return None

# Load the dataset
df = load_data('datavih.xlsx')

# ============================================================================
# SECTION 3: DATA EXPLORATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: DATA EXPLORATION")
print("=" * 80)

def explore_dataframe(df):
    """
    Comprehensive function to explore a DataFrame
    """
    print("\n--- DataFrame Info ---")
    print(df.info())
    
    print("\n--- First 10 Rows ---")
    print(df.head(10))
    
    print("\n--- Last 5 Rows ---")
    print(df.tail(5))
    
    print("\n--- Column Names ---")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\n--- Data Types ---")
    print(df.dtypes)
    
    print("\n--- Shape ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    return df.shape

explore_dataframe(df)

# Unique values analysis
print("\n--- Unique Values per Column ---")
def count_unique_values(df):
    """
    Count unique values for each column
    """
    unique_counts = {}
    for col in df.columns:
        unique_counts[col] = df[col].nunique()
        print(f"  {col}: {unique_counts[col]} unique values")
    return unique_counts

unique_counts = count_unique_values(df)

# Display unique values for categorical columns
print("\n--- Unique Provinces (26 provinces of DRC) ---")
print(sorted(df['provinces'].unique().tolist()))

print("\n--- Unique Years ---")
print(sorted(df['annees'].unique()))

print("\n--- Unique Quarters ---")
print(df['trimestres'].unique().tolist())

print("\n--- Unique Gender Categories ---")
print(df['sexes'].unique().tolist())

print("\n--- Unique Age Groups ---")
print(df['tranches_ages'].unique().tolist())

# ============================================================================
# SECTION 4: DATA CLEANING
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: DATA CLEANING")
print("=" * 80)

def analyze_missing_values(df):
    """
    Analyze missing values in the DataFrame
    """
    missing = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': missing.values,
        'Missing Percentage': missing_percent.values
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(
        'Missing Percentage', ascending=False
    )
    
    print("\n--- Missing Values Analysis ---")
    if len(missing_df) > 0:
        print(missing_df.to_string(index=False))
    else:
        print("No missing values found!")
    
    return missing_df

missing_analysis = analyze_missing_values(df)

def clean_data(df):
    """
    Comprehensive data cleaning function
    """
    df_clean = df.copy()
    
    # 1. Handle missing values in categorical columns
    print("\n--- Cleaning Process ---")
    
    # Fill missing categorical values with 'Non spécifié'
    categorical_cols = ['provinces', 'trimestres', 'indicateurs', 'cibles', 'sexes', 'tranches_ages']
    for col in categorical_cols:
        if col in df_clean.columns:
            missing_count = df_clean[col].isnull().sum()
            if missing_count > 0:
                df_clean[col] = df_clean[col].fillna('Non spécifié')
                print(f"  - Filled {missing_count} missing values in '{col}' with 'Non spécifié'")
    
    # 2. Handle missing numeric values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing_count = df_clean[col].isnull().sum()
        if missing_count > 0:
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)
            print(f"  - Filled {missing_count} missing values in '{col}' with median: {median_val}")
    
    # 3. Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    if duplicates_removed > 0:
        print(f"  - Removed {duplicates_removed} duplicate rows")
    else:
        print("  - No duplicate rows found")
    
    # 4. Standardize text columns (strip whitespace, consistent case)
    for col in categorical_cols:
        if col in df_clean.columns and df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].str.strip()
    
    print(f"\n  Final cleaned dataset shape: {df_clean.shape}")
    
    return df_clean

df_clean = clean_data(df)

# ============================================================================
# SECTION 5: STATISTICAL ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 5: STATISTICAL ANALYSIS")
print("=" * 80)

def descriptive_statistics(df, column='Valeur'):
    """
    Calculate comprehensive descriptive statistics
    """
    data = df[column].dropna()
    
    stats_dict = {
        'Count': len(data),
        'Mean': data.mean(),
        'Median': data.median(),
        'Mode': data.mode().iloc[0] if len(data.mode()) > 0 else np.nan,
        'Standard Deviation': data.std(),
        'Variance': data.var(),
        'Min': data.min(),
        'Max': data.max(),
        'Range': data.max() - data.min(),
        'Q1 (25%)': data.quantile(0.25),
        'Q2 (50%)': data.quantile(0.50),
        'Q3 (75%)': data.quantile(0.75),
        'IQR': data.quantile(0.75) - data.quantile(0.25),
        'Skewness': data.skew(),
        'Kurtosis': data.kurtosis(),
        'Coefficient of Variation': (data.std() / data.mean()) * 100
    }
    
    print(f"\n--- Descriptive Statistics for '{column}' ---")
    for key, value in stats_dict.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value:,}")
    
    return stats_dict

desc_stats = descriptive_statistics(df_clean)

# Statistical analysis by province
print("\n--- Statistics by Province ---")
province_stats = df_clean.groupby('provinces')['Valeur'].agg([
    'count', 'sum', 'mean', 'median', 'std', 'min', 'max'
]).round(2)
print(province_stats)

# Statistical analysis by year
print("\n--- Statistics by Year ---")
year_stats = df_clean.groupby('annees')['Valeur'].agg([
    'count', 'sum', 'mean', 'median', 'std'
]).round(2)
print(year_stats)

# Statistical analysis by gender
print("\n--- Statistics by Gender ---")
gender_stats = df_clean.groupby('sexes')['Valeur'].agg([
    'count', 'sum', 'mean', 'median'
]).round(2)
print(gender_stats)

# ============================================================================
# SECTION 6: OUTLIER DETECTION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 6: OUTLIER DETECTION")
print("=" * 80)

def detect_outliers_iqr(data, column):
    """
    Detect outliers using IQR method
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    print(f"\n--- IQR Method for '{column}' ---")
    print(f"  Q1: {Q1:,.2f}")
    print(f"  Q3: {Q3:,.2f}")
    print(f"  IQR: {IQR:,.2f}")
    print(f"  Lower Bound: {lower_bound:,.2f}")
    print(f"  Upper Bound: {upper_bound:,.2f}")
    print(f"  Number of Outliers: {len(outliers)}")
    print(f"  Outlier Percentage: {(len(outliers)/len(data))*100:.2f}%")
    
    return outliers, lower_bound, upper_bound

def detect_outliers_zscore(data, column, threshold=3):
    """
    Detect outliers using Z-score method
    """
    z_scores = np.abs(zscore(data[column].dropna()))
    outliers_idx = np.where(z_scores > threshold)[0]
    
    print(f"\n--- Z-Score Method for '{column}' (threshold={threshold}) ---")
    print(f"  Number of Outliers: {len(outliers_idx)}")
    print(f"  Outlier Percentage: {(len(outliers_idx)/len(data))*100:.2f}%")
    
    return outliers_idx

# Detect outliers in 'Valeur' column
outliers_iqr, lb, ub = detect_outliers_iqr(df_clean, 'Valeur')
outliers_zscore = detect_outliers_zscore(df_clean, 'Valeur')

# Outlier analysis for specific indicator:
# "Nombre de préservatifs masculins distribués"
print("\n--- Outlier Analysis: Nombre de préservatifs masculins distribués ---")
preservatifs_data = df_clean[df_clean['indicateurs'] == 'Nombre de préservatifs masculins distribués']
if len(preservatifs_data) > 0:
    outliers_preserv, _, _ = detect_outliers_iqr(preservatifs_data, 'Valeur')
    print(f"\n  Sample outliers:")
    print(outliers_preserv[['provinces', 'annees', 'trimestres', 'Valeur']].head(10))

# ============================================================================
# SECTION 7: DATA AGGREGATION AND PIVOT TABLES
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 7: DATA AGGREGATION AND PIVOT TABLES")
print("=" * 80)

# Pivot table: Values by Province and Year
print("\n--- Pivot Table: Total Values by Province and Year ---")
pivot_province_year = pd.pivot_table(
    df_clean,
    values='Valeur',
    index='provinces',
    columns='annees',
    aggfunc='sum',
    fill_value=0
)
print(pivot_province_year.head(10))

# Pivot table: Values by Gender and Age Group
print("\n--- Pivot Table: Total Values by Gender and Age Group ---")
pivot_gender_age = pd.pivot_table(
    df_clean,
    values='Valeur',
    index='sexes',
    columns='tranches_ages',
    aggfunc='sum',
    fill_value=0
)
print(pivot_gender_age)

# Group by multiple columns
print("\n--- Grouped Analysis: Province, Year, Quarter ---")
grouped_analysis = df_clean.groupby(['provinces', 'annees', 'trimestres']).agg({
    'Valeur': ['sum', 'mean', 'count']
}).round(2)
grouped_analysis.columns = ['Total', 'Average', 'Count']
print(grouped_analysis.head(20))

# ============================================================================
# SECTION 8: CORRELATION ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 8: CORRELATION ANALYSIS")
print("=" * 80)

# Create a pivot for correlation analysis by indicator
indicators_pivot = df_clean.pivot_table(
    values='Valeur',
    index=['provinces', 'annees'],
    columns='indicateurs',
    aggfunc='sum'
).reset_index()

# Select key indicators for UNAIDS 95-95-95
key_indicators = [
    'Nombre de clients testés',  # 1st 95: Know status
    'Nombre de PVVIH sous TAR',   # 2nd 95: On treatment
    'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'  # 3rd 95: Viral suppression
]

print("\n--- Key UNAIDS 95-95-95 Indicators ---")
for i, ind in enumerate(key_indicators, 1):
    data = df_clean[df_clean['indicateurs'] == ind]['Valeur']
    print(f"\n{i}. {ind}")
    print(f"   Count: {len(data):,}")
    print(f"   Total: {data.sum():,.0f}")
    print(f"   Mean: {data.mean():,.2f}")

# ============================================================================
# SECTION 9: TIME SERIES ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 9: TIME SERIES ANALYSIS")
print("=" * 80)

# Create time period column
df_clean['period'] = df_clean['annees'].astype(str) + '-' + df_clean['trimestres']

# Trend analysis by year
print("\n--- Yearly Trend Analysis ---")
yearly_trend = df_clean.groupby('annees')['Valeur'].agg(['sum', 'mean', 'count'])
yearly_trend['YoY_Growth_%'] = yearly_trend['sum'].pct_change() * 100
print(yearly_trend.round(2))

# Quarterly trend
print("\n--- Quarterly Totals by Year ---")
quarterly_trend = df_clean.groupby(['annees', 'trimestres'])['Valeur'].sum().unstack()
print(quarterly_trend)

# ============================================================================
# SECTION 10: ADVANCED STATISTICAL TESTS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 10: ADVANCED STATISTICAL TESTS")
print("=" * 80)

# Sample data for normality test (using a manageable sample)
sample_data = df_clean['Valeur'].dropna().sample(min(5000, len(df_clean)), random_state=42)

# Normality Test (D'Agostino-Pearson)
print("\n--- Normality Test (D'Agostino-Pearson) ---")
try:
    stat, p_value = normaltest(sample_data)
    print(f"  Test Statistic: {stat:.4f}")
    print(f"  P-value: {p_value:.4e}")
    print(f"  Result: {'Normal distribution' if p_value > 0.05 else 'Not normal distribution'}")
except Exception as e:
    print(f"  Test could not be performed: {e}")

# Compare means between genders (excluding NaN)
print("\n--- T-Test: Comparing Values between Genders ---")
male_data = df_clean[df_clean['sexes'] == 'Masculin']['Valeur'].dropna()
female_data = df_clean[df_clean['sexes'] == 'Féminin']['Valeur'].dropna()

if len(male_data) > 0 and len(female_data) > 0:
    t_stat, p_value = stats.ttest_ind(male_data.sample(min(1000, len(male_data)), random_state=42),
                                       female_data.sample(min(1000, len(female_data)), random_state=42))
    print(f"  T-statistic: {t_stat:.4f}")
    print(f"  P-value: {p_value:.4e}")
    print(f"  Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")

# Chi-square test for independence
print("\n--- Chi-Square Test: Province vs Gender Independence ---")
contingency = pd.crosstab(df_clean['provinces'], df_clean['sexes'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
print(f"  Chi-square statistic: {chi2:.4f}")
print(f"  P-value: {p_value:.4e}")
print(f"  Degrees of freedom: {dof}")
print(f"  Result: {'Dependent' if p_value < 0.05 else 'Independent'}")

# ============================================================================
# SECTION 11: CUSTOM ANALYSIS FUNCTIONS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 11: CUSTOM ANALYSIS FUNCTIONS")
print("=" * 80)

def calculate_unaids_95_95_95(df):
    """
    Calculate UNAIDS 95-95-95 cascade indicators
    - 1st 95: % of PLHIV who know their HIV status
    - 2nd 95: % of diagnosed PLHIV on treatment
    - 3rd 95: % of those on treatment with viral suppression
    """
    print("\n--- UNAIDS 95-95-95 Cascade Analysis ---")
    
    # Get relevant indicators
    tested = df[df['indicateurs'] == 'Nombre de clients testés']['Valeur'].sum()
    diagnosed = df[df['indicateurs'] == 'Nombre de clients diagnostiqués VIH+']['Valeur'].sum()
    on_tar = df[df['indicateurs'] == 'Nombre de PVVIH sous TAR']['Valeur'].sum()
    viral_suppressed = df[df['indicateurs'] == 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale']['Valeur'].sum()
    
    print(f"\n  Total Tested: {tested:,.0f}")
    print(f"  Total Diagnosed HIV+: {diagnosed:,.0f}")
    print(f"  Total on TAR: {on_tar:,.0f}")
    print(f"  Total with Viral Suppression: {viral_suppressed:,.0f}")
    
    # Calculate cascade (simplified)
    if diagnosed > 0:
        tar_rate = (on_tar / diagnosed) * 100
        print(f"\n  2nd 95 (On Treatment Rate): {tar_rate:.2f}%")
    
    if on_tar > 0:
        suppression_rate = (viral_suppressed / on_tar) * 100
        print(f"  3rd 95 (Viral Suppression Rate): {suppression_rate:.2f}%")
    
    return {
        'tested': tested,
        'diagnosed': diagnosed,
        'on_tar': on_tar,
        'viral_suppressed': viral_suppressed
    }

unaids_results = calculate_unaids_95_95_95(df_clean)

def top_provinces_by_indicator(df, indicator, n=5):
    """
    Find top N provinces for a specific indicator
    """
    filtered = df[df['indicateurs'] == indicator]
    top_provinces = filtered.groupby('provinces')['Valeur'].sum().nlargest(n)
    
    print(f"\n--- Top {n} Provinces for '{indicator}' ---")
    for i, (province, value) in enumerate(top_provinces.items(), 1):
        print(f"  {i}. {province}: {value:,.0f}")
    
    return top_provinces

# Example: Top provinces for condom distribution
top_provinces_by_indicator(df_clean, 'Nombre de préservatifs masculins distribués', 5)
top_provinces_by_indicator(df_clean, 'Nombre de PVVIH sous TAR', 5)

def year_over_year_comparison(df, indicator):
    """
    Compare year-over-year changes for an indicator
    """
    yearly_data = df[df['indicateurs'] == indicator].groupby('annees')['Valeur'].sum()
    
    print(f"\n--- Year-over-Year Comparison: {indicator[:50]}... ---")
    for year in sorted(yearly_data.index):
        value = yearly_data[year]
        if year > yearly_data.index.min():
            prev_value = yearly_data[year - 1]
            change = ((value - prev_value) / prev_value) * 100 if prev_value > 0 else 0
            print(f"  {year}: {value:,.0f} ({change:+.2f}% vs {year-1})")
        else:
            print(f"  {year}: {value:,.0f} (baseline)")
    
    return yearly_data

yoy_tar = year_over_year_comparison(df_clean, 'Nombre de PVVIH sous TAR')

# ============================================================================
# SECTION 12: DATA VISUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 12: DATA VISUALIZATION")
print("=" * 80)

# Create output directory for charts
import os
output_dir = 'charts'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Figure 1: Distribution of Values (Histogram)
print("\nGenerating Chart 1: Value Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Log-transformed histogram (due to extreme values)
axes[0].hist(np.log1p(df_clean['Valeur']), bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Log(Value + 1)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Distribution of Values (Log-transformed)', fontsize=14)
axes[0].axvline(np.log1p(df_clean['Valeur'].median()), color='red', linestyle='--', label='Median')
axes[0].legend()

# Box plot
axes[1].boxplot(np.log1p(df_clean['Valeur'].dropna()), vert=True)
axes[1].set_ylabel('Log(Value + 1)', fontsize=12)
axes[1].set_title('Box Plot of Values (Log-transformed)', fontsize=14)

plt.tight_layout()
plt.savefig(f'{output_dir}/01_value_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Yearly Trend
print("Generating Chart 2: Yearly Trend...")
yearly_totals = df_clean.groupby('annees')['Valeur'].sum() / 1e9  # In billions

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(yearly_totals.index, yearly_totals.values, color='teal', edgecolor='black')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Total Value (Billions)', fontsize=12)
ax.set_title('Total Values by Year', fontsize=14)

# Add value labels
for bar, val in zip(bars, yearly_totals.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
            f'{val:.2f}B', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/02_yearly_trend.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Top 10 Provinces
print("Generating Chart 3: Top 10 Provinces...")
top_provinces = df_clean.groupby('provinces')['Valeur'].sum().nlargest(10) / 1e9

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top_provinces.index, top_provinces.values, color='coral', edgecolor='black')
ax.set_xlabel('Total Value (Billions)', fontsize=12)
ax.set_ylabel('Province', fontsize=12)
ax.set_title('Top 10 Provinces by Total Value', fontsize=14)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(f'{output_dir}/03_top_provinces.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Gender Distribution
print("Generating Chart 4: Gender Distribution...")
gender_totals = df_clean.groupby('sexes')['Valeur'].sum()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
colors = ['#ff9999', '#66b3ff', '#99ff99']
axes[0].pie(gender_totals.values, labels=gender_totals.index, autopct='%1.1f%%',
            colors=colors, startangle=90, explode=[0.02]*len(gender_totals))
axes[0].set_title('Distribution by Gender', fontsize=14)

# Bar chart
axes[1].bar(gender_totals.index, gender_totals.values / 1e9, color=colors, edgecolor='black')
axes[1].set_xlabel('Gender', fontsize=12)
axes[1].set_ylabel('Total Value (Billions)', fontsize=12)
axes[1].set_title('Total Values by Gender', fontsize=14)

plt.tight_layout()
plt.savefig(f'{output_dir}/04_gender_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 5: Age Group Analysis
print("Generating Chart 5: Age Group Analysis...")
age_totals = df_clean.groupby('tranches_ages')['Valeur'].sum().sort_values(ascending=True) / 1e9

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(age_totals.index, age_totals.values, color='mediumpurple', edgecolor='black')
ax.set_xlabel('Total Value (Billions)', fontsize=12)
ax.set_ylabel('Age Group', fontsize=12)
ax.set_title('Values by Age Group', fontsize=14)

plt.tight_layout()
plt.savefig(f'{output_dir}/05_age_groups.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 6: Quarterly Heatmap
print("Generating Chart 6: Quarterly Heatmap...")
quarterly_pivot = df_clean.pivot_table(values='Valeur', index='annees', 
                                        columns='trimestres', aggfunc='sum') / 1e9

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(quarterly_pivot, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax,
            cbar_kws={'label': 'Value (Billions)'})
ax.set_title('Quarterly Values by Year (Billions)', fontsize=14)
ax.set_xlabel('Quarter', fontsize=12)
ax.set_ylabel('Year', fontsize=12)

plt.tight_layout()
plt.savefig(f'{output_dir}/06_quarterly_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 7: Scatter Plot for Outlier Detection - Preservatifs Distribution
print("Generating Chart 7: Outlier Detection Scatter Plot...")
preservatifs = df_clean[df_clean['indicateurs'] == 'Nombre de préservatifs masculins distribués'].copy()

if len(preservatifs) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate Z-scores for coloring
    preservatifs['log_valeur'] = np.log1p(preservatifs['Valeur'])
    
    # Create scatter plot
    scatter = ax.scatter(range(len(preservatifs)), preservatifs['Valeur'], 
                        c=preservatifs['annees'], cmap='viridis', alpha=0.6, s=30)
    
    # Add outlier threshold line (IQR method)
    Q1 = preservatifs['Valeur'].quantile(0.25)
    Q3 = preservatifs['Valeur'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    ax.axhline(y=upper_bound, color='red', linestyle='--', linewidth=2, 
               label=f'Outlier Threshold: {upper_bound:,.0f}')
    
    ax.set_xlabel('Observation Index', fontsize=12)
    ax.set_ylabel('Number of Male Condoms Distributed', fontsize=12)
    ax.set_title('Outlier Detection: Male Condom Distribution', fontsize=14)
    ax.legend()
    plt.colorbar(scatter, label='Year')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_outlier_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()

# Figure 8: Province-wise Yearly Trend (Line Chart)
print("Generating Chart 8: Province Yearly Trends...")
top_5_provinces = df_clean.groupby('provinces')['Valeur'].sum().nlargest(5).index

fig, ax = plt.subplots(figsize=(12, 6))
for province in top_5_provinces:
    prov_data = df_clean[df_clean['provinces'] == province].groupby('annees')['Valeur'].sum() / 1e9
    ax.plot(prov_data.index, prov_data.values, marker='o', linewidth=2, markersize=8, label=province)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Total Value (Billions)', fontsize=12)
ax.set_title('Yearly Trends - Top 5 Provinces', fontsize=14)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/08_province_trends.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 9: UNAIDS 95-95-95 Cascade
print("Generating Chart 9: UNAIDS 95-95-95 Cascade...")
cascade_indicators = {
    'Tested': df_clean[df_clean['indicateurs'] == 'Nombre de clients testés']['Valeur'].sum(),
    'Diagnosed HIV+': df_clean[df_clean['indicateurs'] == 'Nombre de clients diagnostiqués VIH+']['Valeur'].sum(),
    'On TAR': df_clean[df_clean['indicateurs'] == 'Nombre de PVVIH sous TAR']['Valeur'].sum(),
    'Viral Suppression': df_clean[df_clean['indicateurs'] == 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale']['Valeur'].sum()
}

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']
bars = ax.bar(cascade_indicators.keys(), [v/1e6 for v in cascade_indicators.values()], 
              color=colors, edgecolor='black')

ax.set_ylabel('Value (Millions)', fontsize=12)
ax.set_title('UNAIDS 95-95-95 Cascade Indicators (Total)', fontsize=14)

# Add value labels
for bar, val in zip(bars, cascade_indicators.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{val/1e6:.1f}M', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/09_unaids_cascade.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 10: Correlation Matrix for Year-Province Values
print("Generating Chart 10: Correlation Analysis...")
province_year_pivot = df_clean.pivot_table(values='Valeur', index='provinces', columns='annees', aggfunc='sum')
correlation_matrix = province_year_pivot.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax, center=0,
            fmt='.3f', square=True)
ax.set_title('Year-to-Year Correlation Matrix', fontsize=14)

plt.tight_layout()
plt.savefig(f'{output_dir}/10_correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nAll charts saved to '{output_dir}/' directory")

# ============================================================================
# SECTION 13: EXPORT CLEANED DATA
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 13: DATA EXPORT")
print("=" * 80)

# Export cleaned data to CSV
df_clean.to_csv('datavih_cleaned.csv', index=False, encoding='utf-8-sig')
print("Cleaned data exported to: datavih_cleaned.csv")

# Export summary statistics
summary_stats = df_clean.groupby(['provinces', 'annees']).agg({
    'Valeur': ['sum', 'mean', 'count']
}).round(2)
summary_stats.columns = ['Total', 'Average', 'Count']
summary_stats.to_csv('summary_by_province_year.csv', encoding='utf-8-sig')
print("Summary statistics exported to: summary_by_province_year.csv")

# Export UNAIDS indicators data
unaids_indicators = [
    'Nombre de clients testés',
    'Nombre de clients diagnostiqués VIH+',
    'Nombre de PVVIH sous TAR',
    'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
]
unaids_df = df_clean[df_clean['indicateurs'].isin(unaids_indicators)]
unaids_df.to_csv('unaids_95_95_95_data.csv', index=False, encoding='utf-8-sig')
print("UNAIDS 95-95-95 data exported to: unaids_95_95_95_data.csv")

# ============================================================================
# SECTION 14: FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 14: ANALYSIS SUMMARY")
print("=" * 80)

print(f"""
DATASET OVERVIEW:
----------------
- Total Records: {len(df_clean):,}
- Total Columns: {len(df_clean.columns)}
- Time Period: {df_clean['annees'].min()} - {df_clean['annees'].max()}
- Provinces Covered: {df_clean['provinces'].nunique()}
- Indicators Tracked: {df_clean['indicateurs'].nunique()}

KEY FINDINGS:
-------------
1. Top 3 Provinces by Total Values:
   {', '.join(df_clean.groupby('provinces')['Valeur'].sum().nlargest(3).index.tolist())}

2. Yearly Growth Trend:
   - The data shows the evolution of HIV/AIDS response from 2020 to 2024
   
3. UNAIDS 95-95-95 Cascade:
   - Total Tested: {unaids_results['tested']:,.0f}
   - Total on Treatment (TAR): {unaids_results['on_tar']:,.0f}
   - Viral Suppression: {unaids_results['viral_suppressed']:,.0f}

4. Data Quality:
   - Missing values handled appropriately
   - Outliers identified and documented
   - Data cleaned and ready for further analysis

FILES GENERATED:
---------------
- datavih_cleaned.csv (cleaned dataset)
- summary_by_province_year.csv (summary statistics)
- unaids_95_95_95_data.csv (key indicators data)
- charts/ folder (10 visualizations)
""")

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
