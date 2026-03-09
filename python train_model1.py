# ==========================================
# TRAIN MODEL FILE (train_model.py)
# ==========================================

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# ==========================
# LOAD DATASET
# ==========================
df = pd.read_csv("ecommerce_returns_synthetic_datas.csv")
df.columns = df.columns.str.strip()

# Drop missing categorical rows
df = df.dropna(subset=[
    'Product_Category',
    'Payment_Method',
    'Shipping_Method',
    'User_Gender',
    'User_Location'
])

# ==========================
# TARGET VARIABLE
# ==========================
df['Returned'] = df['Return_Status'].apply(
    lambda x: 1 if x == 'Returned' else 0
)

# ==========================
# FEATURE ENGINEERING
# ==========================
df['HighValueOrder'] = (
    df['Product_Price'] > df['Product_Price'].quantile(0.75)
).astype(int)

df['ExpressShipping'] = (
    df['Shipping_Method'].str.contains('Express|Next-Day', na=False)
).astype(int)

df['DiscountHigh'] = (df['Discount_Applied'] > 20).astype(int)
df['BulkOrder'] = (df['Order_Quantity'] >= 3).astype(int)

# ==========================
# FEATURE SELECTION
# ==========================
features = [
    'Product_Category',
    'User_Age',
    'User_Gender',
    'User_Location',
    'Product_Price',
    'Order_Quantity',
    'Discount_Applied',
    'Payment_Method',
    'Shipping_Method',
    'HighValueOrder',
    'ExpressShipping',
    'DiscountHigh',
    'BulkOrder'
]

X = df[features].copy()
y = df['Returned']

# ==========================
# ENCODING
# ==========================
encoders = {}

for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

# ==========================
# TRAIN TEST SPLIT
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================
# RANDOM FOREST MODEL
# ==========================
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=3,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================
# EVALUATION
# ==========================
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\nMODEL PERFORMANCE")
print(classification_report(y_test, y_pred))
print("AUC-ROC:", roc_auc_score(y_test, y_proba))

# ==========================
# SAVE MODEL & ENCODERS
# ==========================
joblib.dump(model, "return_model.pkl")
joblib.dump(encoders, "encoders.pkl")
joblib.dump(features, "features.pkl")

print("\nModel & Encoders Saved Successfully!")
df['Return_Status'].value_counts()
