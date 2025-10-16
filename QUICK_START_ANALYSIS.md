# 🚀 Quick Start Guide - Advanced Analysis Modules

## Navigation

Your dashboard now has **4 main sections**:

```
🏠 Home (/)
   └─ Landing page with feature overview

📊 Dashboard (/dashboard)
   └─ Overview with KPIs and basic charts

🔬 Advanced Analysis (NEW!)
   ├─ 👥 Cohort Analysis (/cohort-analysis)
   ├─ 🏥 Clinical Insights (/clinical-insights)
   └─ 📈 Predictive Analytics (/predictive-analytics)
```

---

## 👥 Cohort Analysis - Quick Reference

**What**: Track patient journeys and readmission patterns

**Key Metrics**:
- ⏱️ Readmission Rate (%)
- 📅 Average Days to Readmission
- 👤 Total Cohort Patients
- 📋 Total Admissions

**Main Charts**:
1. **Patient Journey** - Scatter plot showing admission count vs total cost
2. **Readmission Distribution** - Pie chart: with vs without readmission
3. **Comorbidity** - Bar chart of diagnosis complexity
4. **Cost Analysis** - Dual chart: cost accumulation vs patient count

**Filters**:
- Date Range
- Readmission Threshold: 7/14/30/60/90 days
- Minimum Admissions: 2-10+

**Best Used For**:
- Identifying high-risk patients
- Resource planning for frequent admitters
- Studying comorbidity patterns

---

## 🏥 Clinical Insights - Quick Reference

**What**: Deep dive into clinical patterns and outcomes

**Main Charts**:
1. **Severity Analysis** - 3-panel view (patients, costs, LOS by severity level)
2. **Risk Stratification** - Patient distribution by mortality risk
3. **Diagnosis Correlations** - Top 20 diagnosis pairs that occur together
4. **Length of Stay** - Statistical distribution with percentiles

**Key Statistics**:
- Mean, Median, Std Dev
- 25th, 75th, 90th Percentiles
- Total Patients
- High-Risk Patient Count

**Filters**:
- Date Range
- Minimum Co-occurrence (5-50)
- Service Filter

**Best Used For**:
- Understanding severity-cost relationships
- Identifying high-risk populations
- Researching diagnosis associations
- Benchmarking length of stay

---

## 📈 Predictive Analytics - Quick Reference

**What**: Temporal trends and pattern forecasting

**Main Charts**:
1. **Multi-Metric Trends** - 4-panel time series (admissions, cost, LOS, severity)
2. **Cost vs Severity** - Scatter plot with bubble sizing
3. **Admissions Forecast** - Actual data + trend line projection
4. **Activity Heatmap** - Year x Month intensity map
5. **Variability Box Plot** - Distribution of selected metric
6. **Statistical Summary** - Descriptive statistics table

**Features**:
- 🤖 **Auto Insights**: AI-generated trend observations
- 📊 **Aggregation**: Choose Monthly or Quarterly
- 🎯 **Metric Focus**: Select primary metric for analysis

**Filters**:
- Date Range
- Aggregation Level (Monthly/Quarterly)
- Primary Metric

**Best Used For**:
- Capacity planning
- Budget forecasting
- Detecting seasonal patterns
- Performance monitoring

---

## 🎓 Usage Tips

### Getting Started
1. **Choose your date range** - Start broad, then narrow down
2. **Apply filters** - Click "Actualizar" or "Refresh" button
3. **Interact with charts** - Hover for details, zoom, pan
4. **Export insights** - Take screenshots or notes

### Best Practices
✅ **Compare periods** - Use consistent date ranges for comparisons  
✅ **Check sample size** - Larger date ranges = more reliable trends  
✅ **Combine modules** - Use cohort + clinical for comprehensive view  
✅ **Reset filters** - Use reset button if results seem wrong  

### Performance Tips
⚡ **Faster loading**: Reduce date range or increase aggregation level  
⚡ **Better accuracy**: Use longer date ranges (6+ months)  
⚡ **Clearer charts**: Adjust minimum thresholds to reduce noise  

---

## 📱 Mobile Access

All analysis pages are **fully responsive**:
- Filters stack vertically on mobile
- Charts auto-resize
- Navigation buttons adapt
- Zoom disabled for better scrolling

---

## 🔍 Interpreting Results

### Cohort Analysis
- **High readmission rate** (>20%): Consider intervention programs
- **Short readmission window** (<14 days): Post-discharge support needed
- **High comorbidity**: Integrated care pathways recommended

### Clinical Insights
- **Severity Level 3-4**: Resource-intensive cases
- **High risk patients**: Priority for case management
- **Common diagnosis pairs**: Opportunity for treatment protocols

### Predictive Analytics
- **Upward trends**: Plan for capacity expansion
- **Seasonal peaks**: Staff accordingly
- **High variability**: Investigate causes of fluctuation

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Charts not loading | Click refresh button, check date range |
| "No data available" | Expand date range, reset filters |
| Slow performance | Reduce date range, try quarterly aggregation |
| Unexpected results | Reset filters, verify filter values |

---

## 📊 Data Sources

All analysis uses **Oracle database** with tables:
- `PACIENTE` - Patient demographics
- `INGRESO` - Hospital admissions
- `DIAGNOSTICOS_INGRESO` - Diagnosis records
- `PROCEDIMIENTOS_INGRESO` - Procedure records

**Data Quality**: Real mental health data from Spanish hospitals

---

## 🎯 Common Workflows

### **Workflow 1: Readmission Analysis**
1. Go to Cohort Analysis
2. Set 30-day readmission threshold
3. Filter for recent 6 months
4. Identify top readmitted patients
5. Export patient IDs for intervention

### **Workflow 2: Resource Planning**
1. Go to Predictive Analytics
2. View admissions forecast
3. Check seasonal heatmap
4. Go to Clinical Insights
5. Review severity distribution
6. Calculate staffing needs

### **Workflow 3: Clinical Research**
1. Go to Clinical Insights
2. Set minimum co-occurrence to 10
3. Review diagnosis correlations
4. Go to Cohort Analysis
5. Check comorbidity distribution
6. Cross-reference with literature

---

## 💡 Pro Tips

🎯 **Combine filters** for precise analysis  
📊 **Export data** by taking screenshots  
🔄 **Compare periods** using consistent date ranges  
📈 **Track trends** over time to spot patterns  
🤝 **Share insights** with team using specific URLs  

---

## 📚 Learn More

- Full Technical Documentation: `ADVANCED_ANALYSIS_GUIDE.md`
- Architecture Overview: `ARCHITECTURE_GUIDE.md`
- Database Schema: `SCHEMA_REFERENCE.md`

---

**Questions?** Check the logs or contact support team.

**Happy Analyzing! 🎉**
