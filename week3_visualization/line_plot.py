import pandas as pd
import matplotlib.pyplot as pilot

#Learning to use 
# x =[1,2,3,4]
# y=[10,20,30,40]

# pilot.plot(x,y)
# pilot.title("simple line plot")
# pilot.xlabel("X Axis")
# pilot.ylabel("Y Axis")

# pilot.show()

#implying it 
df = pd.read_csv("datasets/students.csv")

pilot.plot(df["Name"],df["Marks"])

pilot.title("Students Marks line plot")
pilot.xlabel("Students")
pilot.ylabel("Marks")

pilot.grid(True)
pilot.show()
