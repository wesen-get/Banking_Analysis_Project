import pandas as pd

def flag_anomalies(df):
    print("-> Scanning dataset for high-risk fraud markers...")
    debit_df = df[df['Type'] == 'Debit']
    
    # Z-Score Category Outliers
    cat_stats = debit_df.groupby('Category')['Amount'].agg(['mean', 'std']).reset_index()
    df_merged = pd.merge(df, cat_stats, on='Category', how='left')
    df_merged['Z_Score'] = (df_merged['Amount'] - df_merged['mean']) / df_merged['std']
    
    fraud_alerts = df_merged[(df_merged['Type'] == 'Debit') & (df_merged['Z_Score'] > 3)]
    return fraud_alerts[['Transaction_ID', 'Customer_ID', 'Date', 'Category', 'Amount', 'Z_Score']]