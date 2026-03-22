import pandas as pd
import matplotlib.pyplot as plt

# # x =[1,2,3,4]
# # y=[10,20,30,40]

# # pilot.plot(x,y,marker='o',linestyle="--",color="red")
# # pilot.title("simple line plot")
# # pilot.xlabel("X Axis")
# # pilot.ylabel("Y Axis")

# # pilot.grid(True)
# x =[1,2,3,4]
# y1=[10,20,30,40]
# y2=[13,26,39,52]

# pilot.plot(x,y1,label="Line 1")
# pilot.plot(x,y2,label="Line 2")
# pilot.title("MUltiple lines")
# pilot.xlabel("X Axis")
# pilot.ylabel("Values")
# pilot.legend()


# pilot.show()


df = pd.read_csv("datasets/students.csv")

plt.plot(df["Name"], df["Marks"], marker='o',linestyle="--",color="red",label="Marks")

plt.title("Student Marks Visualization")
plt.xlabel("Students")
plt.ylabel("Marks")

plt.legend()
plt.grid(True)
plt.show()

df = pd.read_csv("datasets/students.csv")

plt.plot(df["Name"], df["Marks"], marker='o',linestyle="--",color="red",label="Marks")
plt.plot(df["Name"], df["Age"], marker='x',linestyle="--",color="blue",label="Age")

plt.title("Marks vs Age")
plt.xlabel("Students")
plt.ylabel("Values")

plt.legend()
plt.grid(True)
plt.show()