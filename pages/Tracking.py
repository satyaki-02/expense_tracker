import streamlit as st
import pandas as pd
import os
import altair as alt
from src.theme import theme_toggle

theme_toggle()  

DATA_PATH = "data/expenses.csv"

st.title("📊 Expense Tracking")

# Load data
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    if "date" in df.columns:
        df = df.rename(columns={"date": "Date"})
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
    else:
        st.error("The file doesn't contain a 'date' column.")
        st.stop()
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # Show total expense
    total = df["Amount"].sum()
    st.metric("Total Expense", f"₹{total:,.2f}")

    # Bar chart: Monthly expenses
    monthly = df.groupby("Month")["Amount"].sum().reset_index()
    bar = alt.Chart(monthly).mark_bar().encode(
        x="Month",
        y="Amount"
    ).properties(title="Monthly Expenses")
    st.altair_chart(bar, use_container_width=True)

    # Pie chart: Expense by category
    category = df.groupby("Category")["Amount"].sum().reset_index()
    st.subheader("Expenses by Category")
    st.dataframe(category)

    pie = alt.Chart(category).mark_arc().encode(
        theta="Amount",
        color="Category",
        tooltip=["Category", "Amount"]
    )
    st.altair_chart(pie, use_container_width=True)

else:
    st.warning("No expenses found. Add entries from the Home page.")
