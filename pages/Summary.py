import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_summary():
    st.title("📊 Monthly Summary")

    # Load budget and expenses
    budget_path = os.path.join("data", "budget.csv")
    expense_path = os.path.join("data", "expenses.csv")

    if os.path.exists(budget_path):
        budget_df = pd.read_csv(budget_path)
    else:
        budget_df = pd.DataFrame(columns=["month", "budget"])

    if os.path.exists(expense_path):
        expense_df = pd.read_csv(expense_path)
    else:
        expense_df = pd.DataFrame(columns=["date", "amount", "category"])

    # Format date
    expense_df["date"] = pd.to_datetime(expense_df["date"], format="%d-%m-%Y", errors="coerce")
    expense_df.dropna(subset=["date"], inplace=True)
    expense_df["month"] = expense_df["date"].dt.strftime("%m-%Y")

    # Current month
    current_month = datetime.now().strftime("%m-%Y")

    # Show current month summary
    st.subheader(f"Summary for {current_month}")

    monthly_expenses = expense_df[expense_df["month"] == current_month]
    total_spent = monthly_expenses["amount"].sum()

    current_budget_row = budget_df[budget_df["month"] == current_month]
    if not current_budget_row.empty:
        monthly_budget = current_budget_row["budget"].values[0]
        remaining = monthly_budget - total_spent
        st.metric("💰 Monthly Budget", f"₹{monthly_budget:,.2f}")
        st.metric("💸 Spent", f"₹{total_spent:,.2f}")
        st.metric("📉 Remaining", f"₹{remaining:,.2f}")
    else:
        st.warning("No budget set for this month.")

    if not monthly_expenses.empty:
        st.subheader("📂 Expenses Breakdown")
        st.dataframe(monthly_expenses[["date", "amount", "category"]])
    else:
        st.info("No expenses recorded for this month.")
