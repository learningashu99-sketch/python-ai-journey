import pandas as pd

df = pd.read_csv("F:/python ai journey/datasets/students.csv")

print("Datasets: \n",df)
print("\nFirst rows:")
print(df.head(),"\n")
print("\nDataset info:")
print(df.info(),)

print("\nStatistics:")
print(df.describe())