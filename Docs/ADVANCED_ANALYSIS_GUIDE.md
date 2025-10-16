# 📊 Advanced Data Analysis Documentation

## Overview

The Malackathon Health Dashboard now includes three sophisticated analysis modules designed for deep clinical and operational insights. These modules follow software engineering best practices and leverage the full Oracle database schema for comprehensive mental health data analysis.

---

## 🏗️ Architecture & Design Principles

### **1. Separation of Concerns**
- **Layouts** (`layouts/`): Pure presentation layer with no business logic
- **Callbacks** (`callbacks/`): Interactive logic and UI updates
- **Data Layer** (`data/db_utils.py`): All SQL queries centralized
- **Configuration** (`config/`): Database connection management

### **2. Modularity**
Each analysis module is self-contained with:
- Dedicated layout file
- Dedicated callback file
- Reusable components
- Independent routing

### **3. Performance Optimization**
- Connection pooling for database efficiency
- Parameterized queries to prevent SQL injection
- Client-side data caching with `dcc.Store`
- Lazy loading of charts (only load when data available)

### **4. Responsive Design**
- Bootstrap grid system (xl/lg/md/sm/xs breakpoints)
- Mobile-first approach
- Auto-adjusting charts with Plotly's automargin
- Accessible UI with proper ARIA labels

---

## 📈 Module 1: Cohort Analysis

**Route**: `/cohort-analysis`

### Purpose
Track patient journeys through multiple hospital admissions, analyze readmission patterns, and identify high-utilization cohorts.

### Key Features

#### **1. Readmission Analysis**
```sql
-- Calculates 30-day readmission rates using window functions
WITH PatientAdmissions AS (
    SELECT 
        ID_PACIENTE,
        FECHA_DE_INGRESO,
        FECHA_DE_FIN_CONTACTO,
        LEAD(FECHA_DE_INGRESO) OVER (
            PARTITION BY ID_PACIENTE 
            ORDER BY FECHA_DE_INGRESO
        ) AS next_admission
    FROM INGRESO
)
-- Identifies patients readmitted within threshold days
```

**Metrics Provided**:
- Total readmission rate (%)
- Average days to readmission
- Distribution of readmitted vs non-readmitted patients

#### **2. Patient Journey Tracking**
```sql
-- Tracks patients with multiple admissions
SELECT 
    ID_PACIENTE,
    COUNT(*) AS admission_count,
    SUM(ESTANCIA_DIAS) AS total_days,
    SUM(COSTE_APR) AS total_cost,
    MAX(FECHA_DE_INGRESO) - MIN(FECHA_DE_INGRESO) AS journey_length
FROM INGRESO
GROUP BY ID_PACIENTE
HAVING COUNT(*) >= 2
```

**Visualizations**:
- Scatter plot: Admissions vs Total Cost (size = total days)
- Dual-axis chart: Cost accumulation by admission frequency

#### **3. Comorbidity Analysis**
```sql
-- Counts diagnoses per admission
SELECT 
    (CASE WHEN DIAGNOSTICO_PRINCIPAL IS NOT NULL THEN 1 ELSE 0 END +
     CASE WHEN DIAGNOSTICO_2 IS NOT NULL THEN 1 ELSE 0 END +
     ...) AS num_diagnoses,
    COUNT(*) AS patient_count
FROM DIAGNOSTICOS_INGRESO
GROUP BY num_diagnoses
```

**Chart**: Bar chart showing patient distribution by number of diagnoses

### Filters
- **Date Range**: Focus on specific time periods
- **Readmission Threshold**: 7, 14, 30, 60, or 90 days
- **Minimum Admissions**: Filter cohort by admission frequency (2-10+)

### Use Cases
1. **Identify high-risk patients** for readmission interventions
2. **Resource planning** based on cohort size and costs
3. **Comorbidity research** to understand diagnosis complexity
4. **Quality improvement** by tracking readmission trends

---

## 🏥 Module 2: Clinical Insights

**Route**: `/clinical-insights`

### Purpose
Understand clinical patterns through severity analysis, risk stratification, diagnosis correlations, and outcome metrics.

### Key Features

#### **1. Severity Analysis**
```sql
-- Analyzes metrics by APR severity level (1-4)
SELECT 
    NIVEL_SEVERIDAD_APR,
    COUNT(*) AS patient_count,
    AVG(COSTE_APR) AS avg_cost,
    AVG(ESTANCIA_DIAS) AS avg_los
FROM INGRESO
GROUP BY NIVEL_SEVERIDAD_APR
```

**Visualization**: Three-panel bar chart
- Panel 1: Patient count by severity
- Panel 2: Average cost by severity
- Panel 3: Average length of stay by severity

**Clinical Insight**: Demonstrates relationship between severity and resource utilization

#### **2. Risk Stratification**
```sql
-- Groups patients by APR mortality risk (1-4)
SELECT 
    RIESGO_MORTALIDAD_APR,
    COUNT(*) AS patient_count,
    AVG(COSTE_APR) AS avg_cost,
    AVG(NIVEL_SEVERIDAD_APR) AS avg_severity
FROM INGRESO
GROUP BY RIESGO_MORTALIDAD_APR
```

**Visualization**: Grouped bar + line chart
- Bars: Patient count per risk level
- Line: Average cost trend

**Clinical Value**: Identifies high-risk populations for targeted interventions

#### **3. Diagnosis Correlations**
```sql
-- Finds diagnoses that frequently occur together
WITH DiagnosisPairs AS (
    SELECT DIAGNOSTICO_PRINCIPAL, DIAGNOSTICO_2
    FROM DIAGNOSTICOS_INGRESO
    UNION ALL
    SELECT DIAGNOSTICO_PRINCIPAL, DIAGNOSTICO_3
    ...
)
SELECT diag1, diag2, COUNT(*) AS co_occurrence
FROM DiagnosisPairs
GROUP BY diag1, diag2
HAVING COUNT(*) >= 10
ORDER BY COUNT(*) DESC
```

**Visualization**: Horizontal bar chart (top 20 pairs)

**Research Application**: 
- Discover comorbidity patterns
- Inform treatment protocols
- Support diagnosis prediction models

#### **4. Length of Stay Distribution**
```sql
-- Statistical analysis of hospital stay duration
SELECT 
    AVG(ESTANCIA_DIAS) AS mean_los,
    MEDIAN(ESTANCIA_DIAS) AS median_los,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ESTANCIA_DIAS) AS p25,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ESTANCIA_DIAS) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY ESTANCIA_DIAS) AS p90,
    STDDEV(ESTANCIA_DIAS) AS std_dev
FROM INGRESO
```

**Visualization**: Box plot with percentiles

**Statistical Metrics Displayed**:
- Mean, Median, Standard Deviation
- 25th, 75th, 90th percentiles
- Min/Max values

### Filters
- **Date Range**
- **Minimum Co-occurrence**: Threshold for diagnosis pairs (5-50)
- **Service Filter**: Focus on specific hospital services

### Use Cases
1. **Clinical research** on diagnosis associations
2. **Risk assessment** for patient triage
3. **Resource allocation** based on severity distribution
4. **Benchmarking** length of stay against standards

---

## 🔮 Module 3: Predictive Analytics

**Route**: `/predictive-analytics`

### Purpose
Identify temporal trends, forecast future patterns, and detect seasonal variations in hospital activity and outcomes.

### Key Features

#### **1. Multi-Metric Temporal Trends**
```sql
-- Monthly aggregation of key metrics
SELECT 
    TO_CHAR(FECHA_DE_INGRESO, 'YYYY-MM') AS month,
    COUNT(*) AS admissions,
    AVG(ESTANCIA_DIAS) AS avg_los,
    AVG(COSTE_APR) AS avg_cost,
    AVG(NIVEL_SEVERIDAD_APR) AS avg_severity
FROM INGRESO
GROUP BY TO_CHAR(FECHA_DE_INGRESO, 'YYYY-MM')
ORDER BY month
```

**Visualization**: 2x2 grid of line charts
- Top-left: Admissions trend
- Top-right: Cost trend  
- Bottom-left: Length of stay trend
- Bottom-right: Severity trend

**Analytical Value**: Spot seasonal patterns and long-term trends

#### **2. Admissions Forecasting**
Uses **linear regression** (scipy.stats) to:
- Calculate trend line from historical data
- Project future admission volumes
- Quantify trend strength (R² value)

**Visualization**: Actual data + trend line overlay

```python
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
trend_line = slope * x + intercept
```

#### **3. Cost vs Severity Correlation**
**Visualization**: Scatter plot
- X-axis: Severity level
- Y-axis: Average cost
- Bubble size: Patient count
- Color: Average length of stay

**Business Insight**: Quantifies financial impact of severity levels

#### **4. Activity Heatmap**
**Visualization**: Year x Month heatmap
- Rows: Years
- Columns: Months (Jan-Dec)
- Color intensity: Admission volume

**Pattern Detection**: Identifies:
- Seasonal peaks/troughs
- Year-over-year growth
- Holiday effects

#### **5. Metric Variability Analysis**
**Visualization**: Box plot
- Shows distribution of selected metric over time
- Highlights outliers
- Demonstrates consistency/volatility

#### **6. Statistical Summary Table**
Displays for all metrics:
- Mean
- Standard Deviation
- Minimum
- Maximum

### Filters
- **Date Range**
- **Aggregation Level**: Monthly vs Quarterly
- **Primary Metric**: Select focus metric for detailed analysis

### Advanced Features
- **Automated Insights**: AI-generated observations (e.g., "Admissions increasing by 15%")
- **Export Capability**: Download data for external analysis (future)

### Use Cases
1. **Capacity planning** based on admission forecasts
2. **Budget forecasting** using cost trends
3. **Staffing optimization** around seasonal patterns
4. **Performance monitoring** against historical benchmarks

---

## 🔧 Technical Implementation

### Database Queries

#### **Performance Optimizations**
1. **Window Functions**: Used for complex calculations without self-joins
   ```sql
   LEAD(FECHA_DE_INGRESO) OVER (PARTITION BY ID_PACIENTE ORDER BY FECHA_DE_INGRESO)
   ```

2. **CTEs (Common Table Expressions)**: Improve readability and performance
   ```sql
   WITH PatientAdmissions AS (...), ReadmissionCases AS (...)
   SELECT * FROM ReadmissionCases
   ```

3. **Parameterized Queries**: Security + query plan caching
   ```python
   params = {'date_start': date_start, 'date_end': date_end}
   df = pd.read_sql(sql, con=conn, params=params)
   ```

4. **Result Limiting**: Prevent memory overflow
   ```sql
   FETCH FIRST 100 ROWS ONLY
   ```

### Frontend Architecture

#### **Callback Pattern**
```python
@callback(
    Output("chart-id", "figure"),
    Input("data-store", "data")
)
def update_chart(data):
    # Process data
    # Create Plotly figure
    # Return figure
```

#### **Data Flow**
```
User Interaction → Filter Callback → Database Query → Data Store → Chart Callbacks → UI Update
```

#### **State Management**
- `dcc.Store`: Client-side data caching (reduces DB calls)
- Separate stores per page to avoid conflicts

### Error Handling
```python
try:
    result = query_database()
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    return default_empty_figure()
```

---

## 📊 Data Schema Utilization

### Tables Used

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| **PACIENTE** | Demographics | ID_PACIENTE, SEXO, COMUNIDAD_AUTONOMA, FECHA_DE_NACIMIENTO |
| **INGRESO** | Admissions | ID_INGRESO, FECHA_DE_INGRESO, ESTANCIA_DIAS, COSTE_APR, NIVEL_SEVERIDAD_APR, RIESGO_MORTALIDAD_APR |
| **DIAGNOSTICOS_INGRESO** | Diagnoses | ID_INGRESO, DIAGNOSTICO_PRINCIPAL, DIAGNOSTICO_2..20 |
| **PROCEDIMIENTOS_INGRESO** | Procedures | ID_INGRESO, PROCEDIMIENTO_1..20 |

### Join Patterns
```sql
-- Most common: Patient + Admission
FROM PACIENTE p
JOIN INGRESO i ON p.ID_PACIENTE = i.ID_PACIENTE

-- With diagnoses:
JOIN DIAGNOSTICOS_INGRESO d ON i.ID_INGRESO = d.ID_INGRESO

-- With procedures:
JOIN PROCEDIMIENTOS_INGRESO pr ON i.ID_INGRESO = pr.ID_INGRESO
```

---

## 🎯 Best Practices Followed

### **1. Code Organization**
✅ DRY (Don't Repeat Yourself) - Reusable components  
✅ Single Responsibility - Each function does one thing  
✅ Clear naming conventions  
✅ Comprehensive logging  

### **2. Security**
✅ Parameterized queries (no SQL injection)  
✅ Input validation  
✅ Error handling without exposing internals  
✅ Wallet-based DB authentication  

### **3. Performance**
✅ Connection pooling  
✅ Client-side caching  
✅ Lazy loading  
✅ Efficient queries (avoid N+1)  

### **4. Maintainability**
✅ Modular architecture  
✅ Comprehensive documentation  
✅ Consistent code style  
✅ Version control ready  

### **5. User Experience**
✅ Responsive design  
✅ Loading states  
✅ Error messages  
✅ Accessible UI  

---

## 🚀 Future Enhancements

### Potential Additions
1. **Machine Learning Integration**
   - Readmission risk prediction models
   - Length of stay forecasting
   - Diagnosis recommendation

2. **Advanced Visualizations**
   - Network graphs for patient flow
   - Sankey diagrams for care pathways
   - 3D scatter plots for multi-variate analysis

3. **Export Functionality**
   - PDF report generation
   - CSV/Excel data export
   - Custom date range exports

4. **Real-time Alerts**
   - Anomaly detection
   - Threshold notifications
   - Automated email reports

5. **Comparative Analysis**
   - Benchmark against national averages
   - Multi-facility comparison
   - Historical period comparison

---

## 📖 Usage Guide

### For Clinicians
1. **Cohort Analysis**: Identify patients needing follow-up care
2. **Clinical Insights**: Understand comorbidity patterns in your service
3. **Predictive Analytics**: Plan for seasonal admission spikes

### For Administrators
1. **Cohort Analysis**: Estimate costs for high-utilization patients
2. **Clinical Insights**: Allocate resources based on severity distribution
3. **Predictive Analytics**: Forecast budget and staffing needs

### For Researchers
1. **Cohort Analysis**: Study readmission patterns
2. **Clinical Insights**: Explore diagnosis correlations
3. **Predictive Analytics**: Analyze temporal trends in mental health

---

## 🔍 Troubleshooting

### Common Issues

**No data showing**
- Check date range filters
- Verify database connection
- Check browser console for errors

**Slow performance**
- Reduce date range
- Increase aggregation level (quarterly vs monthly)
- Clear browser cache

**Charts not updating**
- Click "Actualizar" button
- Refresh page
- Check filter values are valid

---

## 📚 Technical Stack Summary

- **Backend**: Python 3.10, Dash 3.2.0, Pandas 2.3.3
- **Database**: Oracle with connection pooling
- **Visualization**: Plotly 6.3.1
- **Statistical**: SciPy 1.11.0, NumPy 1.26.0
- **Frontend**: Bootstrap 5, Custom CSS
- **Server**: Gunicorn, Systemd

---

## 👥 Support

For questions or issues:
1. Check this documentation
2. Review `ARCHITECTURE_GUIDE.md`
3. Check application logs: `/var/log/malackathon/`
4. Contact development team

---

**Version**: 1.0  
**Last Updated**: October 16, 2025  
**Author**: Malackathon Development Team
