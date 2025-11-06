# --------------------------------------------
# 📊 Dashboard - Accounts Receivable Analytics
# --------------------------------------------

import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# 🧩 مرحله ۱: خواندن داده‌ها
kpi_file = Path("data/processed/AR_KPI_Summary.xlsx")
data_file = Path("data/processed/AR_Clean_Features.xlsx")

df_kpi = pd.read_excel(kpi_file)
df = pd.read_excel(data_file)

st.set_page_config(page_title="AR Analytics Dashboard", layout="wide")

st.title("📘 Accounts Receivable Analytics Dashboard")
st.markdown("**Data cleaned and analyzed with Python (Pandas)**")

# 🧩 مرحله ۲: نمایش KPI Summary در بالا
col1, col2, col3, col4 = st.columns(4)

col1.metric("🕒 Avg Delay (Days)", f"{df_kpi['Average Delay (Days)'][0]:.2f}")
col2.metric("✅ On-Time %", f"{df_kpi['On-Time %'][0]:.1f}%")
col3.metric("💰 Outstanding ($)", f"{df_kpi['Total Outstanding'][0]:,.0f}")
col4.metric("📆 DSO (Days)", f"{df_kpi['DSO (Days Sales Outstanding)'][0]:.1f}")

st.divider()

# 🧩 مرحله ۳: نمودار مشتریان با بیشترین تأخیر
top_customers = (
    df.groupby("Customer")["DaysLate"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_customers,
    x="Customer",
    y="DaysLate",
    color="DaysLate",
    title="🚨 Top 10 Customers by Average Delay (DaysLate)",
)
st.plotly_chart(fig1, use_container_width=True)

# 🧩 مرحله ۴: نمودار وضعیت فاکتورها (Open, Partial, Paid)
fig2 = px.pie(
    df,
    names="PaidStatus",
    title="💼 Invoice Status Distribution",
    color_discrete_sequence=px.colors.sequential.Blues,
)
st.plotly_chart(fig2, use_container_width=True)

# 🧩 مرحله ۵: جدول داده‌ها برای مرور دقیق
st.subheader("📋 Detailed Data (Sample)")
st.dataframe(df.head(20))
