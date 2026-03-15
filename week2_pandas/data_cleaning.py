import pandas as pd

df = pd.read_csv("datasets/students.csv")

print("Missing Values: \n",df.isnull())
#False-Values, True- Missing Value

print("\nRemoving Missing Values: \n",df.dropna())
print("\nFilling Value with 0: \n",df.fillna(0))

print("\nColumn:- Missing Value:\n",df.isnull().sum())

df["Marks"]= df["Marks"].fillna(df["Marks"].mean())
print("\nFilling Missing Value with the mean of Marks: ")
print(df)