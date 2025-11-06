import pandas as pd

def engineer_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    if {"DueDate","ReceivedDate"}.issubset(df.columns):
        df["DaysLate"] = (df["ReceivedDate"] - df["DueDate"]).dt.days
        df["DaysLate"] = df["DaysLate"].clip(lower=0)
        df["OnTime"] = (df["ReceivedDate"] <= df["DueDate"]).astype(int)
    return df
