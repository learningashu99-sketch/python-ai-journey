import numpy as np  
arr = np.array([1,2,3,4,5,6])
matrix1 = arr.reshape(2,3) #2 rows and 3 column 
## rule:
# rows × columns must equal number of elements

print("Matrix 1:\n",matrix1,"\n")
matrix2 = arr.reshape(3,2)
print("Matrix 2: \n",matrix2,"\n")

##FLATTEN

flat = matrix1.flatten()
print("Flatten Matrix:",flat)

##RANDOM NO.
a1 = np.random.randint(1,100,10)
print("Randomely generated array:",a1,"\n")
matrix3 = np.random.randint(1,50,(3,3))
print("Randomely generated matrix :\n",matrix3)