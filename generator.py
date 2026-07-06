import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_transaction_data(cust_file='data/customers.csv', txn_file='data/customer_transactions.csv', num_rows=5500):
    os.makedirs(os.path.dirname(cust_file), exist_ok=True)
    
    np.random.seed(42)
    
    # 1. GENERATE DISTINCT CUSTOMERS BASE
    cust_ids = [f"CUST{i}" for i in range(100, 125)] # 25 unique customers
    names = ["Wesen Getnet", "Almaz Abebe", "Dawit Yohannes", "Chala Kebede", "Aster Tolossa", 
             "Makeda Selassie", "Yonas Assefa", "Fatuma Mohammed", "Eleni Tsegaye", "Bekele Zewdu"]
    
    # Fill remaining names if list is shorter than customer count
    while len(names) < len(cust_ids):
        names.append(f"Customer User {len(names)+1}")
        
    genders = ['Male', 'Female', 'Non-binary']
    locations = ["Addis Ababa", "Hawassa", "Adama", "Bahir Dar", "Gondar", "Dire Dawa"]
    account_types = ["Savings", "Checking", "Premium Checking", "Student Account"]
    
    customers_data = {
        'Customer_ID': cust_ids,
        'Customer_Name': names,
        'Age': np.random.randint(18, 65, size=len(cust_ids)),
        'Gender': np.random.choice(genders, size=len(cust_ids), p=[0.48, 0.48, 0.04]),
        'City': np.random.choice(locations, size=len(cust_ids)),
        'Account_Type': np.random.choice(account_types, size=len(cust_ids))
    }
    
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_csv(cust_file, index=False)
    print(f"[SUCCESS] Customer Profile file saved with {len(df_customers)} records at: {cust_file}")
    # 2. GENERATE TRANSACTIONS MAP
    merchants = ["Amazon", "Walmart", "Uber", "Netflix", "Local Shell Gas", "Starbucks", "Target", "Costco", "Stripe Vendor", "City Utilities"]
    categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Health']
    start_date = datetime(2025, 1, 1)
    row_cust_ids = np.random.choice(cust_ids, size=num_rows)
    row_types = np.random.choice(['Credit', 'Debit'], size=num_rows, p=[0.3, 0.7])
    row_amounts = np.round(np.random.exponential(scale=120, size=num_rows) + 5, 2)
    
    balance_tracker = {cid: np.random.uniform(5000, 25000) for cid in cust_ids}
    row_balances = []
    row_fraud_flags = np.zeros(num_rows, dtype=int)
    
    dates = [start_date + timedelta(minutes=int(i * (525600 / num_rows))) for i in range(num_rows)]
    
    for i in range(num_rows):
        cid = row_cust_ids[i]
        ttype = row_types[i]
        amt = row_amounts[i]
        
        if ttype == 'Credit':
            balance_tracker[cid] += amt
        else:
            balance_tracker[cid] -= amt
            
        row_balances.append(round(balance_tracker[cid], 2))
        
    transactions_data = {
        'Transaction_ID': [f"TXN{i:05d}" for i in range(1, num_rows + 1)],
        'Customer_ID': row_cust_ids,
        'Date': dates,
        'Type': row_types,
        'Category': np.random.choice(categories, size=num_rows),
        'Merchant': np.random.choice(merchants, size=num_rows),
        'Amount': row_amounts,
        'Balance': row_balances,
        'Fraud_Flag': row_fraud_flags
    }
    
    df_transactions = pd.DataFrame(transactions_data)
    
    # Inject anomalies
    anomaly_indices = [120, 450, 1200, 3100, 4800]
    for idx in anomaly_indices:
        if idx < num_rows:
            df_transactions.loc[idx, 'Amount'] = round(np.random.uniform(12000, 25000), 2)
            df_transactions.loc[idx, 'Fraud_Flag'] = 1
            df_transactions.loc[idx, 'Balance'] = round(df_transactions.loc[idx, 'Balance'] - df_transactions.loc[idx, 'Amount'], 2)
            
    df_transactions.to_csv(txn_file, index=False)
    print(f"[SUCCESS] Transactions Log file saved with {len(df_transactions)} records at: {txn_file}")