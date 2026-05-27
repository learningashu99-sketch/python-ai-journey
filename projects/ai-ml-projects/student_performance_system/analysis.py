import pandas as pd
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv("F:/python ai journey/projects/ai-ml-projects/student_performance_system/data/student_data.csv")

print("\nFirst row:\n")
print(df.head(),"\n")
print("Dataset info: \n")
df.info()


print("\nMissing values: \n",df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nCorrelation Matrix:\n")
print(df.corr(numeric_only=True))

#average marks 
avg = df["marks"].mean()
print(f"\nAverage Marks: {avg:.2f}")

# top marks
top_marks = df[df["marks"]==df["marks"].max()]
print("\nHighest marks: \n",top_marks)

#lowest marks
low_marks = df[df["marks"]==df["marks"].min()]
print("\nLowest makrs: \n",low_marks)

##plotting time baby.....

plt.figure(figsize=(8,5))

#Scattering plot
plt.scatter(df["hours_studied"],df["marks"],color='blue',s=50)

for i,id in enumerate(df["student_id"]):
    plt.text(df["hours_studied"][i],df["marks"][i],id)

plt.title("Hours studied VS Marks")
plt.xlabel("Hours studied")
plt.ylabel("Marks")

plt.savefig("F:/python ai journey/projects/ai-ml-projects/student_performance_system/outputs/scatter_plot.png")
plt.show()


# NEW FIGURE
plt.figure(figsize=(8,5))

#Bar chart

plt.bar(df["student_id"],df["marks"],color='violet')

for i,value in enumerate(df["marks"]):
    plt.text(df["student_id"][i],value+1,str(value),ha='center')

plt.title("Student performance")
plt.xlabel("Student ID")
plt.ylabel("Marks")

plt.savefig("F:/python ai journey/projects/ai-ml-projects/student_performance_system/outputs/bar_chart.png")
plt.show()