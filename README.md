# AR Analytics – Open Data Project

Open, reproducible Accounts Receivable (AR) analytics using a public sample dataset.

## Data
- **Source:** Excelx – *Free Finance & Accounting Sample Data* (Accounts Receivable Dataset)
- **URL:** https://excelx.com/practice-data/finance-accounting/
- **Notes:** Data is fully synthetic/dummy per the publisher. Review the site's Terms & Conditions before redistribution.

**Included columns (per source page):**
`ARID`, `Customer`, `InvoiceDate`, `DueDate`, `Amount`, `Currency`, `Status`, `ReceivedDate`, `Terms`.

## Project Structure
```
AR-OpenData/
├─ data/
│  ├─ raw/              # original files from source (read-only)
│  ├─ interim/          # partially cleaned data
│  └─ processed/        # final, clean data for modeling & dashboard
├─ notebooks/
│  ├─ 01_eda.ipynb
│  ├─ 02_cleaning.ipynb
│  ├─ 03_feature_engineering.ipynb
│  └─ 04_modeling.ipynb
├─ src/
│  ├─ data_prep.py
│  ├─ features.py
│  ├─ metrics.py
│  └─ visualization.py
├─ reports/
│  ├─ data_dictionary.md
│  ├─ data_quality_report.md
│  └─ final_report.pdf
├─ dashboards/
│  └─ streamlit_app/
│     └─ app.py
├─ environment.yml
└─ .gitignore
```

## How to Run
1. Create environment  
   ```bash
   conda env create -f environment.yml && conda activate ar
   ```
2. Place the downloaded **Accounts Receivable (.xlsx)** file into `data/raw/`.
3. Launch notebooks in order (EDA → Cleaning → Features → Modeling).
4. Run the dashboard:  
   ```bash
   streamlit run dashboards/streamlit_app/app.py
   ```

## KPIs & Ideas
- DSO, ADD, CEI, On-time %, Aging buckets (0-30/31-60/61-90/>90)
- Top delinquent customers, monthly DSO trend
- Baseline model: predict `OnTime` or `DaysLate`

*Generated on 2025-11-03.*
