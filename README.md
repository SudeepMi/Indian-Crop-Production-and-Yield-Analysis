# 🌾 Indian Crop Production and Yield Analysis (1997 - 2015)

> **An End-to-End Python Data Analytics, Statistical Analysis, Gujarat State Case Study, and Interactive Streamlit Application built on the Kaggle Indian Crop Production Dataset (246,091 records).**

---

## 📌 Executive Summary

Agriculture forms the cornerstone of the Indian economy. This project delivers a comprehensive, full-fledged data analytics suite to investigate national crop production dynamics, cultivated land area, and crop yield productivity ($Yield = \frac{Production}{Area}$) across **33 Indian States and Union Territories** over an 18-year period.

A primary objective of this project is a dedicated **Gujarat Case Study**, examining the state's commercial cash crop specialization (Groundnut, Cotton, Bajra, Wheat, Sugarcane) relative to overall Indian production trends.

---

## 📂 Repository Architecture

```text
d:/sudeep-projects/ostf-sudeep/
├── data/
│   ├── crop_production.csv          # Raw Kaggle Dataset (246,091 rows, 15.3 MB)
│   └── cleaned_crop_production.csv  # Preprocessed Dataset with Derived Yield Metrics
│
├── notebooks/
│   └── Indian_Crop_Production_Analysis.ipynb # Executable Jupyter Notebook
│
├── outputs/                         # 12 High-Resolution Analytical Charts (300 DPI)
│   ├── 01_production_vs_year.png
│   ├── 02_area_vs_year.png
│   ├── 03_top_10_crops.png
│   ├── 04_top_10_states.png
│   ├── 05_yield_by_crop.png
│   ├── 06_gujarat_production_trend.png
│   ├── 07_gujarat_top_crops.png
│   ├── 08_area_vs_production_scatter.png
│   ├── 09_crop_production_trends.png
│   ├── 10_state_crop_heatmap.png
│   ├── 11_yield_boxplot.png
│   └── 12_season_comparison.png
│
├── dashboard/
│   └── app.py                       # Interactive Streamlit Web Application
│
├── report/
│   └── Project_Report.pdf           # Programmatically Generated PDF Project Report
│
├── scripts/
│   ├── analyze_and_build.py         # Main Cleaning, Analysis & Image Generation Engine
│   ├── build_notebook.py            # Jupyter Notebook Builder
│   └── build_report.py              # ReportLab PDF Generator
│
├── app.md                           # Original Project Specification & Requirements
├── requirements.txt                 # Python Dependencies
└── README.md                        # Documentation & Guide
```

---

## 🚀 Key Features & Analytical Pipeline

### 1. Data Cleaning & Standardization
- **Schema Harmonization:** Standardized raw column headers (`State_Name`, `District_Name`, `Crop_Year`, `Season`, `Crop`, `Area`, `Production`) into lowercase snake_case.
- **Categorical Trimming:** Cleaned whitespace anomalies (e.g., `'Coconut '` $\rightarrow$ `'Coconut'`, `'Kharif '` $\rightarrow$ `'Kharif'`).
- **Missing Value Handling:** Investigated missing production values (1.5% missing) without forcing artificial zero imputations.
- **Derived Metrics:** Calculated crop yield in Tonnes per Hectare ($Yield = \frac{Production}{Area}$) and Kg per Hectare ($Yield_{kg/ha} = Yield \times 1000$).

### 2. Statistical Analysis & Hypothesis Testing
- **Pearson Correlation:** Evaluated relationship between cultivated area and crop production ($r = 0.34$), revealing area expansion as a baseline driver alongside yield intensity variations.
- **One-Way ANOVA:** Tested crop yield variance across seasons ($F\text{-stat} > 100, p < 0.001$), establishing statistically significant seasonal yield productivity differences.
- **Coefficient of Variation (CV):** Quantified yield volatility across staple and commercial crops.

### 3. Gujarat State Case Study
- **Dataset Coverage:** Analyzed 8,986 records across Gujarat's districts (Saurashtra, North, Central, and South Gujarat).
- **Key Findings:** Gujarat contributes significantly to national production of **Groundnut**, **Cotton (lint)**, **Bajra**, **Sugarcane**, and **Castor Seed**, demonstrating high productivity efficiency in rainfed and semi-arid agro-climatic zones.

---

## 📊 Analytical Chart Showcase (12 High-Resolution Visualizations)

| # | Visualization File | Description & Purpose |
|---|---|---|
| **1** | [01_production_vs_year.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/01_production_vs_year.png) | National annual production trend line chart |
| **2** | [02_area_vs_year.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/02_area_vs_year.png) | Total cultivated area trend over time |
| **3** | [03_top_10_crops.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/03_top_10_crops.png) | Top 10 crops by total production volume |
| **4** | [04_top_10_states.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/04_top_10_states.png) | Top 10 agricultural states by production volume |
| **5** | [05_yield_by_crop.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/05_yield_by_crop.png) | Average yield (Tonnes / Hectare) for major crops |
| **6** | [06_gujarat_production_trend.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/06_gujarat_production_trend.png) | Gujarat state annual production trajectory |
| **7** | [07_gujarat_top_crops.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/07_gujarat_top_crops.png) | Major crops in Gujarat by production volume |
| **8** | [08_area_vs_production_scatter.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/08_area_vs_production_scatter.png) | Cultivated area vs production scatter plot with regression |
| **9** | [09_crop_production_trends.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/09_crop_production_trends.png) | Time-series trajectories of top 5 major crops |
| **10** | [10_state_crop_heatmap.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/10_state_crop_heatmap.png) | State $\times$ Crop production intensity matrix heatmap |
| **11** | [11_yield_boxplot.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/11_yield_boxplot.png) | Yield distribution & variability boxplot across crops |
| **12** | [12_season_comparison.png](file:///d:/sudeep-projects/ostf-sudeep/outputs/12_season_comparison.png) | Seasonal breakdown: Production vs Cultivated Area |

---

## 🛠️ Installation & Execution Guide

### Prerequisites
- Python 3.10+
- Installed dependencies (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `streamlit`, `plotly`, `reportlab`)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Data Analytics & Chart Generation Engine
```bash
python scripts/analyze_and_build.py
```

### 3. Launch Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
*Access the dashboard in browser at:* `http://localhost:8501`

### 4. Build PDF Project Report
```bash
python scripts/build_report.py
```
*Output generated at:* `report/Project_Report.pdf`

### 5. Build Jupyter Notebook
```bash
python scripts/build_notebook.py
```
*Output generated at:* `notebooks/Indian_Crop_Production_Analysis.ipynb`

---

## 💡 Policy Recommendations & Strategic Takeaways

1. **Precision Micro-Irrigation:** Expand drip and sprinkler irrigation in rainfed commercial belts of Gujarat and Rajasthan for oilseeds (Groundnut, Sesame) and fiber crops (Cotton).
2. **Crop Yield Optimization:** Shift policy focus from purely expanding cultivated acreage towards augmenting per-hectare yield intensity through high-yielding variety (HYV) seeds and soil nutrient management.
3. **Cold Storage Infrastructure:** Reduce post-harvest loss in perishable horticultural crops (Potato, Onion) through cold chain network integration.

---
*Developed by Senior Data Analyst & Software Engineer.*
