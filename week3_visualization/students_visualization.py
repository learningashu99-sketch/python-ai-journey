import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/students.csv")

print("Average marks: ",df["Marks"].mean())
print("Maximum marks: ",df["Marks"].max())
print("Minimum marks: ",df["Marks"].min())

#Lin plot

plt.plot(df["Name"],df["Marks"],marker='o',color='green')
plt.title("Marks trend")
plt.xlabel("Student")
plt.ylabel("Marks")
plt.grid(True)
plt.savefig("week3_visualization/marks_trend.png")
plt.close()

#bar chart
plt.bar(df["Name"],df["Marks"],color='violet')
for i,value in enumerate(df["Marks"]):
    plt.text(i,value,str(value),ha='center')
plt.title("Marks comparison")
plt.xlabel("Student")
plt.ylabel("Marks")
plt.grid(axis='y')
plt.savefig("week3_visualization/marks_comparison.png")
plt.close()

#scatter plot
plt.scatter(df["Age"],df["Marks"],color='red',s=100)
for i,Name in enumerate(df["Name"]):
    plt.text(df["Age"][i],df["Marks"][i],Name)
plt.title("Age vs Marks")
plt.xlabel("Age")
plt.ylabel("Marks")
plt.grid(True)
plt.savefig("week3_visualization/age_vs_marks.png")
plt.close()
