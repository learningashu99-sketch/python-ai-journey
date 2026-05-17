import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/s1.csv")

plt.scatter(df["math"],df["science"],color='red',s=100)

for i,Name in enumerate(df["name"]):
    plt.text(df["math"][i],df["science"][i],Name)

plt.title("math vs science")

plt.xlabel("Math")
plt.ylabel("Science")


plt.show()