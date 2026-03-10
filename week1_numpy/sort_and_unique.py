import numpy as np

arr = np.array([9,3,6,1,5])
print("Original array:", arr)
print("Sorted array:", np.sort(arr))
dup_arr = np.array([1,2,2,3,3,4])

print("Array with duplicates:", dup_arr)
print("Unique values:", np.unique(dup_arr))