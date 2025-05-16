import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
from typing import Tuple

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and merge budget and expense data"""
    budget_path = Path("data") / "budget.csv"
    expense_path = Path("data") / "expenses.csv"
    
    budget_df = pd.read_csv(budget_path) if budget_path.exists() else pd.DataFrame(columns=["month", "budget"])
    expense_df = pd.read_csv(expense_path) if expense_path.exists() else pd.DataFrame(columns=["date", "amount", "category"])
    
    # Clean and merge data
    expense_df["date"] = pd.to_datetime(expense_df["date"], format="%d-%m-%Y", errors="coerce")
    expense_df.dropna(subset=["date"], inplace=True)
    expense_df["month"] = expense_df["date"].dt.strftime("%m-%Y")
    
    return budget_df, expense_df

def show_summary():
    st.title("📊 Monthly Summary")
    
    try:
        budget_df, expense_df = load_data()
        current_month = datetime.now().strftime("%m-%Y")
        monthly_expenses = expense_df[expense_df["month"] == current_month]
        total_spent = monthly_expenses["amount"].sum()
        
        current_budget_row = budget_df[budget_df["month"] == current_month]
        
        if not current_budget_row.empty:
            monthly_budget = current_budget_row["budget"].values[0]
            remaining = monthly_budget - total_spent
            
            # Display metrics
            st.markdown(f"""
                <div style="font-size:24px; margin-bottom:10px;">
                    🧮 Amount Left to Spend: <span style="color:{'red' if remaining < 0 else '#4BB543'}">₹{remaining:,.2f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(3)
            cols[0].metric("💰 Monthly Budget", f"₹{monthly_budget:,.2f}")
            cols[1].metric("💸 Spent", f"₹{total_spent:,.2f}")
            cols[2].metric("📉 Remaining", f"₹{remaining:,.2f}")
            
            if remaining < 0:
                st.error("🚨 You've overspent your monthly budget!")
            
            st.progress(min(total_spent / monthly_budget, 1.0))
            
            # Visualizations
            if not monthly_expenses.empty:
                st.subheader("📂 Expenses Breakdown")
                category_summary = monthly_expenses.groupby("category")["amount"].sum().reset_index()
                
                tab1, tab2 = st.tabs(["Chart", "Data"])
                with tab1:
                    fig = px.pie(category_summary, names='category', values='amount', 
                               title='Spending by Category')
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    st.dataframe(monthly_expenses[["date", "amount", "category"]]
                                 .sort_values(by="date", ascending=False))
        else:
            st.warning("⚠️ No budget set for this month.")
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")