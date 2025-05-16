import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional

DATA_FILE = Path("data") / "expenses.csv"
CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Other", "Entertainment"]

def initialize_data_file():
    """Ensure data file exists with correct structure"""
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(exist_ok=True)
        pd.DataFrame(columns=["date", "category", "amount", "month", "type"]).to_csv(DATA_FILE, index=False)

def get_current_budget(df: pd.DataFrame) -> Optional[float]:
    """Get current month's budget if set"""
    current_month = datetime.now().strftime("%Y-%m")
    monthly_budget_row = df[(df["month"] == current_month) & (df["type"] == "budget")]
    return float(monthly_budget_row["amount"].iloc[0]) if not monthly_budget_row.empty else None

def show_home():
    st.title("🏠 Home - Monthly Expense Setup")
    initialize_data_file()
    
    try:
        df = pd.read_csv(DATA_FILE)
        current_month = datetime.now().strftime("%Y-%m")
        monthly_budget = get_current_budget(df)
        monthly_expenses = df[(df["month"] == current_month) & (df["type"] == "expense")]["amount"].sum()

        if monthly_budget is None:
            st.subheader("📝 Set Monthly Budget")
            with st.form("budget_form"):
                budget = st.number_input("Enter your total budget for this month", 
                                       min_value=0.0, format="%.2f", step=100.0)
                if st.form_submit_button("Set Budget"):
                    new_row = {
                        "date": datetime.now().strftime("%d-%m-%Y"),
                        "category": "Total Budget",
                        "amount": budget,
                        "month": current_month,
                        "type": "budget"
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Budget set successfully!")
                    st.experimental_rerun()
        else:
            st.subheader(f"💰 Current Budget: ₹{monthly_budget:,.2f}")
            st.subheader("📥 Add Expense")
            
            with st.form("expense_form"):
                date = st.date_input("Date")
                category = st.selectbox("Category", CATEGORIES)
                amount = st.number_input("Expense Amount", min_value=0.0, format="%.2f")
                
                if st.form_submit_button("Add Expense"):
                    new_expense = {
                        "date": date.strftime("%d-%m-%Y"),
                        "category": category,
                        "amount": amount,
                        "month": current_month,
                        "type": "expense"
                    }
                    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Expense added!")
                    st.experimental_rerun()
                    
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")