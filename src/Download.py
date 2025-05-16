import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple

def get_date_range(selected: str) -> Tuple[datetime, datetime]:
    """Helper function to get date range based on selection"""
    today = datetime.today()
    if selected == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=today - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=today)
        return start_date, end_date
    
    durations = {"1M": 30, "6M": 182, "1Y": 365, "5Y": 1825}
    days = durations[selected]
    return today - timedelta(days=days), today

def show_download():
    st.title("📥 Download Expense History")

    file_path = Path("data") / "expenses.csv"
    if not file_path.exists():
        st.warning("No expense data found.")
        return

    try:
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
        df.dropna(subset=["date"], inplace=True)

        st.subheader("Select Duration")
        selected = st.radio(
            "Choose a range",
            ["Custom Range", "1M", "6M", "1Y", "5Y"],
            index=0,
            horizontal=True,
        )

        start_date, end_date = get_date_range(selected)
        filtered = df[(df["date"] >= pd.to_datetime(start_date)) & 
                      (df["date"] <= pd.to_datetime(end_date))]

        if filtered.empty:
            max_available = df["date"].max()
            if pd.isna(max_available):
                st.info("No valid date found in the dataset.")
            else:
                st.info(f"No data found in selected range. Data till {max_available.strftime('%d-%m-%Y')} available.")
        else:
            st.table(filtered[["date", "category", "amount"]])
            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download CSV", 
                csv, 
                file_name=f"expenses_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
