import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/students.csv")

plt.bar(df["Name"],df["Marks"],color="blue")
#add value on top of the bar
for i,value in enumerate(df["Marks"]):
    plt.text(i,value,str(value),ha='center')
plt.title("Students performance")

plt.xlabel("Students")
plt.ylabel("Marks")
plt.grid(axis='y')

plt.show()