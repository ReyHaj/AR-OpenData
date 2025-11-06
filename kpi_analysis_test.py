# --------------------------------------------
# 📘 KPI Analysis – Accounts Receivable Analytics
# --------------------------------------------

import pandas as pd
from pathlib import Path

# 🧩 مرحله ۱: خواندن داده تمیز (از گام ۳)
file = Path("data/processed/AR_Clean_Features.xlsx")
df = pd.read_excel(file)

print("✅ Data loaded successfully!")
print("Rows & Columns:", df.shape)
print("=" * 60)

# 🧩 مرحله ۲: محاسبه KPIها

# 1️⃣ میانگین تأخیر پرداخت (Average Delay)
avg_delay = df["DaysLate"].mean()

# 2️⃣ درصد پرداخت به‌موقع (On-Time %)
on_time_percent = (df["OnTime"].sum() / len(df)) * 100

# 3️⃣ مجموع مبلغ‌های باز (Outstanding Total)
outstanding_total = df["Outstanding"].sum()

# 4️⃣ DSO (Days Sales Outstanding)
# میانگین زمان دریافت پول از تاریخ صدور فاکتور تا تاریخ پرداخت
df["DaysToPay"] = (df["ReceivedDate"] - df["InvoiceDate"]).dt.days
dso = df["DaysToPay"].mean()

# 🧩 مرحله ۳: تحلیل مشتریان
# ۵ مشتری با بیشترین تأخیر
top_late_customers = (
    df.groupby("Customer")["DaysLate"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

# 🧩 مرحله ۴: نمایش نتایج
print("📊 KPI Summary")
print("=" * 60)
print(f"🕒 Average Payment Delay (DaysLate): {avg_delay:.2f} days")
print(f"✅ On-Time Payment Rate: {on_time_percent:.1f}%")
print(f"💰 Total Outstanding Amount: {outstanding_total:,.2f}")
print(f"📆 DSO (Days Sales Outstanding): {dso:.2f} days")
print("=" * 60)
print("🚨 Top 5 Late Customers:")
print(top_late_customers)

# 🧩 مرحله ۵: ذخیره خلاصه KPIها در فایل Excel
kpi_data = {
    "Average Delay (Days)": [avg_delay],
    "On-Time %": [on_time_percent],
    "Total Outstanding": [outstanding_total],
    "DSO (Days Sales Outstanding)": [dso],
}

kpi_df = pd.DataFrame(kpi_data)
output_path = Path("data/processed/AR_KPI_Summary.xlsx")
kpi_df.to_excel(output_path, index=False)

print(f"\n✅ KPI summary saved to: {output_path}")
