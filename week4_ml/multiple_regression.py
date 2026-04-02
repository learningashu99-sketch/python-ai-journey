import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#Create dataset
df = pd.DataFrame({
    "hours": [1, 2, 3, 4, 5],
    "sleep": [5,6,7,8,9],
    "practice": [1,2,3,4,5],
    "marks": [30, 40, 50, 60, 70]
})




#Feature and target
x = df[["hours","sleep","practice"]] #multiple inputs
y= df["marks"]

#split
x_train,x_test,y_train,y_test = train_test_split(
    x,y,test_size=0.4,random_state=42)

#model 
model = LinearRegression()
model.fit(x_train,y_train)


#predict
y_pred = model.predict(x_test)

#print information
print("Actual: ",y_test.values)
print("Predicted: ",y_pred)

#model coffiecient
print("Coffiecients: ",model.coef_)
print("Intercept: ",model.intercept_)

new_data = pd.DataFrame([[6,6,6]], columns=["hours","sleep","practice"])
prediction = model.predict(new_data)
print("Predcted Marks:",prediction)