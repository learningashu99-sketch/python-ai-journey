import pandas as pd

# Load dataset
df = pd.read_csv("datasets/s1.csv")

print("===== STUDENT ANALYSIS =====\n")

# Dataset info
print("Dataset Info:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

# Top students in each subject
top_math = df[df["math"] == df["math"].max()]["name"].values[0]
top_science = df[df["science"] == df["science"].max()]["name"].values[0]
top_english = df[df["english"] == df["english"].max()]["name"].values[0]

print("\nTop Students:")
print("Math:", top_math)
print("Science:", top_science)
print("English:", top_english)

# Add average column
df["average"] = (df["math"] + df["science"] + df["english"]) / 3

# Best overall student
best_student = df[df["average"] == df["average"].max()]["name"].values[0]
print("\nBest Overall Student:", best_student)

# Students with average > 80
high_performers = df[df["average"] > 80]["name"]

print("\nStudents with Average > 80:")
for student in high_performers:
    print(student)

# Ranking students
sorted_df = df.sort_values("average", ascending=False)

print("\nTop 3 Students:")
top3 = sorted_df.head(3)

for i, name in enumerate(top3["name"], start=1):
    print(f"{i}. {name}")

# Add result column
def get_result(avg):
    if avg >= 80:
        return "Excellent"
    elif avg >= 60:
        return "Good"
    else:
        return "Needs Improvement"

df["result"] = df["average"].apply(get_result)

print("\nFinal Dataset with Results:")
print(df[["name", "average", "result"]])