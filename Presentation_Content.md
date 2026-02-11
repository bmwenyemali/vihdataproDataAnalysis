# VIH DATA ANALYSIS PROJECT

## PowerPoint Presentation Content

---

### SLIDE 1: TITLE SLIDE

**VIH DATA ANALYSIS PROJECT**
Democratic Republic of Congo

HIV/AIDS Data Analytics Portfolio

Author: Bienvenu Mwenyemali
Date: February 2026

---

### SLIDE 2: PROJECT OVERVIEW

**Objective:** Analyze HIV/AIDS data from DRC to track UNAIDS 95-95-95 targets

**Scope:**

- 85,811 records analyzed
- 26 provinces covered
- 5 years of data (2020-2024)
- 118 health indicators

**Tools Used:**

- Microsoft Excel
- Python (pandas, matplotlib, seaborn, scipy)
- SQL
- Power BI

---

### SLIDE 3: DATA PIPELINE

**Step 1:** Excel Data Source
|
**Step 2:** Python ETL (Extract, Transform, Load)
|
**Step 3:** Statistical Analysis
|
**Step 4:** SQL Queries
|
**Step 5:** Power BI Dashboard
|
**Step 6:** Insights and Recommendations

---

### SLIDE 4: UNAIDS 95-95-95 TARGETS

**The Global HIV Treatment Cascade:**

**1st 95**: 95% of PLHIV know their HIV status
--> Indicator: Testing coverage

**2nd 95**: 95% of diagnosed on treatment (TAR)
--> Indicator: Treatment enrollment

**3rd 95**: 95% on treatment with viral suppression
--> Indicator: Viral load monitoring

---

### SLIDE 5: PYTHON ANALYSIS HIGHLIGHTS

**Data Processing:**

- Loaded 85,811 records from Excel
- Handled missing values (15% in gender, 10% in age)
- Detected outliers using IQR and Z-score methods

**Key Functions Developed:**

- calculate_unaids_95_95_95()
- detect_outliers_iqr()
- year_over_year_comparison()

**Statistical Tests:**

- Normality test (D'Agostino-Pearson)
- T-test for gender comparison
- Chi-square for categorical analysis

---

### SLIDE 6: SQL ANALYSIS CAPABILITIES

**Query Categories:**

1. Descriptive Statistics
   - COUNT, SUM, AVG, MIN, MAX

2. Data Aggregation
   - GROUP BY, ROLLUP, PIVOT

3. Window Functions
   - RANK, LAG, cumulative sums

4. Year-over-Year Analysis
   - CTEs for growth calculations

5. Stored Procedures
   - GetProvinceStats()
   - GetUNAIDSCascade()

---

### SLIDE 7: POWER BI DASHBOARD

**Dashboard Structure:**

- Home/Navigation Menu
- Executive Overview (KPIs)
- 1st 95: Testing Analysis
- 2nd 95: Treatment Analysis
- 3rd 95: Viral Suppression
- Provincial Deep-dive
- Trends and Forecasting

**Interactive Features:**

- Year/Quarter slicers
- Province filters
- Cross-filtering visuals

---

### SLIDE 8: KEY FINDINGS

**1. Top Performing Provinces:**

- Kinshasa (capital)
- Haut-Katanga
- Nord-Kivu

**2. Data Quality Observations:**

- 18% outliers detected (IQR method)
- Non-normal distribution of values
- Significant gender-province relationship

**3. Year-over-Year Trends:**

- Growth patterns identified
- Seasonal variations in Q1 vs Q4

---

### SLIDE 9: RECOMMENDATIONS

**1. Testing Coverage:**

- Scale up testing in low-coverage provinces
- Implement community-based testing

**2. Treatment Linkage:**

- Reduce diagnosis-to-treatment time
- Strengthen referral systems

**3. Viral Suppression:**

- Expand viral load testing capacity
- Support adherence programs

**4. Data Quality:**

- Standardize data collection
- Real-time validation systems

---

### SLIDE 10: TECHNICAL SKILLS DEMONSTRATED

**Data Analytics:**

- Data extraction and cleaning
- Exploratory data analysis
- Statistical testing
- Outlier detection

**Programming:**

- Python (pandas, numpy, scipy)
- SQL (advanced queries)
- DAX (Power BI measures)

**Visualization:**

- matplotlib/seaborn charts
- Power BI dashboards
- Interactive reports

---

### SLIDE 11: PROJECT DELIVERABLES

| File                       | Description           |
| -------------------------- | --------------------- |
| datavih.xlsx               | Original dataset      |
| vih_data_analysis.py       | Python analysis       |
| vih_data_analysis.sql      | SQL queries           |
| PowerBI_Dashboard_Guide.md | Dashboard specs       |
| Project_Report.md          | Full documentation    |
| charts/                    | Visualization outputs |

GitHub: github.com/bmwenyemali/vihdataproDataAnalysis

---

### SLIDE 12: THANK YOU

**Questions?**

Author: Bienvenu Mwenyemali
GitHub: github.com/bmwenyemali/vihdataproDataAnalysis

---

## NOTES FOR POWERPOINT CREATION:

1. Use clean, professional template (no excessive icons)
2. Color scheme: Blue (#2C3E50), Red (#E74C3C), White
3. Font: Segoe UI or Arial
4. Keep text minimal - bullet points only
5. Add data visualizations where appropriate
6. Include screenshots of Python code/output
7. Show SQL query examples
8. Add Power BI dashboard screenshots
