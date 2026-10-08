import numpy as np

arr = np.array([1, 2, 3, 4])
print(arr * 2)         

a = np.array([1, 2, 3])
print(a.shape)      

b = np.array([[1, 2, 3], [4, 5, 6]])
print(b.shape)      

num_1 = np.array([[1, 2, 3, 4]])
print(num_1[0])

arr = np.array([10, 20, 30, 40, 50])
print(arr[1:3])     

b = np.array([[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 9]])
print(b[1:3, 1:3])   

arr= np.array([29, 34, 65, 76, 87, 90])
print(arr[0:6])

arr = np.array([1, 2, 3, 4, 5])
sub = arr[1:3]
sub[0] = 999
print(arr)  


scores = np.array([
    [85, 90, 78, 92],
    [72, 88, 91, 80],
    [95, 84, 89, 93]
])

sliced = scores[0:2, 2:4]       # first 2 students, last 2 subjects
sliced_copy = sliced.copy()     # independent copy of that slice

sliced_copy[0, 0] = 999

print(sliced_copy)
print(scores)