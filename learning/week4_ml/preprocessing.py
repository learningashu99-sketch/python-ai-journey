import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

#Create dataset with missing values
df = pd.DataFrame({
    "hours": [1, 2, None, 4, 5],
    "sleep": [8, None, 6, 6, 5],
    "gender": ["M", "F", "M", "F", "M"],
    "city": ["A", "B", "A", "B", "C"],
    "marks": [30, 40, 50, 60, 70]
})

print("Original Data: \n",df)

#Missing values
#1. Filling missing values with mean
df["hours"] = df["hours"].fillna(df["hours"].mean())
df["sleep"] = df["sleep"].fillna(df["sleep"].mean())

print("\nAfter handling missing values: \n",df)

#Encoding 
encoder = LabelEncoder()
df["gender"] = encoder.fit_transform(df["gender"])
df["city"] = encoder.fit_transform(df["city"])

print("\nAfter Encoding:\n",df)

#Feature scaling
scaler = StandardScaler()
df[["hours","sleep"]] = scaler.fit_transform(df[["hours","sleep"]])

print("\nAfter scaling:\n",df)
print("\nDescirbe data: \n",df.describe())
# print("\n",df.head())