import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

def show_download():
    st.title("📥 Download Expense History")

    file_path = os.path.join("data", "expenses.csv")

    if not os.path.exists(file_path):
        st.warning("No expense data found.")
        return

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    # Button selection
    st.subheader("Select Duration")
    selected = st.radio(
        "Choose a range",
        ["Custom Range", "1M", "6M", "1Y", "5Y"],
        index=0,  # Default to the first option
        horizontal=True,
    )

    today = datetime.today()

    if selected == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=today - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=today)
    else:
        durations = {"1M": 30, "6M": 182, "1Y": 365, "5Y": 1825}
        days = durations[selected]
        start_date = today - timedelta(days=days)
        end_date = today

    # Filter data based on the selected date range
    filtered = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

    # If no data is found in the selected range
    if filtered.empty:
        max_available = df["date"].max()
        st.info(f"No data found in selected range. Data till {max_available.strftime('%d-%m-%Y')} is available.")
    else:
        # Display filtered data
        st.dataframe(filtered[["date", "category", "amount"]])
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, file_name="expenses_filtered.csv", mime="text/csv")

