# --------------------------------------------
# 📘 Data Cleaning - Accounts Receivable Project
# --------------------------------------------

import pandas as pd
from pathlib import Path

# 🧩 مرحله ۱: خواندن داده از فایل اکسل
p = Path("data/raw")
file = list(p.glob("*.xlsx"))[0]
df = pd.read_excel(file)

print("✅ Data loaded successfully!")
print("Rows & Columns:", df.shape)
print("=" * 50)

# 🧩 مرحله ۲: بررسی مقادیر خالی (Missing Values)
print("\n🔍 Missing Values:")
print(df.isna().sum())

# 🧠 توضیح:
# isna() بررسی می‌کند کدام سلول‌ها خالی‌اند.
# sum() تعداد سلول‌های خالی در هر ستون را نشان می‌دهد.

print("=" * 50)

# 🧩 مرحله ۳: بررسی رکوردهای تکراری (Duplicates)
duplicates = df.duplicated().sum()
print(f"🔁 Duplicate Rows Found: {duplicates}")

# اگر خواستی رکوردهای تکراری را ببینی:
# print(df[df.duplicated()])

print("=" * 50)

# 🧩 مرحله ۴: بررسی نوع داده‌ها (Data Types)
print("\n🔍 Column Data Types:")
print(df.dtypes)

# 🧠 اگر تاریخ‌ها به صورت Text بودند، در مرحله بعد تبدیل می‌کنیم.

print("=" * 50)

# 🧩 مرحله ۵: بررسی ناسازگاری‌ها (Inconsistent Data)
# مثلا اگر Status = "Received" باشد ولی ReceivedDate خالی باشد → ناسازگار
mask_inconsistent = (df["Status"].str.lower() == "received") & (df["ReceivedDate"].isna())
print(f"⚠️ Inconsistent Records (Received but no date): {mask_inconsistent.sum()}")

# 🧠 این خط تشخیص می‌دهد چند ردیف از نوع ناسازگار هستند.

print("=" * 50)

# 🧩 مرحله ۶: بررسی مقادیر نامعتبر (Invalid)
# مثلا اگر Amount منفی باشد
invalid_amounts = df[df["Amount"] < 0]
print(f"🚫 Invalid Amount Rows: {len(invalid_amounts)}")

# 🧠 چون مبلغ منفی در حساب‌های دریافتنی معنی ندارد.

print("=" * 50)

# 🧩 مرحله ۷: جمع‌بندی خلاصه کیفیت داده
print("\n📊 Data Quality Summary:")
print({
    "missing_values": df.isna().sum().sum(),
    "duplicates": duplicates,
    "inconsistent": mask_inconsistent.sum(),
    "invalid_amounts": len(invalid_amounts)
})
