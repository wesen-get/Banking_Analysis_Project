import pandas as pd
import numpy as np

def clean_transaction_data(file_path):
    print("-> Reading and cleaning raw data...")
    df = pd.read_csv(file_path)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Drop records missing vital ID elements
    df.dropna(subset=['Customer_ID'], inplace=True)
    
    # Fill missing transaction values using category medians
    df['Amount'] = df.groupby('Category')['Amount'].transform(lambda x: x.fillna(x.median()))
    
    # Explicit type casting
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].astype(float)
    
    # Save a copy to the processed folder for audit records
    df.to_csv("data/processed/cleaned_transactions.csv", index=False)
    return df