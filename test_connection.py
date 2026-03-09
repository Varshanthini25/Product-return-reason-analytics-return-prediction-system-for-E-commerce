import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",              
    password="varsha06",  
    database="ecommerce_returns"  
)

if conn.is_connected():
    print("MySQL Connected Successfully!")

conn.close()
