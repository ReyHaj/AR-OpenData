# --------------------------------------------
# 📘 Feature Engineering - Accounts Receivable
# --------------------------------------------

import pandas as pd
from pathlib import Path

# 🧩 مرحله ۱: خواندن داده
p = Path("data/raw")
file = list(p.glob("*.xlsx"))[0]
df = pd.read_excel(file)

print("✅ Data loaded successfully!")
print("Rows & Columns:", df.shape)
print("=" * 50)

# 🧩 مرحله ۲: تبدیل ستون‌های تاریخ به فرمت datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["DueDate"] = pd.to_datetime(df["DueDate"])
df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")

print("📅 تاریخ‌ها به فرمت datetime تبدیل شدند.")
print("=" * 50)

# 🧩 مرحله ۳: محاسبه DaysLate (تعداد روزهای تأخیر)
# اگر ReceivedDate خالی باشد، یعنی هنوز پرداخت نشده → از امروز تا DueDate حساب می‌کنیم
today = pd.Timestamp.today()

df["DaysLate"] = (
    df.apply(
        lambda x: (x["ReceivedDate"] - x["DueDate"]).days
        if pd.notna(x["ReceivedDate"])
        else (today - x["DueDate"]).days,
        axis=1,
    )
)

# اگر مقدار منفی شد (یعنی قبل از موعد پرداخت شده)، آن را صفر می‌کنیم
df.loc[df["DaysLate"] < 0, "DaysLate"] = 0

print("📆 ستون DaysLate ساخته شد.")
print("=" * 50)

# 🧩 مرحله ۴: ساخت ستون OnTime (پرداخت به موقع یا با تأخیر)
df["OnTime"] = df["DaysLate"] == 0

# True → پرداخت به‌موقع
# False → با تأخیر

print("⏱️ ستون OnTime اضافه شد.")
print("=" * 50)

# 🧩 مرحله ۵: ساخت ستون Outstanding (مبلغ باقی‌مانده)
# اگر Status = "Open" یا "Partial" باشد → هنوز مبلغی باقی مانده
df["Outstanding"] = df.apply(
    lambda x: x["Amount"]
    if x["Status"].lower() in ["open", "partial"]
    else 0,
    axis=1,
)

print("💰 ستون Outstanding ساخته شد.")
print("=" * 50)

# 🧩 مرحله ۶: ساخت ستون PaidStatus (توضیح خلاصه برای گزارش)
def paid_status(row):
    if row["Outstanding"] == 0:
        return "Paid"
    elif row["Status"].lower() == "partial":
        return "Partially Paid"
    else:
        return "Open"

df["PaidStatus"] = df.apply(paid_status, axis=1)

print("📋 ستون PaidStatus اضافه شد.")
print("=" * 50)

# 🧩 مرحله ۷: بررسی نتیجه
print("\n🔍 نمونه خروجی:")
print(df[["Customer", "DueDate", "ReceivedDate", "DaysLate", "OnTime", "Outstanding", "PaidStatus"]].head())

# 🧩 مرحله ۸: ذخیره‌ی داده‌ی آماده در پوشه‌ی processed
output_path = Path("data/processed/AR_Clean_Features.xlsx")
df.to_excel(output_path, index=False)

print(f"\n✅ فایل تمیز و تحلیلی ذخیره شد در: {output_path}")
