import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error



df = pd.read_csv("projects/ai-ml-projects/student_performance_system/data/student_data.csv")

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

print("\nModel Coefficients:")
print(model.coef_.round(2))

print("\nModel Intercept:")
print(model.intercept_.round(2),"\n")

#Predict 
y_pred = model.predict(x_test)

#Visualization

plt.plot(y_test.values, marker='o',color='blue', label="Actual")
plt.plot(y_pred, marker='x',color='red', label="Predicted")

plt.title("Actual VS Predicted Marks")
plt.xlabel("Actual Marks")
plt.ylabel("Predicted Marks")

plt.grid(True)

plt.legend()

plt.savefig("F:/python ai journey/projects/ai-ml-projects/student_performance_system/outputs/actual_vs_predicted.png")
plt.show()


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

#New data for prediction
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




