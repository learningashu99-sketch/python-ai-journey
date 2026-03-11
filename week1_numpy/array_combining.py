import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

print("Original aaray A: ",a)
print("Original aaray B: ",b,"\n")

r1 = np.concatenate((a,b))
print("Concatenate array (A+B): ",r1)

r2 = np.vstack((a,b))
print("Vertical Stack: \n ",r2)

r3 = np.hstack((a,b))
print("Horizontal Stack: ",r3)