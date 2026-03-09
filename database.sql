USE ecommerce_returns;


CREATE TABLE returns_data (
    Order_ID VARCHAR(20),
    Product_ID VARCHAR(20),
    User_ID VARCHAR(20),
    Order_Date VARCHAR(20),
    Return_Date VARCHAR(20),
    Product_Category VARCHAR(50),
    Product_Price DECIMAL(10,2),
    Order_Quantity INT,
    Return_Reason VARCHAR(100),
    Return_Status VARCHAR(20),
    Days_to_Return VARCHAR(20),
    User_Age INT,
    User_Gender VARCHAR(10),
    User_Location VARCHAR(50),
    Payment_Method VARCHAR(20),
    Shipping_Method VARCHAR(20),
    Discount_Applied DECIMAL(10,2)
);


TRUNCATE TABLE returns_data;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ecommerce_returns_synthetic_datas.csv'
INTO TABLE returns_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Order_ID, Product_ID, User_ID, @Order_Date, @Return_Date,
 Product_Category, Product_Price, Order_Quantity, @Return_Reason,
 Return_Status, @Days_to_Return, User_Age, User_Gender,
 User_Location, Payment_Method, Shipping_Method, Discount_Applied)
SET
Order_Date = STR_TO_DATE(@Order_Date, '%Y-%m-%d'),
Return_Date = NULLIF(@Return_Date, ''),
Return_Reason = NULLIF(@Return_Reason, ''),
Days_to_Return = NULLIF(@Days_to_Return, '');
SELECT COUNT(*) FROM returns_data;
ALTER TABLE returns_data
ADD COLUMN Prediction INT,
ADD COLUMN RiskScore FLOAT;
INSERT INTO returns_data 
(Order_ID, User_ID, Product_Category, Product_Price, Order_Quantity, Discount_Applied, Payment_Method, Shipping_Method, User_Age, User_Gender, User_Location)
VALUES 
('ORDER20001', 'USER20001', 'Electronics', 600, 1, 10, 'Credit Card', 'Express', 26, 'Male', 'CityX');
SELECT COUNT(*) FROM returns_data;
ALTER TABLE returns_data
DROP COLUMN Prediction;
ALTER TABLE returns_data
ADD COLUMN Prediction INT;
INSERT INTO returns_data 
(Order_ID, Product_ID, User_ID, Product_Category, User_Age, User_Gender, User_Location,
 Product_Price, Order_Quantity, Discount_Applied, Payment_Method, Shipping_Method)
VALUES
('ORDER30001', 'PROD30001', 'USER30001', 'Electronics', 28, 'Female', 'CityB',
 1200, 2, 25, 'Credit Card', 'Express');
 SELECT Order_ID, Prediction, RiskScore 
FROM returns_data
WHERE Order_ID = 'ORDER30001';
SELECT Order_ID, Prediction, RiskScore 
FROM returns_data
WHERE Order_ID = 'ORDER30001';
INSERT INTO returns_data 
(Order_ID, Product_ID, User_ID, Product_Category, User_Age, User_Gender, User_Location,
 Product_Price, Order_Quantity, Discount_Applied, Payment_Method, Shipping_Method)
VALUES
('ORDER30005', 'PROD30005', 'USER30005', 'Clothing', 28, 'Female', 'CityE',
 1200, 2, 25, 'Credit Card', 'Express');
SELECT Order_ID, Prediction, RiskScore
FROM returns_data
ORDER BY Order_ID DESC
LIMIT 1;



