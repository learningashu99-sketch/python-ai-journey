import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("datasets/ml_hours_marks.csv")

X = df[["hours"]]
y = df["marks"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Model
model = LinearRegression()

# Train only on training data
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Plot
plt.scatter(X_train, y_train, label="Train")
plt.scatter(X_test, y_test, label="Test", color="red")
plt.plot(X, model.predict(X), label="Model")
plt.legend()
plt.plot(X, model.predict(X))
plt.title("Train-Test Split Regression")
plt.xlabel("Hours")
plt.ylabel("Marks")
plt.savefig("outputs/day22_split_plot.png")
plt.show()

# Print values
print("X_train: \n",X_train)
print("X_test: \n",X_test)
print("Actual:", y_test.values)
print("Predicted:", y_pred)