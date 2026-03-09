# ==========================================
# E-COMMERCE RETURNS ANALYSIS -  FINAL PROJECT CODE 1
# ==========================================
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("ecommerce_returns_synthetic_datas.csv")
df.columns = df.columns.str.strip()

print(" Dataset Loaded: 10,000 Orders")
print("Columns:", list(df.columns))

# === CLEANING ===
print("\n CLEANING DATA...")
print("Missing values:\n", df.isnull().sum())

df.drop_duplicates(inplace=True)
df['Days_to_Return'] = df['Days_to_Return'].abs()

# === TARGET VARIABLE ===
df['Returned'] = df['Return_Status'].apply(lambda x: 1 if x == 'Returned' else 0)

# === SAFE FEATURES ===
df['HighValueOrder'] = (df['Product_Price'] > df['Product_Price'].quantile(0.75)).astype(int)
df['ExpressShipping'] = (df['Shipping_Method'].str.contains('Express|Next-Day', na=False)).astype(int)

print("\n BASIC STATS:")
print(f"Total Orders: {len(df):,}")
print(f"Returns: {df['Returned'].sum():,} ({df['Returned'].mean():.1%})")

# === ANALYSIS ===
print("\n TOP RETURN REASONS:")
returned_df = df[df['Returned'] == 1]
print(returned_df['Return_Reason'].value_counts())

print("\n CATEGORY RETURN RATES:")
print(df.groupby('Product_Category')['Returned'].mean().sort_values(ascending=False))

# ==========================================
# HIGH RISK CUSTOMERS - IF-ELSE VERSION
# ==========================================
print("\n HIGH RISK CUSTOMERS :")

customer_returns = df.groupby('User_ID')['Returned'].sum()
df['CustomerReturnCount'] = df['User_ID'].map(customer_returns)

high_risk_customers = df[df['CustomerReturnCount'] >= 2]

if high_risk_customers['User_ID'].nunique() > 0:

    print(high_risk_customers[['User_ID', 'CustomerReturnCount']]
          .drop_duplicates()
          .sort_values('CustomerReturnCount', ascending=False).head(10))
else:
    print("0  high-risk customers found")


