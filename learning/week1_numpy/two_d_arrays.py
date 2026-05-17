import numpy as np
matrix = np.array([
    [1,2,3],
    [4,5,6]
])
print("The matrix: ")
print(matrix)
print("No. of rows,columns: ",matrix.shape) #(row,column)

print("the element: ",matrix[0,0]) #matrix[row,column]

print("The 1 row: ",matrix[0]) #prints 1 row

print("The 2 column: ",matrix[:,1],"\n")
print("Changing elements now...")
matrix[0,1]=20
print("New matrix: ")
print(matrix,"\n")

print("'Exercise:'")
e_matrix = np.array([
 [10,20,30],
 [40,50,60]
])
print("the matrix: ")
print(e_matrix)
print("element: ",e_matrix[1,1])
print("The first row: ",e_matrix[0])
print("the second column: ",e_matrix[:,1])
