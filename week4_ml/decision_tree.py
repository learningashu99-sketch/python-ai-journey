import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

#Create Dataset 
df = pd.DataFrame({
    "hours": [1, 2, 3, 4, 5, 6],
    "marks": [30, 35, 40, 55, 70, 90],
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
model = DecisionTreeClassifier()
model.fit(x_train,y_train)

#Prediction
y_pred = model.predict(x_test)

print("Actual:", y_test.values)
print("Predicted:", y_pred)

n_pred = pd.DataFrame([[3, 45]],columns = ["hours","marks"])
print("\nPrediction for [hours=3, marks=45]:", model.predict(n_pred))

print("\nTree Depth:", model.get_depth())
print("\nFeature Importance:", model.feature_importances_)