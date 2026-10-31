
import pandas as pd

# ----------------------------------
# 1. Load the sales dataset
# ----------------------------------

df = pd.read_csv('sales_data.csv')

print("\n========== SALES DATA ANALYSIS ==========")

print("\nOriginal Dataset:")
print(df.head())

# ----------------------------------
# 2. Explore the dataset
# ----------------------------------

print("\nDataset Shape:", df.shape)

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

# ----------------------------------
# 3. Check missing values and duplicates
# ----------------------------------

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

# ----------------------------------
# 4. Clean the dataset
# ----------------------------------

df_clean = df.copy()

# Remove duplicate records
df_clean = df_clean.drop_duplicates()

# Fill missing product names
df_clean['Product'] = df_clean['Product'].fillna('Unknown')

# Convert numerical columns
for column in ['Quantity', 'Unit_Price', 'Total_Sales']:
    df_clean[column] = pd.to_numeric(
        df_clean[column], errors='coerce'
    )

# Remove rows with missing quantity or price
df_clean = df_clean.dropna(
    subset=['Quantity', 'Unit_Price']
)

# Fill missing sales values
df_clean['Total_Sales'] = df_clean['Total_Sales'].fillna(
    df_clean['Quantity'] * df_clean['Unit_Price']
)

# Save cleaned dataset
df_clean.to_csv('cleaned_sales_data.csv', index=False)

print("\nData cleaning completed!")

# ----------------------------------
# 5. Analyze the sales data
# ----------------------------------

if df_clean.empty:
    raise ValueError("No valid sales records available for analysis.")

# Calculate total revenue
total_revenue = df_clean['Total_Sales'].sum()

# Calculate total quantity sold
total_quantity = df_clean['Quantity'].sum()

# Calculate average sales
average_sales = df_clean['Total_Sales'].mean()

# Calculate highest and lowest sales
highest_sales = df_clean['Total_Sales'].max()
lowest_sales = df_clean['Total_Sales'].min()

# Find best-selling product by quantity
product_sales = df_clean.groupby('Product')['Quantity'].sum()

best_product = product_sales.idxmax()
best_quantity = product_sales.max()

# Calculate revenue by product
revenue_by_product = df_clean.groupby(
    'Product'
)['Total_Sales'].sum()

# ----------------------------------
# 6. Display the results
# ----------------------------------

print("\n========== SALES SUMMARY ==========")

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Products Sold: {total_quantity:,.0f}")
print(f"Average Sales: ₹{average_sales:,.2f}")
print(f"Highest Sales: ₹{highest_sales:,.2f}")
print(f"Lowest Sales: ₹{lowest_sales:,.2f}")

print("\nBest-Selling Product:", best_product)
print("Quantity Sold:", best_quantity)

print("\nRevenue by Product:")
print(revenue_by_product.sort_values(ascending=False))

# ----------------------------------
# 7. Generate the analysis report
# ----------------------------------

report = f"""
# SALES DATA ANALYSIS REPORT

## Dataset Information

- Original Records: {len(df)}
- Cleaned Records: {len(df_clean)}
- Columns: {len(df.columns)}
- Duplicate Records Removed: {df.duplicated().sum()}

## Sales Metrics

- Total Revenue: ₹{total_revenue:,.2f}
- Total Products Sold: {total_quantity:,.0f}
- Average Sales: ₹{average_sales:,.2f}
- Highest Sales: ₹{highest_sales:,.2f}
- Lowest Sales: ₹{lowest_sales:,.2f}

## Best-Selling Product

- Product: {best_product}
- Quantity Sold: {best_quantity:,.0f}

## Revenue by Product

{revenue_by_product.sort_values(ascending=False).to_string()}

## Conclusion

The sales analysis identified the best-selling product
and calculated important sales performance metrics.

The dataset was cleaned before analysis to improve
the reliability of the results.
"""

# Save report as Markdown
with open('analysis_report.md', 'w', encoding='utf-8') as file:
    file.write(report)

print("\nAnalysis report generated successfully!")
print("Files created: analysis_report.md and cleaned_sales_data.csv")
