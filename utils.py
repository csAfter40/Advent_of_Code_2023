def print_matrix(matrix):
    """
    Prints a given 2d array on console without commas and brackets.
    """
    for row in matrix:
        print(*row, sep="")
