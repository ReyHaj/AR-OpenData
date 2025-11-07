# 📘 Accounts Receivable Analytics – Open Data Project

### 🔹 Overview
Questo progetto analizza dati dei conti da incassare (Accounts Receivable) utilizzando **Python (Pandas)** e li integra in **Microsoft Dynamics 365** come dashboard interattivo per il monitoraggio dei KPI finanziari.



### ⚙️ Tools & Technologies
- **Python 3.13**
- **Libraries:** Pandas, NumPy, Plotly, Streamlit
- **ERP / BI Integration:** Microsoft Dynamics 365, Power BI
- **Data Source:** Open dataset (Kaggle / Excel)



### 🧱 Project Structure
FBA_365D.PYTHON_AR/
│
├── data/
│ ├── raw/ # Dati originali (Excel)
│ ├── processed/ # Dati puliti e con KPI
│
├── data_cleaning_test.py # Data cleaning script
├── feature_engineering_test.py # Feature engineering
├── kpi_analysis_test.py # KPI calculation
├── dashboard_app.py # Streamlit dashboard
├── README.md # Documentation




### 📊 Project Steps
1. **Data Loading:** Importazione dei dati Excel in Pandas.  
2. **Data Cleaning:** Rimozione valori mancanti, duplicati e incoerenze.  
3. **Feature Engineering:** Creazione colonne `DaysLate`, `OnTime`, `Outstanding`.  
4. **KPI Calculation:** Calcolo DSO, % pagamenti puntuali, importi aperti.  
5. **Dashboard:** Visualizzazione interattiva con Streamlit e Power BI.  



### 📈 Main KPIs
| KPI | Descrizione |
|------|-------------|
| **DSO (Days Sales Outstanding)** | Media giorni per ricevere il pagamento |
| **On-Time Payment %** | Percentuale di fatture pagate puntualmente |
| **Average Delay** | Ritardo medio dei pagamenti |
| **Outstanding Total** | Totale importi ancora da incassare |



### 🚀 How to Run Locally
1. Installa i pacchetti:
   ```bash
   pip install pandas numpy plotly streamlit openpyxl
2. Esegui gli script in ordine:
python data_cleaning_test.py
python feature_engineering_test.py
python kpi_analysis_test.py
3. Avvia la dashboard:
streamlit run dashboard_app.py
💾 Output

data/processed/AR_Clean_Features.xlsx → Dati puliti
data/processed/AR_KPI_Summary.xlsx → KPI calcolati
Dashboard: http://localhost:8501

## 🔗 Live Demo (Streamlit App)
https://ar-opendata-boe7z5qwyvkty3sxloufmp.streamlit.app/


## 📊 Dashboard Preview

### Invoice Status Distribution  
![invoice status](image/invoice%20status%20distribution.png)

### Top 10 Customers by Average Delay  
![top 10 customers](image/top%2010%20costumers%20by%20average%20delay.png)

### Top 10 Customers by Average Delay  
![account Receivable](image/Accounts%20Receivable%20Analytics%20Dashboard.png)

👩‍💻 Author

[REYHANEH HAJILI]
Data Engineer & Data Analyst – Python & Microsoft Dynamics 365 Integration