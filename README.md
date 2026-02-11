# VIH Data Analysis Project - Democratic Republic of Congo

## Project Overview

This project presents a comprehensive data analytics portfolio demonstrating proficiency in **Python**, **SQL**, and **Power BI** through the analysis of HIV/AIDS data from the Democratic Republic of Congo (DRC).

### UNAIDS 95-95-95 Targets Focus

- **First 95:** 95% of people living with HIV know their status
- **Second 95:** 95% of people who know their status are on treatment
- **Third 95:** 95% of people on treatment have suppressed viral loads

## Dataset

- **Source:** datavih.xlsx
- **Records:** 85,811 rows
- **Period:** 2020-2024
- **Provinces:** 26 (all provinces of DRC)
- **Indicators:** 118 health metrics

## Project Structure

```
VIHDatapro/
|-- datavih.xlsx                    # Original dataset
|-- datavih_cleaned.csv             # Cleaned dataset (generated)
|-- vih_data_analysis.py            # Python analysis script
|-- vih_data_analysis.sql           # SQL queries
|-- PowerBI_Dashboard_Guide.md      # Power BI setup guide
|-- Project_Report.md               # Full project documentation
|-- Presentation_Content.md         # PowerPoint content
|-- charts/                         # Generated visualizations
|   |-- 01_value_distribution.png
|   |-- 02_yearly_trend.png
|   |-- 03_top_provinces.png
|   |-- 04_gender_distribution.png
|   |-- 05_age_groups.png
|   |-- 06_quarterly_heatmap.png
|   |-- 07_outlier_scatter.png
|   |-- 08_province_trends.png
|   |-- 09_unaids_cascade.png
|   |-- 10_correlation_matrix.png
|-- README.md                       # This file
```

## Technologies Used

| Technology     | Purpose                                    |
| -------------- | ------------------------------------------ |
| **Python**     | Data extraction, cleaning, EDA, statistics |
| **pandas**     | Data manipulation                          |
| **numpy**      | Numerical operations                       |
| **matplotlib** | Data visualization                         |
| **seaborn**    | Statistical visualization                  |
| **scipy**      | Statistical tests                          |
| **SQL**        | Data aggregation, reporting                |
| **Power BI**   | Interactive dashboards                     |
| **Excel**      | Data source                                |

## Python Analysis Features

### Data Processing

- Data extraction from Excel
- Missing value handling
- Outlier detection (IQR and Z-score methods)
- Data type standardization

### Statistical Analysis

- Descriptive statistics (mean, median, std, quartiles)
- Normality tests (D'Agostino-Pearson)
- T-tests for group comparison
- Chi-square tests for independence
- Year-over-year growth analysis

### Visualizations

1. Value distribution histograms
2. Yearly trend bar charts
3. Provincial ranking charts
4. Gender distribution (pie/bar)
5. Age group analysis
6. Quarterly heatmaps
7. Outlier scatter plots
8. Multi-line province trends
9. UNAIDS cascade visualization
10. Correlation matrices

### Custom Functions

```python
def calculate_unaids_95_95_95(df)      # UNAIDS cascade metrics
def detect_outliers_iqr(data, column)  # IQR-based outlier detection
def detect_outliers_zscore(data, col)  # Z-score outlier detection
def top_provinces_by_indicator(df, indicator, n)  # Top N ranking
def year_over_year_comparison(df, indicator)  # YoY analysis
```

## SQL Analysis Features

### Query Categories

- Basic exploration and counts
- Descriptive statistics
- Data aggregation (GROUP BY, ROLLUP)
- UNAIDS 95-95-95 cascade queries
- Year-over-year analysis
- Window functions (RANK, LAG, cumulative)
- Data quality checks
- Views and stored procedures

### Key Queries

- Provincial summary statistics
- Gender/age cross-tabulations
- Yearly trend analysis
- Top N rankings
- Outlier detection

## Power BI Dashboard

### Pages

1. **Home:** Navigation menu
2. **Overview:** Executive summary with KPIs
3. **Testing (1st 95):** HIV testing analysis
4. **Treatment (2nd 95):** TAR coverage
5. **Suppression (3rd 95):** Viral load monitoring
6. **Provincial:** Detailed province analysis
7. **Trends:** Time-based analysis and forecasting

### DAX Measures

- Total Tested
- Total Diagnosed
- Total on TAR
- Viral Suppression Rate
- Treatment Coverage Rate
- Year-over-Year Growth

## How to Run

### Python Script

```bash
cd VIHDatapro
python vih_data_analysis.py
```

### Output

- Console: Detailed analysis results
- Files: CSV exports and PNG charts

## Key Findings

1. **85,811 records** analyzed across 26 provinces
2. **118 indicators** tracked for HIV response
3. Top provinces identified: Kinshasa, Haut-Katanga, Nord-Kivu
4. **18% outliers** detected using IQR method
5. Non-normal distribution requiring non-parametric analysis
6. Significant relationship between gender and province (Chi-square)

## Author

**Bienvenu Mwenyemali**

- **GitHub:** [bmwenyemali](https://github.com/bmwenyemali)
- **Repository:** [vihdataproDataAnalysis](https://github.com/bmwenyemali/vihdataproDataAnalysis)

## License

This project is for educational and portfolio demonstration purposes.

---

_Created: February 2026_
