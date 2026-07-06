from generator import generate_transaction_data
from analyzers import run_financial_analysis
from visualizer import generate_charts
from data_cleaning import clean_transaction_data


def main():
    # Step 1: Run Data Generation
    generate_transaction_data()
    # Step 2: Clean
    cleaned_df = clean_transaction_data("data/customer_transactions.csv")
    # Step 3: Extract Metrics via Analyzer
    report_data = run_financial_analysis()
    
    # Step : Draw plots
    generate_charts(report_data)
    
    # Step 5: Display standard text report
    print("\n" + "="*50)
    print("          FINANCIAL ANALYSIS REPORT          ")
    print("="*50)
    
    print(f"Total Customers           : {report_data['total_customers']}")
    print(f"Total Transactions        : {report_data['total_transactions']}")
    print(f"Total Deposits            : ${report_data['total_deposits']:,.2f}")
    print(f"Total Withdrawals         : ${report_data['total_withdrawals']:,.2f}")
    
    top_cat = report_data['spending_by_category'].idxmax()
    top_cat_val = report_data['spending_by_category'].max()
    print(f"Top Spending Category     : {top_cat} (${top_cat_val:,.2f})")
    
    top_cust = report_data['cust_spending'].idxmax()
    top_cust_val = report_data['cust_spending'].max()
    print(f"Highest Customer Spending : {top_cust} (${top_cust_val:,.2f})")
    
    print("\nMonthly Summary")
    print(report_data['monthly_summary'].tail(3))
    
    print("\nFraud Alerts")
    total_alerts = len(report_data['fraud_alerts'])
    print(f"Flagged Transactions (Threshold: ${report_data['outlier_threshold']:.2f}): {total_alerts} detected.")
    if total_alerts > 0:
        print(report_data['fraud_alerts'][['Transaction_ID', 'Customer_ID', 'Amount']].head(3).to_string(index=False))
        
    print("\nRecommendations")
    if report_data['net_savings'] < 0:
        print(f"⚠️ Net burn structural variance negative. Reduce budget caps inside the '{top_cat}' segment.")
    else:
        print("✅ Liquidity positions strong. Target secondary reserves into diversified asset classes.")
    print(f"⚠️ Flag operations processing on accounts showing spikes clear of standard boundaries.")
    print("="*50)

if __name__ == "__main__":
    main()