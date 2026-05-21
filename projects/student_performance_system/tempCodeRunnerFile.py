import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error

df = pd.read_csv("F:/python ai journey/projects/student_performance_system/data/student_data.csv")

#input
X = df[["hours_studied", "attendance", "sleep_hours", "practice_tests"]]
hours, attendance, sleep_hours,practice_tests = map(float,input().split())
new_data = [[hours,attendance,sleep_hours,practice_tests]]
#output
Y = df["marks"]

#split
x_train,x_test,y_train,y_test = train_test_split(
    X,Y,test_size=0.3,random_state=42
)

#Model 
model = LinearRegression()
model.fit(x_train,y_train)

#Predict 
y_pred = model.predict(new_data)

#Evaluation 
r2 = r2_score(y_test,y_pred)
mae = mean_absolute_error(y_test,y_pred)
mse = mean_squared_error(y_test,y_pred)

#Print information
print("X_train: \n",x_train)
print("X_test: \n",x_test)
print("Actual:", y_test.values)
print("Predicted:", y_pred.round(2))


print("R2 Score: ", round(r2,2))
print("MAE: ",round(mae,2))
print("MSE: ", round(mse,2))