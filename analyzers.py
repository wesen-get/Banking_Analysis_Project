import pandas as pd

def run_spending_analysis(df):
    print("-> Analyzing sector spending behaviors...")
    debit_df = df[df['Type'] == 'Debit']
    summary = debit_df.groupby('Category')['Amount'].agg(['sum', 'mean', 'count']).rename(
        columns={'sum': 'Total_Spent', 'mean': 'Average_Ticket', 'count': 'Transaction_Count'}
    ).reset_index()
    return summary

def run_trend_analysis(df):
    print("-> Computing macro monthly trends...")
    df_trends = df.copy()
    df_trends['Year_Month'] = df_trends['Date'].dt.to_period('M').astype(str)
    summary = df_trends.groupby(['Year_Month', 'Type'])['Amount'].sum().unstack(fill_value=0).reset_index()
    return summary

def aggregate_customer_metrics(df):
    print("-> Aggregating individual customer balances...")
    metrics = df.groupby('Customer_ID').agg(
        Total_Deposits=('Amount', lambda x: x[df.loc[x.index, 'Type'] == 'Credit'].sum()),
        Total_Withdrawals=('Amount', lambda x: x[df.loc[x.index, 'Type'] == 'Debit'].sum())
    ).reset_index()
    metrics['Net_Balance'] = metrics['Total_Deposits'] - metrics['Total_Withdrawals']
    return metrics