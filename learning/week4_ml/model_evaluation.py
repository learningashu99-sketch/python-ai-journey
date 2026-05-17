import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv("datasets/ml_hours_marks.csv")

X = df[["hours"]]
y = df["marks"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

#Evaluation
mse = mean_squared_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)

#Print information
print("X_train: \n",X_train)
print("X_test: \n",X_test)
print("Actual:", y_test.values)
print("Predicted:", y_pred)

print("MSE:", mse)
print("R2 Score:", r2)