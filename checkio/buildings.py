def istall(matrix):
    max_element = max(x[4] for x in matrix)
    return [row for row in matrix if row[4] == max_element] 

def issouth(matrix):
    min_element = min(x[1] for x in matrix)
    return [row for row in matrix if row[1] == min_element] 

def reltall(matrix, selected_submatrix):
    return [row for row in matrix if row in selected_submatrix]

x = [[1, 1, 11, 2, 2], [2, 1, 10, 4, 1], [3, 2, 9, 6, 3], [4, 7, 8, 8, 2]]
print istall(x) # [[3, 2, 9, 6, 3]]
print issouth(x) # [[1, 1, 11, 2, 2], [2, 1, 10, 4, 1]]
print reltall(x, istall(x)) # [[3, 2, 9, 6, 3]]
print reltall(x, issouth(x)) # [[1, 1, 11, 2, 2], [2, 1, 10, 4, 1]]
