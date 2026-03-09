# ==========================================
# PREDICT FROM MYSQL (predict_mysql.py)
# ==========================================

import pandas as pd
import mysql.connector
import joblib

# ==========================
# LOAD SAVED MODEL FILES
# ==========================
model = joblib.load("return_model.pkl")
encoders = joblib.load("encoders.pkl")
features = joblib.load("features.pkl")

# ==========================
# MYSQL CONNECTION
# ==========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="varsha06",      # 🔴 change this
    database="ecommerce_returns"      # 🔴 change this
)

# ==========================
# GET LATEST ORDER
# ==========================
query = """
SELECT * 
FROM returns_data 
ORDER BY id DESC 
LIMIT 1
"""

new_order = pd.read_sql(query, conn)
if new_order.empty:
    print("No new orders found.")
    conn.close()
    exit()

order_id = new_order.loc[0, 'Order_ID']

# ==========================
# FEATURE ENGINEERING
# ==========================
new_order['HighValueOrder'] = (
    new_order['Product_Price'] > 1000
).astype(int)

new_order['ExpressShipping'] = (
    new_order['Shipping_Method'].str.contains('Express|Next-Day', na=False)
).astype(int)

new_order['DiscountHigh'] = (
    new_order['Discount_Applied'] > 20
).astype(int)

new_order['BulkOrder'] = (
    new_order['Order_Quantity'] >= 3
).astype(int)

# ==========================
# REMOVE UNNECESSARY COLUMNS
# ==========================
drop_cols = [
    'Order_ID',
    'User_ID',
    'Product_ID',
    'Order_Date',
    'Return_Status',
    'Prediction',
    'RiskScore'
]

new_order = new_order.drop(columns=drop_cols, errors='ignore')

# ==========================
# HANDLE UNSEEN CATEGORIES
# ==========================
for col in new_order.select_dtypes(include='object').columns:
    if col in encoders:
        if new_order[col].iloc[0] not in encoders[col].classes_:
            new_order[col] = encoders[col].classes_[0]

# ==========================
# ENCODE
# ==========================
for col in encoders.keys():
    if col in new_order.columns:
        new_order[col] = encoders[col].transform(
            new_order[col].astype(str)
        )

# Ensure correct column order
new_order = new_order.reindex(columns=features, fill_value=0)

# ==========================
# PREDICTION
# ==========================
risk_score = model.predict_proba(new_order)[:, 1][0]
prediction = int(model.predict(new_order)[0])

# ==========================
# UPDATE MYSQL
# ==========================
cursor = conn.cursor()

update_query = """
UPDATE returns_data
SET Prediction = %s,
    RiskScore = %s
WHERE Order_ID = %s
"""

cursor.execute(update_query, (
    prediction,
    float(risk_score),
    order_id
))

conn.commit()

print("Prediction Updated Successfully!")
print("Risk Score:", round(risk_score, 3))
print("Prediction:", prediction)

cursor.close()
conn.close()       


