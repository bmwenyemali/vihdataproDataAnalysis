-- ============================================================================
-- VIH DATA ANALYSIS PROJECT - SQL QUERIES
-- Democratic Republic of Congo - HIV/AIDS Data Analysis
-- ============================================================================
-- Author: Data Analyst Portfolio Project
-- Date: February 2026
-- Description: Comprehensive SQL queries for data extraction, analysis,
--              and business intelligence reporting
-- Database: Compatible with PostgreSQL, MySQL, SQL Server, SQLite
-- ============================================================================

-- ============================================================================
-- SECTION 1: DATABASE SETUP AND TABLE CREATION
-- ============================================================================

-- Drop table if exists (for recreation)
DROP TABLE IF EXISTS vih_data;

-- Create main data table
CREATE TABLE vih_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    provinces VARCHAR(100) NOT NULL,
    annees INT NOT NULL,
    trimestres VARCHAR(10) NOT NULL,
    indicateurs TEXT NOT NULL,
    cibles VARCHAR(100),
    sexes VARCHAR(50),
    tranches_ages VARCHAR(50),
    valeur BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for better query performance
CREATE INDEX idx_provinces ON vih_data(provinces);
CREATE INDEX idx_annees ON vih_data(annees);
CREATE INDEX idx_trimestres ON vih_data(trimestres);
CREATE INDEX idx_indicateurs ON vih_data(indicateurs(255));
CREATE INDEX idx_sexes ON vih_data(sexes);
CREATE INDEX idx_tranches_ages ON vih_data(tranches_ages);

-- Composite indexes for common query patterns
CREATE INDEX idx_province_year ON vih_data(provinces, annees);
CREATE INDEX idx_year_quarter ON vih_data(annees, trimestres);

-- ============================================================================
-- SECTION 2: BASIC DATA EXPLORATION QUERIES
-- ============================================================================

-- 2.1 View all records (limited)
SELECT * FROM vih_data LIMIT 100;

-- 2.2 Count total records
SELECT COUNT(*) AS total_records FROM vih_data;

-- 2.3 View distinct values for each categorical column
SELECT DISTINCT provinces FROM vih_data ORDER BY provinces;
SELECT DISTINCT annees FROM vih_data ORDER BY annees;
SELECT DISTINCT trimestres FROM vih_data ORDER BY trimestres;
SELECT DISTINCT sexes FROM vih_data;
SELECT DISTINCT tranches_ages FROM vih_data;

-- 2.4 Count distinct values
SELECT 
    COUNT(DISTINCT provinces) AS nb_provinces,
    COUNT(DISTINCT annees) AS nb_annees,
    COUNT(DISTINCT trimestres) AS nb_trimestres,
    COUNT(DISTINCT indicateurs) AS nb_indicateurs,
    COUNT(DISTINCT sexes) AS nb_sexes,
    COUNT(DISTINCT tranches_ages) AS nb_tranches_ages
FROM vih_data;

-- 2.5 Data types and structure (SQL Server syntax)
-- EXEC sp_columns vih_data;

-- ============================================================================
-- SECTION 3: DESCRIPTIVE STATISTICS
-- ============================================================================

-- 3.1 Basic statistics for Valeur column
SELECT 
    COUNT(valeur) AS count_values,
    SUM(valeur) AS total_sum,
    AVG(valeur) AS average_value,
    MIN(valeur) AS min_value,
    MAX(valeur) AS max_value,
    MAX(valeur) - MIN(valeur) AS range_value,
    STDDEV(valeur) AS std_deviation,
    VARIANCE(valeur) AS variance_value
FROM vih_data;

-- 3.2 Percentiles/Quartiles (PostgreSQL syntax)
SELECT 
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY valeur) AS Q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY valeur) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY valeur) AS Q3,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY valeur) - 
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY valeur) AS IQR
FROM vih_data;

-- 3.3 Statistics by Province
SELECT 
    provinces,
    COUNT(*) AS nb_records,
    SUM(valeur) AS total_value,
    ROUND(AVG(valeur), 2) AS avg_value,
    MIN(valeur) AS min_value,
    MAX(valeur) AS max_value,
    ROUND(STDDEV(valeur), 2) AS std_dev
FROM vih_data
GROUP BY provinces
ORDER BY total_value DESC;

-- 3.4 Statistics by Year
SELECT 
    annees,
    COUNT(*) AS nb_records,
    SUM(valeur) AS total_value,
    ROUND(AVG(valeur), 2) AS avg_value,
    ROUND(STDDEV(valeur), 2) AS std_dev
FROM vih_data
GROUP BY annees
ORDER BY annees;

-- 3.5 Statistics by Gender
SELECT 
    COALESCE(sexes, 'Non spécifié') AS sexe,
    COUNT(*) AS nb_records,
    SUM(valeur) AS total_value,
    ROUND(AVG(valeur), 2) AS avg_value,
    ROUND(100.0 * SUM(valeur) / (SELECT SUM(valeur) FROM vih_data), 2) AS percentage
FROM vih_data
GROUP BY sexes
ORDER BY total_value DESC;

-- ============================================================================
-- SECTION 4: DATA AGGREGATION AND GROUPING
-- ============================================================================

-- 4.1 Total by Province and Year
SELECT 
    provinces,
    annees,
    SUM(valeur) AS total_value,
    COUNT(*) AS nb_records
FROM vih_data
GROUP BY provinces, annees
ORDER BY provinces, annees;

-- 4.2 Total by Year and Quarter
SELECT 
    annees,
    trimestres,
    SUM(valeur) AS total_value,
    COUNT(DISTINCT indicateurs) AS nb_indicators_tracked
FROM vih_data
GROUP BY annees, trimestres
ORDER BY annees, trimestres;

-- 4.3 Total by Province, Year, Quarter (ROLLUP for subtotals)
SELECT 
    COALESCE(provinces, 'TOTAL') AS province,
    COALESCE(CAST(annees AS VARCHAR), 'ALL YEARS') AS annee,
    SUM(valeur) AS total_value
FROM vih_data
GROUP BY ROLLUP(provinces, annees)
ORDER BY provinces NULLS LAST, annees NULLS LAST;

-- 4.4 Pivot: Values by Province and Year (using CASE WHEN)
SELECT 
    provinces,
    SUM(CASE WHEN annees = 2020 THEN valeur ELSE 0 END) AS "2020",
    SUM(CASE WHEN annees = 2021 THEN valeur ELSE 0 END) AS "2021",
    SUM(CASE WHEN annees = 2022 THEN valeur ELSE 0 END) AS "2022",
    SUM(CASE WHEN annees = 2023 THEN valeur ELSE 0 END) AS "2023",
    SUM(CASE WHEN annees = 2024 THEN valeur ELSE 0 END) AS "2024",
    SUM(valeur) AS total
FROM vih_data
GROUP BY provinces
ORDER BY total DESC;

-- 4.5 Cross-tabulation: Gender vs Age Groups
SELECT 
    COALESCE(sexes, 'Non spécifié') AS sexe,
    SUM(CASE WHEN tranches_ages = '< 10 ans' THEN valeur ELSE 0 END) AS "< 10 ans",
    SUM(CASE WHEN tranches_ages = '10 à 14 ans' THEN valeur ELSE 0 END) AS "10-14 ans",
    SUM(CASE WHEN tranches_ages = '15 à 19 ans' THEN valeur ELSE 0 END) AS "15-19 ans",
    SUM(CASE WHEN tranches_ages = '20 à 24 ans' THEN valeur ELSE 0 END) AS "20-24 ans",
    SUM(CASE WHEN tranches_ages = '25 à 49 ans' THEN valeur ELSE 0 END) AS "25-49 ans",
    SUM(CASE WHEN tranches_ages = '>= 50 ans' THEN valeur ELSE 0 END) AS ">= 50 ans"
FROM vih_data
GROUP BY sexes;

-- ============================================================================
-- SECTION 5: UNAIDS 95-95-95 CASCADE ANALYSIS
-- ============================================================================

-- 5.1 First 95: HIV Testing - People who know their status
SELECT 
    'Testing (1st 95)' AS indicator_category,
    annees,
    SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS total_tested,
    SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END) AS total_diagnosed
FROM vih_data
WHERE indicateurs IN ('Nombre de clients testés', 'Nombre de clients diagnostiqués VIH+')
GROUP BY annees
ORDER BY annees;

-- 5.2 Second 95: Treatment - People on antiretroviral therapy
SELECT 
    'Treatment (2nd 95)' AS indicator_category,
    annees,
    SUM(valeur) AS total_on_tar
FROM vih_data
WHERE indicateurs = 'Nombre de PVVIH sous TAR'
GROUP BY annees
ORDER BY annees;

-- 5.3 Third 95: Viral Suppression
SELECT 
    'Viral Suppression (3rd 95)' AS indicator_category,
    annees,
    SUM(valeur) AS total_viral_suppression
FROM vih_data
WHERE indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
GROUP BY annees
ORDER BY annees;

-- 5.4 Complete UNAIDS Cascade by Year
SELECT 
    annees,
    SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS tested,
    SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END) AS diagnosed_hiv_positive,
    SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS on_treatment_tar,
    SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS viral_suppression,
    -- Calculate cascade percentages (simplified)
    ROUND(100.0 * SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END), 0), 2) AS pct_on_treatment,
    ROUND(100.0 * SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END), 0), 2) AS pct_viral_suppression
FROM vih_data
WHERE indicateurs IN (
    'Nombre de clients testés',
    'Nombre de clients diagnostiqués VIH+',
    'Nombre de PVVIH sous TAR',
    'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
)
GROUP BY annees
ORDER BY annees;

-- 5.5 UNAIDS Cascade by Province
SELECT 
    provinces,
    SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS tested,
    SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END) AS diagnosed,
    SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS on_tar,
    SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS viral_suppressed
FROM vih_data
WHERE indicateurs IN (
    'Nombre de clients testés',
    'Nombre de clients diagnostiqués VIH+',
    'Nombre de PVVIH sous TAR',
    'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
)
GROUP BY provinces
ORDER BY tested DESC;

-- ============================================================================
-- SECTION 6: TOP N ANALYSIS
-- ============================================================================

-- 6.1 Top 10 Provinces by Total Value
SELECT 
    provinces,
    SUM(valeur) AS total_value,
    COUNT(*) AS nb_records,
    ROUND(AVG(valeur), 2) AS avg_value
FROM vih_data
GROUP BY provinces
ORDER BY total_value DESC
LIMIT 10;

-- 6.2 Top 5 Indicators by Total Value
SELECT 
    indicateurs,
    SUM(valeur) AS total_value,
    COUNT(*) AS nb_occurrences
FROM vih_data
GROUP BY indicateurs
ORDER BY total_value DESC
LIMIT 5;

-- 6.3 Top Provinces for Condom Distribution
SELECT 
    provinces,
    annees,
    SUM(valeur) AS total_condoms_distributed
FROM vih_data
WHERE indicateurs = 'Nombre de préservatifs masculins distribués'
GROUP BY provinces, annees
ORDER BY total_condoms_distributed DESC
LIMIT 10;

-- 6.4 Bottom 5 Provinces by Testing (identify areas needing attention)
SELECT 
    provinces,
    SUM(valeur) AS total_tested
FROM vih_data
WHERE indicateurs = 'Nombre de clients testés'
GROUP BY provinces
ORDER BY total_tested ASC
LIMIT 5;

-- ============================================================================
-- SECTION 7: YEAR-OVER-YEAR ANALYSIS
-- ============================================================================

-- 7.1 Year-over-Year Growth Rate
WITH yearly_totals AS (
    SELECT 
        annees,
        SUM(valeur) AS total_value
    FROM vih_data
    GROUP BY annees
)
SELECT 
    y1.annees,
    y1.total_value,
    y2.total_value AS previous_year_value,
    ROUND(100.0 * (y1.total_value - y2.total_value) / NULLIF(y2.total_value, 0), 2) AS yoy_growth_pct
FROM yearly_totals y1
LEFT JOIN yearly_totals y2 ON y1.annees = y2.annees + 1
ORDER BY y1.annees;

-- 7.2 Year-over-Year Growth by Province
WITH province_yearly AS (
    SELECT 
        provinces,
        annees,
        SUM(valeur) AS total_value
    FROM vih_data
    GROUP BY provinces, annees
)
SELECT 
    py1.provinces,
    py1.annees,
    py1.total_value,
    LAG(py1.total_value) OVER (PARTITION BY py1.provinces ORDER BY py1.annees) AS previous_year,
    ROUND(100.0 * (py1.total_value - LAG(py1.total_value) OVER (PARTITION BY py1.provinces ORDER BY py1.annees)) / 
          NULLIF(LAG(py1.total_value) OVER (PARTITION BY py1.provinces ORDER BY py1.annees), 0), 2) AS yoy_growth_pct
FROM province_yearly py1
ORDER BY py1.provinces, py1.annees;

-- 7.3 Year-over-Year Growth for TAR (Treatment)
WITH tar_yearly AS (
    SELECT 
        annees,
        SUM(valeur) AS total_on_tar
    FROM vih_data
    WHERE indicateurs = 'Nombre de PVVIH sous TAR'
    GROUP BY annees
)
SELECT 
    annees,
    total_on_tar,
    LAG(total_on_tar) OVER (ORDER BY annees) AS prev_year_tar,
    total_on_tar - LAG(total_on_tar) OVER (ORDER BY annees) AS absolute_change,
    ROUND(100.0 * (total_on_tar - LAG(total_on_tar) OVER (ORDER BY annees)) / 
          NULLIF(LAG(total_on_tar) OVER (ORDER BY annees), 0), 2) AS pct_change
FROM tar_yearly
ORDER BY annees;

-- ============================================================================
-- SECTION 8: COMPARATIVE ANALYSIS
-- ============================================================================

-- 8.1 Province Comparison: Above/Below Average
WITH province_avg AS (
    SELECT AVG(total_value) AS overall_avg
    FROM (
        SELECT provinces, SUM(valeur) AS total_value
        FROM vih_data
        GROUP BY provinces
    ) p
)
SELECT 
    provinces,
    SUM(valeur) AS total_value,
    (SELECT overall_avg FROM province_avg) AS national_average,
    CASE 
        WHEN SUM(valeur) > (SELECT overall_avg FROM province_avg) THEN 'Above Average'
        WHEN SUM(valeur) < (SELECT overall_avg FROM province_avg) THEN 'Below Average'
        ELSE 'Equal to Average'
    END AS performance_status,
    ROUND(100.0 * (SUM(valeur) - (SELECT overall_avg FROM province_avg)) / 
          (SELECT overall_avg FROM province_avg), 2) AS pct_diff_from_avg
FROM vih_data
GROUP BY provinces
ORDER BY total_value DESC;

-- 8.2 Gender Comparison by Province
SELECT 
    provinces,
    SUM(CASE WHEN sexes = 'Masculin' THEN valeur ELSE 0 END) AS male_value,
    SUM(CASE WHEN sexes = 'Féminin' THEN valeur ELSE 0 END) AS female_value,
    ROUND(100.0 * SUM(CASE WHEN sexes = 'Masculin' THEN valeur ELSE 0 END) / 
          NULLIF(SUM(valeur), 0), 2) AS male_pct,
    ROUND(100.0 * SUM(CASE WHEN sexes = 'Féminin' THEN valeur ELSE 0 END) / 
          NULLIF(SUM(valeur), 0), 2) AS female_pct
FROM vih_data
WHERE sexes IS NOT NULL
GROUP BY provinces
ORDER BY provinces;

-- 8.3 Age Group Distribution by Year
SELECT 
    annees,
    COALESCE(tranches_ages, 'Non spécifié') AS age_group,
    SUM(valeur) AS total_value,
    ROUND(100.0 * SUM(valeur) / SUM(SUM(valeur)) OVER (PARTITION BY annees), 2) AS pct_of_year
FROM vih_data
GROUP BY annees, tranches_ages
ORDER BY annees, age_group;

-- ============================================================================
-- SECTION 9: RANKING AND WINDOW FUNCTIONS
-- ============================================================================

-- 9.1 Rank Provinces by Total Value
SELECT 
    provinces,
    SUM(valeur) AS total_value,
    RANK() OVER (ORDER BY SUM(valeur) DESC) AS rank_by_value,
    DENSE_RANK() OVER (ORDER BY SUM(valeur) DESC) AS dense_rank,
    ROW_NUMBER() OVER (ORDER BY SUM(valeur) DESC) AS row_num,
    ROUND(100.0 * SUM(valeur) / SUM(SUM(valeur)) OVER (), 2) AS pct_of_total
FROM vih_data
GROUP BY provinces
ORDER BY total_value DESC;

-- 9.2 Rank Provinces within Each Year
SELECT 
    annees,
    provinces,
    SUM(valeur) AS total_value,
    RANK() OVER (PARTITION BY annees ORDER BY SUM(valeur) DESC) AS rank_in_year
FROM vih_data
GROUP BY annees, provinces
ORDER BY annees, rank_in_year;

-- 9.3 Cumulative Sum by Year
SELECT 
    annees,
    trimestres,
    SUM(valeur) AS quarterly_value,
    SUM(SUM(valeur)) OVER (PARTITION BY annees ORDER BY trimestres) AS cumulative_value,
    SUM(SUM(valeur)) OVER (PARTITION BY annees) AS annual_total,
    ROUND(100.0 * SUM(SUM(valeur)) OVER (PARTITION BY annees ORDER BY trimestres) / 
          NULLIF(SUM(SUM(valeur)) OVER (PARTITION BY annees), 0), 2) AS pct_cumulative
FROM vih_data
GROUP BY annees, trimestres
ORDER BY annees, trimestres;

-- 9.4 Running Average
SELECT 
    annees,
    SUM(valeur) AS yearly_total,
    AVG(SUM(valeur)) OVER (ORDER BY annees ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg,
    AVG(SUM(valeur)) OVER (ORDER BY annees ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_3yr
FROM vih_data
GROUP BY annees
ORDER BY annees;

-- ============================================================================
-- SECTION 10: DATA QUALITY CHECKS
-- ============================================================================

-- 10.1 Check for NULL values
SELECT 
    SUM(CASE WHEN provinces IS NULL THEN 1 ELSE 0 END) AS null_provinces,
    SUM(CASE WHEN annees IS NULL THEN 1 ELSE 0 END) AS null_annees,
    SUM(CASE WHEN trimestres IS NULL THEN 1 ELSE 0 END) AS null_trimestres,
    SUM(CASE WHEN indicateurs IS NULL THEN 1 ELSE 0 END) AS null_indicateurs,
    SUM(CASE WHEN sexes IS NULL THEN 1 ELSE 0 END) AS null_sexes,
    SUM(CASE WHEN tranches_ages IS NULL THEN 1 ELSE 0 END) AS null_tranches_ages,
    SUM(CASE WHEN valeur IS NULL THEN 1 ELSE 0 END) AS null_valeur
FROM vih_data;

-- 10.2 Check for Duplicate Records
SELECT 
    provinces, annees, trimestres, indicateurs, cibles, sexes, tranches_ages, valeur,
    COUNT(*) AS duplicate_count
FROM vih_data
GROUP BY provinces, annees, trimestres, indicateurs, cibles, sexes, tranches_ages, valeur
HAVING COUNT(*) > 1
LIMIT 20;

-- 10.3 Check for Negative Values (should be 0 or positive)
SELECT * FROM vih_data WHERE valeur < 0;

-- 10.4 Identify Potential Outliers (values significantly above average)
WITH stats AS (
    SELECT 
        AVG(valeur) AS avg_val,
        STDDEV(valeur) AS std_val
    FROM vih_data
)
SELECT 
    v.*,
    (v.valeur - s.avg_val) / NULLIF(s.std_val, 0) AS z_score
FROM vih_data v, stats s
WHERE (v.valeur - s.avg_val) / NULLIF(s.std_val, 0) > 3
ORDER BY z_score DESC
LIMIT 50;

-- 10.5 Data Completeness Check
SELECT 
    annees,
    COUNT(DISTINCT provinces) AS provinces_covered,
    COUNT(DISTINCT trimestres) AS quarters_covered,
    COUNT(DISTINCT indicateurs) AS indicators_tracked,
    COUNT(*) AS total_records
FROM vih_data
GROUP BY annees
ORDER BY annees;

-- ============================================================================
-- SECTION 11: ADVANCED ANALYTICAL QUERIES
-- ============================================================================

-- 11.1 Provincial Performance Scoring
WITH province_metrics AS (
    SELECT 
        provinces,
        SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS testing_score,
        SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS treatment_score,
        SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS suppression_score
    FROM vih_data
    GROUP BY provinces
)
SELECT 
    provinces,
    testing_score,
    treatment_score,
    suppression_score,
    (testing_score + treatment_score + suppression_score) AS composite_score,
    NTILE(4) OVER (ORDER BY (testing_score + treatment_score + suppression_score) DESC) AS performance_quartile
FROM province_metrics
ORDER BY composite_score DESC;

-- 11.2 Trend Classification
WITH yearly_change AS (
    SELECT 
        provinces,
        annees,
        SUM(valeur) AS total_value,
        LAG(SUM(valeur)) OVER (PARTITION BY provinces ORDER BY annees) AS prev_value
    FROM vih_data
    GROUP BY provinces, annees
)
SELECT 
    provinces,
    annees,
    total_value,
    prev_value,
    CASE 
        WHEN prev_value IS NULL THEN 'Baseline'
        WHEN total_value > prev_value * 1.1 THEN 'Significant Increase (>10%)'
        WHEN total_value > prev_value THEN 'Moderate Increase'
        WHEN total_value < prev_value * 0.9 THEN 'Significant Decrease (>10%)'
        WHEN total_value < prev_value THEN 'Moderate Decrease'
        ELSE 'Stable'
    END AS trend_classification
FROM yearly_change
ORDER BY provinces, annees;

-- 11.3 Seasonal Analysis (Quarterly Patterns)
SELECT 
    trimestres,
    ROUND(AVG(valeur), 2) AS avg_value,
    SUM(valeur) AS total_value,
    COUNT(*) AS nb_records,
    ROUND(STDDEV(valeur), 2) AS value_volatility
FROM vih_data
GROUP BY trimestres
ORDER BY trimestres;

-- 11.4 Cohort Analysis by Starting Year
WITH first_record AS (
    SELECT 
        provinces,
        MIN(annees) AS first_year
    FROM vih_data
    GROUP BY provinces
)
SELECT 
    fr.first_year AS cohort_year,
    COUNT(DISTINCT fr.provinces) AS provinces_in_cohort,
    SUM(v.valeur) AS total_value_all_time
FROM first_record fr
JOIN vih_data v ON fr.provinces = v.provinces
GROUP BY fr.first_year
ORDER BY fr.first_year;

-- ============================================================================
-- SECTION 12: REPORTING VIEWS
-- ============================================================================

-- 12.1 Create Summary View
CREATE OR REPLACE VIEW v_provincial_summary AS
SELECT 
    provinces,
    COUNT(*) AS total_records,
    SUM(valeur) AS total_value,
    ROUND(AVG(valeur), 2) AS avg_value,
    MIN(annees) AS first_year,
    MAX(annees) AS last_year,
    COUNT(DISTINCT indicateurs) AS indicators_tracked
FROM vih_data
GROUP BY provinces;

-- 12.2 Create UNAIDS Cascade View
CREATE OR REPLACE VIEW v_unaids_cascade AS
SELECT 
    annees,
    provinces,
    SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS tested,
    SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END) AS diagnosed,
    SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS on_treatment,
    SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS viral_suppressed
FROM vih_data
WHERE indicateurs IN (
    'Nombre de clients testés',
    'Nombre de clients diagnostiqués VIH+',
    'Nombre de PVVIH sous TAR',
    'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
)
GROUP BY annees, provinces;

-- 12.3 Create Yearly Performance View
CREATE OR REPLACE VIEW v_yearly_performance AS
SELECT 
    annees,
    SUM(valeur) AS total_value,
    COUNT(DISTINCT provinces) AS active_provinces,
    COUNT(DISTINCT indicateurs) AS indicators_tracked,
    COUNT(*) AS total_records
FROM vih_data
GROUP BY annees;

-- ============================================================================
-- SECTION 13: STORED PROCEDURES (MySQL Syntax)
-- ============================================================================

-- 13.1 Procedure to get Province Statistics
DELIMITER //
CREATE PROCEDURE GetProvinceStats(IN p_province VARCHAR(100))
BEGIN
    SELECT 
        provinces,
        annees,
        COUNT(*) AS records,
        SUM(valeur) AS total_value,
        ROUND(AVG(valeur), 2) AS avg_value
    FROM vih_data
    WHERE provinces = p_province
    GROUP BY provinces, annees
    ORDER BY annees;
END //
DELIMITER ;

-- 13.2 Procedure to get UNAIDS Indicators for a specific year
DELIMITER //
CREATE PROCEDURE GetUNAIDSCascade(IN p_year INT)
BEGIN
    SELECT 
        provinces,
        SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS tested,
        SUM(CASE WHEN indicateurs = 'Nombre de clients diagnostiqués VIH+' THEN valeur ELSE 0 END) AS diagnosed,
        SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS on_tar,
        SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS viral_suppressed
    FROM vih_data
    WHERE annees = p_year
      AND indicateurs IN (
          'Nombre de clients testés',
          'Nombre de clients diagnostiqués VIH+',
          'Nombre de PVVIH sous TAR',
          'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale'
      )
    GROUP BY provinces
    ORDER BY tested DESC;
END //
DELIMITER ;

-- Usage: CALL GetProvinceStats('Kinshasa');
-- Usage: CALL GetUNAIDSCascade(2023);

-- ============================================================================
-- SECTION 14: COMMON TABLE EXPRESSIONS (CTEs) FOR COMPLEX ANALYSIS
-- ============================================================================

-- 14.1 Multi-step Analysis with CTEs
WITH 
testing_data AS (
    SELECT 
        provinces,
        annees,
        SUM(valeur) AS total_tested
    FROM vih_data
    WHERE indicateurs = 'Nombre de clients testés'
    GROUP BY provinces, annees
),
treatment_data AS (
    SELECT 
        provinces,
        annees,
        SUM(valeur) AS total_on_tar
    FROM vih_data
    WHERE indicateurs = 'Nombre de PVVIH sous TAR'
    GROUP BY provinces, annees
),
provincial_ranking AS (
    SELECT 
        t.provinces,
        t.annees,
        t.total_tested,
        COALESCE(tr.total_on_tar, 0) AS total_on_tar,
        RANK() OVER (PARTITION BY t.annees ORDER BY t.total_tested DESC) AS testing_rank,
        RANK() OVER (PARTITION BY t.annees ORDER BY COALESCE(tr.total_on_tar, 0) DESC) AS treatment_rank
    FROM testing_data t
    LEFT JOIN treatment_data tr ON t.provinces = tr.provinces AND t.annees = tr.annees
)
SELECT 
    provinces,
    annees,
    total_tested,
    total_on_tar,
    testing_rank,
    treatment_rank,
    testing_rank + treatment_rank AS combined_rank_score
FROM provincial_ranking
WHERE annees = 2024
ORDER BY combined_rank_score;

-- ============================================================================
-- SECTION 15: EXPORT QUERIES FOR REPORTING
-- ============================================================================

-- 15.1 Executive Summary Data
SELECT 
    'HIV Data Analysis Summary - DRC' AS report_title,
    MIN(annees) AS period_start,
    MAX(annees) AS period_end,
    COUNT(DISTINCT provinces) AS provinces_covered,
    COUNT(DISTINCT indicateurs) AS indicators_tracked,
    SUM(valeur) AS total_program_value,
    COUNT(*) AS total_records
FROM vih_data;

-- 15.2 Key Performance Indicators (KPIs)
SELECT 
    annees,
    SUM(CASE WHEN indicateurs = 'Nombre de clients testés' THEN valeur ELSE 0 END) AS kpi_testing,
    SUM(CASE WHEN indicateurs = 'Nombre de PVVIH sous TAR' THEN valeur ELSE 0 END) AS kpi_treatment,
    SUM(CASE WHEN indicateurs = 'Nombre  de PVVIH sous TAR qui ont supprimée la charge virale' THEN valeur ELSE 0 END) AS kpi_viral_suppression,
    SUM(CASE WHEN indicateurs = 'Nombre de préservatifs masculins distribués' THEN valeur ELSE 0 END) AS kpi_prevention
FROM vih_data
GROUP BY annees
ORDER BY annees;

-- 15.3 Provincial Dashboard Data
SELECT 
    provinces,
    SUM(valeur) AS total_value,
    COUNT(DISTINCT annees) AS years_active,
    ROUND(100.0 * SUM(valeur) / (SELECT SUM(valeur) FROM vih_data), 2) AS national_share_pct,
    RANK() OVER (ORDER BY SUM(valeur) DESC) AS national_rank
FROM vih_data
GROUP BY provinces
ORDER BY total_value DESC;

-- ============================================================================
-- END OF SQL ANALYSIS FILE
-- ============================================================================
