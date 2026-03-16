import pandas as pd

df = pd.read_csv("datasets/s1.csv")

print("Dataset:\n", df)

print("\nDataset info:")
df.info()

print("\nStatistical Summary:\n", df.describe())

# Top student in math
top_math = df[df["math"] == df["math"].max()]
print("\nTop student in Math:")
print(top_math)

# Calculate average marks
df["average"] = (df["math"] + df["science"] + df["english"]) / 3

print("\nStudents with Average Marks:")
print(df[["name", "average"]])

# Best overall student
best_student = df[df["average"] == df["average"].max()]

print("\nBest Overall Student:")
print(best_student)