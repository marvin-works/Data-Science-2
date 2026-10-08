import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

study = pd.DataFrame({
    "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "passed": [0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
})

X = study[["hours_studied"]]
y = study["passed"]

model = LogisticRegression()
model.fit(X, y)

hours_range = np.linspace(0, 11, 200).reshape(-1, 1)
probabilities = model.predict_proba(hours_range)[:, 1]   # probability of "passed"

plt.scatter(X, y, label="actual outcome")
plt.plot(hours_range, probabilities, color="red", label="predicted probability")
plt.axhline(0.5, color="gray", linestyle="--", label="decision threshold")
plt.xlabel("Hours studied")
plt.ylabel("Probability of passing")
plt.title("Logistic Regression — S-curve")
plt.legend()
plt.show()


from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

predictions = model.predict(X)
print(confusion_matrix(y, predictions))
print("Accuracy:", accuracy_score(y, predictions))
print("Precision:", precision_score(y, predictions))
print("Recall:", recall_score(y, predictions))
print("F1:", f1_score(y, predictions))

