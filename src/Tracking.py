import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt
from typing import Optional

def load_expense_data() -> Optional[pd.DataFrame]:
    """Load and clean expense data"""
    data_path = Path("data") / "expenses.csv"
    if not data_path.exists():
        return None
    
    df = pd.read_csv(data_path)
    if "date" not in df.columns:
        return None
    
    df["Date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df.dropna(subset=["Date"], inplace=True)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    
    # Standardize column names
    df = df.rename(columns={
        "amount": "Amount",
        "category": "Category"
    })
    
    return df

def show_tracking():
    st.title("📊 Expense Tracking")
    
    df = load_expense_data()
    if df is None:
        st.warning("No expenses found. Add entries from the Home page.")
        return
    
    # Overall metrics
    total = df["Amount"].sum()
    st.metric("Total Expense", f"₹{total:,.2f}")
    
    # Visualization tabs
    tab1, tab2 = st.tabs(["Monthly Trends", "Category Breakdown"])
    
    with tab1:
        monthly = df.groupby("Month")["Amount"].sum().reset_index()
        bar = alt.Chart(monthly).mark_bar().encode(
            x=alt.X("Month", sort=None),
            y="Amount",
            tooltip=["Month", "Amount"]
        ).properties(
            title="Monthly Expenses",
            width=600
        )
        st.altair_chart(bar, use_container_width=True)
    
    with tab2:
        category = df.groupby("Category")["Amount"].sum().reset_index()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.table(category.sort_values("Amount", ascending=False))
        
        with col2:
            pie = alt.Chart(category).mark_arc().encode(
                theta="Amount",
                color="Category",
                tooltip=["Category", "Amount"]
            ).properties(
                title="Expense Distribution"
            )
            st.altair_chart(pie, use_container_width=True)