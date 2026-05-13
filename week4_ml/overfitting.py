import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dataset
df = pd.DataFrame({
    "hours": [1,2,3,4,5,6,7,8,2,5],
    "marks": [30,35,40,50,60,70,80,90,65,45],
    "result": [0,0,0,0,1,1,1,1,1,0]
})

# Features & target
X = df[["hours","marks"]]
y = df['result']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

#Deep tree(Overfitting risk)
model = DecisionTreeClassifier(max_depth=10)

#Train
model.fit(X_train,y_train)

#predictions
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

# Accuracy
train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, test_pred)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)