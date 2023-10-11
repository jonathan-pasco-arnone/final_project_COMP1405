""" Matrix methods program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: September 2023


import math

def mult_scalar(matrix, scale):
    """ Multiplies the matrix by a scalar """
    new_matrix = []
    row = 0
    for row_values in matrix:
        new_matrix.append([])
        for value in row_values:
            (new_matrix[row]).append(scale * value)
        row += 1
    return new_matrix

def mult_matrix(a, b):
    """ Finds the DOT product of two matrices """
    # Check the matrices are compatible
    compatible = False
    for row in a:
        if len(row) == len(b):
            compatible = True

    # Calculate the DOT product if the matrices are compatible
    if compatible:
        new_matrix = []
        row_index_a = 0
        # Collects each row of a
        for row_a in a:
            new_matrix.append([])

            # Cycles through each column of b
            column_index_b = 0
            while column_index_b != len(b[0]):

                # Goes through each value of the rows of b
                column_index_a = 0
                new_value = 0
                for row_b in b:
                    # Adds each value of row A multiplied by each value of column B
                    new_value += row_a[column_index_a] * row_b[column_index_b]
                    column_index_a += 1
                (new_matrix[row_index_a]).append(new_value)
                
                column_index_b += 1
            row_index_a += 1
        return new_matrix
    else:
        return "None"
    
def euclidean_dist(a,b):
    sum_under_root = 0
    # The 0's are because each vector is within another list conatining only itself
    # ex: [[5,3,7]] 
    # Unnecessary extra brackets
    for index in range(len(a[0])):
        sum_under_root += (a[0][index] - b[0][index]) ** 2
    final_sum = math.sqrt(sum_under_root)
    return final_sum