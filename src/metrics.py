import numpy as np
import pandas as pd

def dso(ar_balance: float, credit_sales_per_day: float) -> float:
    if credit_sales_per_day == 0:
        return np.nan
    return ar_balance / credit_sales_per_day

def average_days_delinquent(df: pd.DataFrame, dayslate_col="DaysLate") -> float:
    if dayslate_col not in df:
        return np.nan
    return float(pd.to_numeric(df[dayslate_col], errors="coerce").dropna().mean())
