import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = pd.DataFrame({
    "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "exam_score":    [42, 50, 54, 60, 63, 70, 72, 80, 85, 90]
})

X = data[["hours_studied"]]   # features
y = data["exam_score"]         # target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)      # THIS is the training loop you did by hand — now automated

print("Learned parameters:", model.coef_, model.intercept_)

predictions = model.predict(X_test)
print("Predictions on NEW data:", predictions)
print("Actual values:", y_test.values)
print("Error (MSE):", mean_squared_error(y_test, predictions))