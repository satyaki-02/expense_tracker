import streamlit as st
import pandas as pd
from datetime import datetime
import os
from src.theme import theme_toggle

def show_home():
    theme_toggle()

    st.title("🏠 Home - Monthly Expense Setup")

    DATA_FILE = "data/expenses.csv"
    current_month = datetime.now().strftime("%Y-%m")

    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["date", "category", "amount", "month", "type"])
        df.to_csv(DATA_FILE, index=False)

    df = pd.read_csv(DATA_FILE)

    monthly_budget_row = df[(df["month"] == current_month) & (df["type"] == "budget")]
    monthly_budget = float(monthly_budget_row["amount"].iloc[0]) if not monthly_budget_row.empty else None
    monthly_expenses = df[(df["month"] == current_month) & (df["type"] == "expense")]["amount"].sum()

    if monthly_budget is None:
        st.subheader("📝 Set Monthly Budget")
        budget = st.number_input("Enter your total budget for this month", min_value=0.0, format="%.2f")
        if st.button("Set Budget"):
            new_row = {
                "date": datetime.now().strftime("%d-%m-%Y"),
                "category": "Total Budget",
                "amount": budget,
                "month": current_month,
                "type": "budget"
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Budget set successfully! Refresh the page to continue.")
    else:
        st.subheader("📥 Add Expense")
        date = st.date_input("Date", format="DD-MM-YYYY")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Other"])
        amount = st.number_input("Expense Amount", min_value=0.0, format="%.2f")

        if st.button("Add Expense"):
            new_expense = {
                "date": date.strftime("%d-%m-%Y"),
                "category": category,
                "amount": amount,
                "month": current_month,
                "type": "expense"
            }
            df = df.append(new_expense, ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Expense added!")

        st.subheader("📊 Monthly Summary")
        st.metric("Total Budget", f"₹{monthly_budget:,.2f}")
        st.metric("Total Spent", f"₹{monthly_expenses:,.2f}")
        st.metric("Remaining", f"₹{monthly_budget - monthly_expenses:,.2f}")

        progress = monthly_expenses / monthly_budget if monthly_budget > 0 else 0
        st.progress(min(progress, 1.0))
