import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("datasets/ml_hours_marks.csv")
X = df[["hours"]]
Y = df["marks"]

#model 
model = LinearRegression()
model.fit(X,Y)

#prediction
y_pred = model.predict(X)

#plot
plt.scatter(X,Y)
plt.plot(X,y_pred)
plt.xlabel("Hours")
plt.ylabel("Makrs")
plt.title("Linear Regression")
plt.savefig("outputs/regression_plot.png")
plt.show()

#model info
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)