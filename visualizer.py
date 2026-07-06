import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_charts(results, output_path='output/financial_charts.png'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = results['raw_df']
    
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    
    # 1. Bar Chart: Customer Spending
    top_cust = results['cust_spending'].sort_values(ascending=False).head(10)
    sns.barplot(x=top_cust.index, y=top_cust.values, ax=axes[0,0], palette="Blues_r")
    axes[0,0].set_title('Top 10 Customers by Total Spending')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. Pie Chart: Expense Category
    axes[0,1].pie(results['spending_by_category'], labels=results['spending_by_category'].index, autopct='%1.1f%%', colors=sns.color_palette("Pastel1"))
    axes[0,1].set_title('Expense Distribution by Category')
    
    # 3. Line Chart: Monthly Expense
    m_summary = results['monthly_summary']
    sns.lineplot(x=m_summary.index, y=m_summary['Monthly_Expenses'], marker="o", color="red", ax=axes[1,0])
    axes[1,0].set_title('Monthly Expense Trend')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 4. Histogram: Transaction Amount Distribution
    sns.histplot(df[df['Amount'] < 1000]['Amount'], bins=50, kde=True, color="purple", ax=axes[1,1])
    axes[1,1].set_title('Transaction Amount Distribution (< $1000)')
    
    # 5. Box Plot: Detect Outliers
    sns.boxplot(x=df['Amount'], ax=axes[2,0], color="orange")
    axes[2,0].set_title('Box Plot for Outlier Detection')
    
    # Clean up empty graph coordinates
    axes[2,1].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"[SUCCESS] Analytical charts compiled successfully at: {output_path}")