import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# -----------------------------
# Existing chart functions
# -----------------------------

def render_line_trends(trends_df):
    fig, ax = plt.subplots(figsize=(10,5))

    trends_plot = trends_df.copy()
    if pd.api.types.is_period_dtype(trends_plot["Year_Month"]):
        trends_plot["Year_Month"] = trends_plot["Year_Month"].astype(str)

    ax.plot(trends_plot["Year_Month"], trends_plot["Credit"], marker="o", label="Inflow")
    ax.plot(trends_plot["Year_Month"], trends_plot["Debit"], marker="o", label="Outflow")

    ax.set_title("Monthly Financial Inflow vs Outflow")
    ax.legend()

    plt.xticks(rotation=30)
    plt.tight_layout()

    return fig


def render_spending_pie(spending_df):
    fig, ax = plt.subplots(figsize=(8,8))

    ax.pie(
        spending_df["Total_Spent"],
        labels=spending_df["Category"],
        autopct="%1.1f%%"
    )

    ax.set_title("Spending Distribution")

    return fig


def render_debit_histogram(df):
    fig, ax = plt.subplots(figsize=(10,5))

    debits = df[df["Type"]=="Debit"]

    sns.histplot(
        data=debits,
        x="Amount",
        bins=30,
        kde=True,
        ax=ax
    )

    return fig


def render_category_boxplot(df):
    fig, ax = plt.subplots(figsize=(12,6))

    debits = df[df["Type"]=="Debit"]

    sns.boxplot(
        data=debits,
        x="Category",
        y="Amount",
        ax=ax
    )

    plt.xticks(rotation=30)

    return fig


# ======================================================
# EXPORT EXCEL
# ======================================================
import os
def export_to_excel_memory(
    df,
    spending,
    trends,
    customers,
    fraud
):
    # Save a local copy
    file_path = "output/reports/Financial_Analytics_Report.xlsx"

    trends_export = trends.copy()
    if pd.api.types.is_period_dtype(trends_export["Year_Month"]):
        trends_export["Year_Month"] = trends_export["Year_Month"].astype(str)

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw_Transactions", index=False)
        trends_export.to_excel(writer, sheet_name="Monthly_Trends", index=False)
        spending.to_excel(writer, sheet_name="Category_Spending", index=False)
        customers.to_excel(writer, sheet_name="Customer_Ledger", index=False)
        fraud.to_excel(writer, sheet_name="Fraud_Alerts", index=False)

    # Create download copy
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw_Transactions", index=False)
        trends_export.to_excel(writer, sheet_name="Monthly_Trends", index=False)
        spending.to_excel(writer, sheet_name="Category_Spending", index=False)
        customers.to_excel(writer, sheet_name="Customer_Ledger", index=False)
        fraud.to_excel(writer, sheet_name="Fraud_Alerts", index=False)

    output.seek(0)

    return output