import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

df = pd.read_csv("projects/ai-ml-projects/student_performance_system/data/student_data.csv")

#Input
X = df[
    [
        "hours_studied",
        "attendance",
        "sleep_hours",
        "practice_tests"
    ]
]

#Output
y = df["result"]

#split
x_train,x_test,y_train,y_test = train_test_split(
    X,y,test_size=0.4,random_state=42)

#Model
model = LogisticRegression()
model.fit(x_train,y_train)

#Predict
y_pred = model.predict(x_test)



#Accuracy
accuracy = accuracy_score(y_test,y_pred)

#Confusion metrics
Confusion_mat = confusion_matrix(y_test,y_pred)

#Custom Predict
hours, attendance, sleep_hours,practice_tests = map(
    float,input("Enter study hours, attendance, sleep hours, and practice tests: ").split())

new_data = pd.DataFrame(
    [[hours, attendance, sleep_hours, practice_tests]],
    columns=["hours_studied", "attendance", "sleep_hours", "practice_tests"]
)

#New data for prediction
c_pred = model.predict(new_data)


#Print information
print("Accuracy Score:", round(accuracy * 100, 2), "%")
print("Y_test:\n",y_test)
print("Y_pred: ",y_pred)
print("Model Coefficient:",model.coef_)
print("Model Intercept:",model.intercept_)
print("Confusion Matrix:")
print(Confusion_mat)


predictedcted_result = c_pred[0]

print("\nCustom Student Prediction:")

if c_pred == 0:
    print("Predicted Result: PASS")

else:
    print("Predicted Result: FAIL")





