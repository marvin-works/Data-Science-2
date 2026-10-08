import numpy as np

# Vectorized operations
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)   # [11 22 33]
print(a * b)   # [10 40 90]

# Broadcasting
arr = np.array([1, 2, 3])
print(arr + 10)     # [11 12 13]  <- 10 is "broadcast" across every element

matrix = np.array([[1, 2, 3], 
                   [4, 5, 6]])   # shape (2, 3)
row = np.array([10, 20, 30])  # shape (3,)
print(matrix + row)
# [[11 22 33]
#  [14 25 36]]
# row is broadcast across every row of matrix


# Aggregation
arr = np.array([[1, 2, 3], 
                [4, 5, 6]])
print(arr.sum())          # 21  <- everything
print(arr.sum(axis=0))    # [5 7 9]   <- sum down each COLUMN
print(arr.sum(axis=1))    # [6 15]     <- sum across each ROW
print(arr.mean())          # 3.5
print(arr.max())            # 6


# Basic linear algebra
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.dot(a, b))   # 32   <- 1*4 + 2*5 + 3*6, a single number

A = np.array([[1, 2], 
              [3, 4]])
B = np.array([[5, 6], 
              [7, 8]])
print(A @ B)   # matrix multiplication (@ is the operator for it)
# [[19 22]
#  [43 50]]

scores = np.array([
    [70, 85, 90], #student 1
    [60, 75, 80], #student 2
    [95, 88, 92], #student 3
    [50, 65, 70]  #student 4
])

print(scores.mean(axis=1))
print(scores.mean(axis=0))
print(scores + 5)
weights = np.array([0.2, 0.3, 0.5])
weighted_total = scores @ weights
print(weighted_total)