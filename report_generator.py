# report_generator.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import streamlit as st
import pandas as pd
from report_generator import export_to_excel_memory
# Set a standard theme
sns.set_theme(style="whitegrid")

def render_line_trends(trends_df):
    """Generates a standard line plot for cash flow trends."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Cast Year_Month back to str if it's Period type
    trends_plot = trends_df.copy()
    if pd.api.types.is_period_dtype(trends_plot['Year_Month']):
         trends_plot['Year_Month'] = trends_plot['Year_Month'].astype(str)

    ax.plot(trends_plot['Year_Month'], trends_plot['Credit'], marker='o', label='Inflow', color='green', linewidth=2.5)
    ax.plot(trends_plot['Year_Month'], trends_plot['Debit'], marker='s', label='Outflow', color='crimson', linewidth=2.5)
    ax.set_title('Monthly Financial Inflow vs Outflow', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Volume ($)')
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    return fig

def render_spending_pie(spending_df):
    """Generates a pie chart of total spending by category."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Define colors
    colors = sns.color_palette('pastel')[0:len(spending_df)]
    
    ax.pie(spending_df['Total_Spent'], 
           labels=spending_df['Category'], 
           autopct='%1.1f%%', 
           startangle=140, 
           colors=colors,
           wedgeprops={'edgecolor': 'white'})
    
    ax.set_title('Aggregate Spending Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def render_debit_histogram(df):
    """Generates a histogram with KDE of debit transaction amounts."""
    debits = df[df['Type'] == 'Debit']
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.histplot(data=debits, x='Amount', bins=30, kde=True, color='purple', ax=ax)
    
    ax.set_title('Frequency Distribution of Debit Amounts', fontsize=14, fontweight='bold')
    ax.set_xlabel('Transaction Amount ($)')
    ax.set_ylabel('Transaction Count')
    plt.tight_layout()
    return fig

def render_category_boxplot(df):
    """Generates box plots of debits, separated by category."""
    debits = df[df['Type'] == 'Debit']
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.boxplot(data=debits, x='Category', y='Amount', palette='Set3', ax=ax)
    
    ax.set_title('Debit Amount Volatility by Sector', fontsize=14, fontweight='bold')
    ax.set_xlabel('Spending Category')
    ax.set_ylabel('Amount ($)')
    plt.xticks(rotation=30)
    plt.tight_layout()
    return fig

# --- Maintain original functionality for main.py automated report ---
def generate_visualizations(spending, trends):
    print("-> Rendering dashboards for file export...")
    
    # Create the combined dashboard for file output
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.barplot(data=spending, x='Category', y='Total_Spent', ax=axes[0], palette='viridis')
    axes[0].set_title('Total Spending per Category', fontsize=12, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=30)

    # Convert Period to string for plotting if necessary
    trends_plot = trends.copy()
    if pd.api.types.is_period_dtype(trends_plot['Year_Month']):
        trends_plot['Year_Month'] = trends_plot['Year_Month'].astype(str)

    axes[1].plot(trends_plot['Year_Month'], trends_plot['Credit'], marker='o', label='Inflow', color='green')
    axes[1].plot(trends_plot['Year_Month'], trends_plot['Debit'], marker='s', label='Outflow', color='crimson')
    axes[1].set_title('Monthly Inflow vs Outflow Trends', fontsize=12, fontweight='bold')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('outputs/charts/financial_dashboard.png', dpi=300)
    plt.close()

