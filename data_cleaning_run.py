# --------------------------------------------
# 🧼 Real Data Cleaning – Accounts Receivable
# --------------------------------------------
import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")
PROC_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- 1) Read ----------
files = list(RAW_DIR.glob("*.xlsx"))
if not files:
    raise FileNotFoundError("❌ هیچ فایل اکسل در data/raw پیدا نشد.")
src = files[0]
df0 = pd.read_excel(src)
df = df0.copy()

log = []  # برای ثبت اقدامات پاکسازی

def add_log(msg, n=None):
    if n is None:
        log.append(msg)
    else:
        log.append(f"{msg}: {n}")

# ---------- 2) Standardize columns ----------
# Trim نام ستون‌ها و یکنواخت‌سازی
df.columns = [c.strip() for c in df.columns]
# نقشه نام‌های متداول به استاندارد
rename_map = {
    "Invoice No": "InvoiceNumber",
    "InvoiceNum": "InvoiceNumber",
    "Invoice ID": "InvoiceID",
    "InvoiceDate":"InvoiceDate",
    "Invoice Date":"InvoiceDate",
    "DueDate":"DueDate",
    "Due Date":"DueDate",
    "ReceivedDate":"ReceivedDate",
    "PaymentDate":"ReceivedDate",
    "Customer":"Customer",
    "Client":"Customer",
    "Amount":"Amount",
    "Total":"Amount",
    "Status":"Status"
}
for k,v in list(rename_map.items()):
    if k in df.columns and v not in df.columns:
        df.rename(columns={k:v}, inplace=True)

# ستون‌های کلیدی حداقلی
needed = ["Customer","InvoiceDate","DueDate","Amount"]
missing_need = [c for c in needed if c not in df.columns]
if missing_need:
    add_log(f"⚠️ ستون‌های ضروری موجود نیستند: {missing_need}")
# ستون‌هایی که اگر باشند استفاده می‌کنیم
opt_cols = ["InvoiceID","InvoiceNumber","ReceivedDate","Status"]
for c in opt_cols:
    if c not in df.columns:
        df[c] = np.nan  # اضافه به صورت خالی تا کد نشکند

# ---------- 3) Strip/normalize strings ----------
str_cols = ["Customer","Status","InvoiceNumber","InvoiceID"]
for c in str_cols:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip()

# ---------- 4) Coerce data types ----------
date_cols = ["InvoiceDate","DueDate","ReceivedDate"]
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce")

# مبلغ به عدد
if "Amount" in df.columns:
    before_nonnum = df["Amount"].isna().sum()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    after_nonnum = df["Amount"].isna().sum()
    add_log("🔁 تبدیل Amount به عدد (ناعددی→NaN)",
            f"قبل {before_nonnum} / بعد {after_nonnum}")

# ---------- 5) Basic validity ----------
# حذف ردیف‌های بدون InvoiceDate یا DueDate یا Amount
n0 = len(df)
df = df[~df["InvoiceDate"].isna() & ~df["DueDate"].isna() & ~df["Amount"].isna()]
add_log("🧹 حذف ردیف‌های فاقد تاریخ/مبلغ", n0 - len(df))

# DueDate نباید قبل از InvoiceDate باشد
mask_due_before = df["DueDate"] < df["InvoiceDate"]
fix_due = mask_due_before.sum()
if fix_due > 0:
    # یا حذف، یا تنظیم: ما حذف می‌کنیم تا KPI مخدوش نشود
    rejected_due = df[mask_due_before].copy()
    rejected_due.to_excel(PROC_DIR / "_rejected_due_before_invoice.xlsx", index=False)
    df = df[~mask_due_before]
    add_log("🚫 حذف ردیف‌هایی که DueDate < InvoiceDate", fix_due)

# Amount منفی → رد (در AR بی‌معناست، مگر Credit Memo؛ اینجا حذف)
mask_neg = df["Amount"] < 0
neg_n = mask_neg.sum()
if neg_n > 0:
    rejected_neg = df[mask_neg].copy()
    rejected_neg.to_excel(PROC_DIR / "_rejected_negative_amount.xlsx", index=False)
    df = df[~mask_neg]
    add_log("🚫 حذف ردیف‌های Amount منفی", neg_n)

# ---------- 6) Duplicates ----------
# کلید تکراری: ترجیحاً InvoiceID، اگر نبود InvoiceNumber، وگرنه ترکیبی
if df["InvoiceID"].notna().any():
    key_cols = ["InvoiceID"]
elif df["InvoiceNumber"].notna().any():
    key_cols = ["Customer","InvoiceNumber","InvoiceDate","Amount"]
else:
    key_cols = ["Customer","InvoiceDate","Amount"]
dup_n = df.duplicated(subset=key_cols, keep="first").sum()
if dup_n > 0:
    rejected_dups = df[df.duplicated(subset=key_cols, keep="first")].copy()
    rejected_dups.to_excel(PROC_DIR / "_rejected_duplicates.xlsx", index=False)
    df = df.drop_duplicates(subset=key_cols, keep="first")
    add_log(f"🔁 حذف رکوردهای تکراری بر اساس {key_cols}", dup_n)

# ---------- 7) Status normalization (اختیاری ولی مفید) ----------
status_map = {
    "open":"Open",
    "partial":"Partial",
    "partially paid":"Partial",
    "received":"Received",
    "paid":"Received",
    "closed":"Received"
}
if "Status" in df.columns:
    df["Status_norm"] = (
        df["Status"].astype(str).str.lower().map(status_map).fillna(df["Status"])
    )

# ---------- 8) Save cleaned & report ----------
clean_path = PROC_DIR / "AR_Clean.xlsx"
df.to_excel(clean_path, index=False)

summary = {
    "rows_raw": len(df0),
    "rows_clean": len(df),
    "removed_missing_core": int(n0 - len(df)),   # تقریبی برای سادگی گزارش
    "removed_due_before_invoice": int(fix_due),
    "removed_negative_amount": int(neg_n),
    "removed_duplicates": int(dup_n),
}
pd.DataFrame({"action_or_note": log}).to_csv(REPORTS_DIR / "cleaning_log.csv", index=False)
pd.DataFrame([summary]).to_csv(REPORTS_DIR / "cleaning_summary.csv", index=False)

print("✅ Cleaning done.")
print("➡️ Clean file:", clean_path)
print("📝 Log:", REPORTS_DIR / "cleaning_log.csv")
print("🧾 Summary:", REPORTS_DIR / "cleaning_summary.csv")
