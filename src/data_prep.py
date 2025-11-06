from pathlib import Path
import pandas as pd

def load_ar_xlsx(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    return df

def standardize_dates(df: pd.DataFrame, cols=("InvoiceDate","DueDate","ReceivedDate")) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def save_parquet(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
