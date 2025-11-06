import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AR Analytics – Open Data", layout="wide")

st.title("Accounts Receivable Analytics – Open Data")
st.caption("Source: Excelx (synthetic). Place AR .xlsx into data/raw/.")

data_path = Path(__file__).parents[2] / "data" / "raw"
uploaded = None

# Auto-load first xlsx in data/raw if present
xlsx_files = list(data_path.glob("*.xlsx"))
if xlsx_files:
    uploaded = xlsx_files[0]
    st.info(f"Auto-loaded: {uploaded.name}")
else:
    st.warning("Put the Accounts Receivable workbook in data/raw/ to auto-load.")

df = None
if uploaded:
    try:
        df = pd.read_excel(uploaded)
        st.subheader("Preview")
        st.dataframe(df.head(25))
        # Basic derived columns if available
        for c in ["InvoiceDate","DueDate","ReceivedDate"]:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")
        if set(["DueDate","ReceivedDate"]).issubset(df.columns):
            df["DaysLate"] = (df["ReceivedDate"] - df["DueDate"]).dt.days.clip(lower=0)
        if "Status" in df.columns:
            ontime = None
            if set(["ReceivedDate","DueDate"]).issubset(df.columns):
                ontime = (df["ReceivedDate"] <= df["DueDate"]).mean()
            st.metric("Rows", len(df))
            if ontime is not None:
                st.metric("On-time Payment %", f"{ontime*100:.1f}%")
    except Exception as e:
        st.error(f"Failed to read Excel: {e}")
