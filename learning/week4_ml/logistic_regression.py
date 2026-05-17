import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

#Create Dataset 
df = pd.DataFrame({
    "hours": [1, 2, 3, 4, 5, 6],
    "marks": [30, 35, 40, 55, 70, 80],
    "result": [0, 0, 0, 1, 1, 1]   # 0 = Fail, 1 = Pass
})

#Features & Marks
x = df[["hours","marks"]]
y = df["result"]

#Split
x_train,x_test,y_train,y_test = train_test_split(
    x,y,test_size=0.6,random_state=42,stratify=y
)

#Model 
model = LogisticRegression()
model.fit(x_train,y_train)

#Prediction
y_pred = model.predict(x_test)

print("Actual:", y_test.values)
print("Predicted:", y_pred)

#Probability
probs = model.predict_proba(x_test)
print("Probabilities:\n", probs)