import pandas as pd

df = pd.read_csv("F:/python ai journey/projects/student_performance_sysytem/data/student_data.csv")

print("First row:\n")
print(df.head(),"\n")
print("Dataset info: \n")
df.info()


print("\nMissing values: \n",df.isnull().sum())

print("\nDuplicate values: \n",df.duplicated().sum())

#adding average marks column
# df["average"] = 

# top marks
top_marks = df[df["marks"]==df["marks"].max()]
print("\nHighest marks: \n",top_marks)