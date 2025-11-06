import matplotlib.pyplot as plt
import pandas as pd

def aging_bar(df: pd.DataFrame, due_col="DueDate", recv_col="ReceivedDate", amount_col="Amount"):
    df = df.copy()
    for c in [due_col, recv_col]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    # compute days late
    if due_col in df.columns and recv_col in df.columns:
        days_late = (df[recv_col] - df[due_col]).dt.days
        days_late = days_late.clip(lower=0).fillna(0)
    else:
        days_late = pd.Series([0]*len(df))
    # buckets
    bins = [-1, 0, 30, 60, 90, 10**9]
    labels = ["On time", "1–30", "31–60", "61–90", ">90"]
    bucket = pd.cut(days_late, bins=bins, labels=labels)
    s = df.groupby(bucket)[amount_col].sum(min_count=1)
    ax = s.plot(kind="bar")
    ax.set_ylabel("Amount")
    ax.set_xlabel("Aging Bucket")
    ax.set_title("AR Aging (by amount)")
    return ax
