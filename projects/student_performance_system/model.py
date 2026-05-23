import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error

df = pd.read_csv("F:/python ai journey/projects/student_performance_system/data/student_data.csv")

#input
X = df[["hours_studied", "attendance", "sleep_hours", "practice_tests"]]

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
y_pred = model.predict(x_test)

#Evaluation 
r2 = r2_score(y_test,y_pred)
mae = mean_absolute_error(y_test,y_pred)
mse = mean_squared_error(y_test,y_pred)


####Now the real game......................

hours, attendance, sleep_hours,practice_tests = map(
    float,input("Enter study hours, attendance, sleep hours, and practice tests: ").split())

new_data = pd.DataFrame(
    [[hours, attendance, sleep_hours, practice_tests]],
    columns=["hours_studied", "attendance", "sleep_hours", "practice_tests"]
)

#New data for predcition
c_pred = model.predict(new_data)

#Print information

print("\nActual Values: \n", y_test.values)
print("\nPredicted Values:\n", y_pred.round(2))

print("\nModel Evaluattion....\n")
print("R2 Score: ", round(r2,2))
print("MAE: ",round(mae,2))
print("MSE: ", round(mse,2))

print("\nCustom Student Prediction:")
predicted_marks = max(0, min(100, c_pred[0]))

print("Predicted Marks:", round(predicted_marks, 2))




