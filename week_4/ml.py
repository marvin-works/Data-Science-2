import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

study_data = pd.DataFrame({
    "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8],
    "exam_score": [52, 58, 63, 68, 74, 77, 84, 88]
})

X = study_data[["hours_studied"]]
y = study_data["exam_score"]

model = LinearRegression()
model.fit(X, y)

print("Learned slope (w):", model.coef_[0])
print("Learned intercept (b):", model.intercept_)
print("R²:", model.score(X, y))

# plt.scatter(X, y, label="actual data")
# plt.plot(X, model.predict(X), color="red", label="fitted line")
# plt.xlabel("Hours studied")
# plt.ylabel("Exam score")
# plt.title("Linear Regression Fit")
# plt.legend()
# plt.show()

# predictions = model.predict(X)
# plt.scatter(X, y, label="actual")
# plt.plot(X, predictions, color="red", label="fitted line")
# for i in range(len(X)):
#     plt.plot([X.iloc[i,0], X.iloc[i,0]], [y.iloc[i], predictions[i]], color="gray", linestyle="--")
# plt.legend()
# plt.show()

from sklearn.metrics import mean_squared_error

predictions = model.predict(X)
mse_1 = mean_squared_error(y, predictions)

mse_2 = np.mean((y - predictions) ** 2)

print("MSE using sklearn:", mse_1)
print("MSE manually:", mse_2)

prediction_10 = model.predict([[10]])

print("Predicted score:", prediction_10[0])