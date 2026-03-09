import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="varsha06",
    database="ecommerce_returns"
)

query = """
SELECT * 
FROM returns_data 
ORDER BY id DESC 
LIMIT 1
"""


new_orders = pd.read_sql(query, conn)

print("New Orders Found:", len(new_orders))
print(new_orders)
print("Picked record:")
print(new_orders[['id','Order_ID']])


conn.close()

