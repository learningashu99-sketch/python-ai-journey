import pandas as pd

df = pd.read_csv("datasets/students.csv")

print("Full dataset:")
print(df)

print("\nNames column:")
print(df["Name"])

print("\nName and Marks columns:")
print(df[["Name","Marks"]])

print("\nStudents scoring above 88:")
print(df[df["Marks"] > 88])