# app.py (Modified sections)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_cleaning import clean_transaction_data
from analyzers import run_spending_analysis, run_trend_analysis, aggregate_customer_metrics
from fraud_detector import flag_anomalies
from report_generator import export_to_excel_memory
import io

# Import the NEW charting functions
from report_generator import (
    render_line_trends,
    render_spending_pie,
    render_debit_histogram,
    render_category_boxplot
)

# Page Configuration (Keep existing)
st.set_page_config(page_title="Financial Transaction Analytics", layout="wide")
st.title("Python-Based Banking and Financial Transaction Analysis Platform")

# Data Caching & Load (Keep existing)
@st.cache_data
def load_and_clean_data():
    return clean_transaction_data("data/customer_transactions.csv")

df = load_and_clean_data()
spending_summary = run_spending_analysis(df)
trend_summary = run_trend_analysis(df)
customer_ledger = aggregate_customer_metrics(df)
fraud_alerts = flag_anomalies(df)

# Sidebar (Keep existing)
st.sidebar.header("Executive Summary")
# ... (Keep existing Sidebar metric code here) ...
st.sidebar.header("Executive Summary")
total_inflow = df[df['Type'] == 'Credit']['Amount'].sum()
total_outflow = df[df['Type'] == 'Debit']['Amount'].sum()

st.sidebar.metric(label="Total Inflow (Credits)", value=f"${total_inflow:,.2f}")
st.sidebar.metric(label="Total Outflow (Debits)", value=f"${total_outflow:,.2f}")
st.sidebar.metric(label="Net Liquidity Position", value=f"${(total_inflow - total_outflow):,.2f}")
# -------------------------------------------------------------------
# Navigation Tabs (Modified)
# -------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Chronological Trends (Line)",
    "🍕 Spending Composition (Pie)",
    "📊 Amount Distribution (Hist/Box)",
    "👥 Customer & Fraud Risk",
    "📁 Raw Ledger Audit"
])

# --- TAB 1: CHRONOLOGICAL TRENDS (LINE) ---
with tab1:
    st.header("Financial Macro-Trends (2026)")
    # LINE CHART
    fig_line = render_line_trends(trend_summary)
    st.pyplot(fig_line)

# --- TAB 2: SPENDING COMPOSITION (PIE) ---
with tab2:
    st.header("Sector Breakdown: Outflow Composition")
    # PIE CHART
    fig_pie = render_spending_pie(spending_summary)
    st.pyplot(fig_pie)

# --- TAB 3: AMOUNT DISTRIBUTION (HIST/BOX) ---
with tab3:
    st.header("Debit Transaction Profiling")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Debit Frequency Analysis (Histogram)")
        # HISTOGRAM
        fig_hist = render_debit_histogram(df)
        st.pyplot(fig_hist)
        
    with col2:
        st.subheader("Category Volatility (Box Plot)")
        # BOX PLOT
        fig_box = render_category_boxplot(df)
        st.pyplot(fig_box)

# --- TAB 4: CUSTOMER & FRAUD RISK (Merged from previous tabs) ---
with tab4:
    col_cust, col_fraud = st.columns([3, 2])
    
    with col_cust:
        st.header("Customer Accounts Balance")
        search_query = st.text_input("Filter by Customer ID (e.g., CUST_001):").strip()
        filtered_ledger = customer_ledger[customer_ledger['Customer_ID'].str.contains(search_query, case=False)] if search_query else customer_ledger
        st.dataframe(filtered_ledger, use_container_width=True)
        
    with col_fraud:
        st.header("Statistical Fraud Alerts")
        st.warning(f"{len(fraud_alerts)} high-risk anomalies flagged.")
        st.dataframe(fraud_alerts, use_container_width=True)

# --- TAB 5: RAW LEDGER AUDIT ---
with tab5:
    st.header("Systemic Master Database Ledger")
    st.dataframe(df, use_container_width=True)

    if st.button("Generate Excel Report"):

        excel_data = export_to_excel_memory(
            spending_summary,
            trend_summary,
            customer_ledger,
            fraud_alerts
        )

        st.download_button(
            label="Download Excel Report",
            data=excel_data,
            file_name="Financial_Analytics_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )