import pandas as pd

data1 = pd.Series([10,20,30,40])
print("Index  elements\n",data1)

data2 = {
    "Name": ["Alice","Bob","Charlie"],
    "Age": [22,25,23],
    "Marks": [85,90,88]
}

df = pd.DataFrame(data2)
print("Student Data:")
print(df)

print("\nFirst rows:")
print(df.head())