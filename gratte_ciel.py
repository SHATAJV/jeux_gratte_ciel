
import random

"""jeux plus genere 
"""


# Function to check visible buildings in a row or column
def height_visibility(building_height):
    maximum = 0
    nb_visible = 0
    for height in building_height:
        if height > maximum:
            maximum = height
            nb_visible += 1
    return nb_visible


# Function to validate if a number can be placed in a cell without repeating in its row and column
def validation_cells(answermatrix, row, column, num):
    size = len(answermatrix)
    for i in range(size):
        if answermatrix[row][i] == num or answermatrix[i][column] == num:
            return False
    return True


# Function to check if the current matrix meets the visibility limits
def check_limitation(answermatrix, limit):
    size = len(answermatrix)
    for i in range(size):
        if 0 < limit['left'][i] != height_visibility(answermatrix[i]):
            return False

        if 0 < limit['right'][i] != height_visibility(answermatrix[i][::-1]):
            return False

        col = [answermatrix[j][i] for j in range(size)]
        if 0 < limit['top'][i] != height_visibility(col):
            return False

        if 0 < limit['bottom'][i] != height_visibility(col[::-1]):
            return False

    return True


# Function to solve the game
def solve_game(limit, answermatrix):
    n = len(answermatrix)
    stack = [(0, 0, 1)]  # (row, column, number to try)

    while stack:
        row, column, num = stack.pop()

        if column == n:
            row += 1
            column = 0

        if row == n:
            if check_limitation(answermatrix, limit):
                return True
            continue

        if answermatrix[row][column] == 0:
            for n in range(num, n + 1):
                if validation_cells(answermatrix, row, column, n):
                    answermatrix[row][column] = n
                    stack.append((row, column + 1, 1))
                    break
            else:
                answermatrix[row][column] = 0
                if stack:
                    stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1)
        else:
            stack.append((row, column + 1, 1))

    return answermatrix


# Function to print the matrix
def print_index(answermatrix, limitation):
    top, bottom, left, right = limitation['top'], limitation['bottom'], limitation['left'], limitation['right']
    n = len(answermatrix)
    print("   " + "  ".join(map(str, top)))
    print(" " + "_____" * n)
    for i in range(n):
        print(f"{left[i]} | {' | '.join(map(str, answermatrix[i]))} | {right[i]}")
        print(" " + "_____" * n)
    print("   " + "  ".join(map(str, bottom)))


def Duplicate(size):
    base = list(range(1, size + 1))
    matrix = []
    for i in range(size):
        row = base[i:] + base[:i]
        matrix.append(row)

    # Transpose the matrix to ensure no duplicates in columns
    transposed = list(map(list, zip(*matrix)))
    for row in transposed:
        random.shuffle(row)

    # Transpose back to get the final Latin Square
    final_matrix = list(map(list, zip(*matrix)))
    return final_matrix


# Initialize size and answer matrix
size = int(input("Enter size of table (enter a number between 4-8): "))

# Generate random Latin Square matrix for the user
user_matrix = Duplicate(size)
print("Generated random matrix:")
for row in user_matrix:
    print(" ".join(map(str, row)))

# Get user input for the limits
limitation = {
    'top': list(map(int, input(f"Enter top limits (space-separated, {size} values): ").split())),
    'bottom': list(map(int, input(f"Enter bottom limits (space-separated, {size} values): ").split())),
    'left': list(map(int, input(f"Enter left limits (space-separated, {size} values): ").split())),
    'right': list(map(int, input(f"Enter right limits (space-separated, {size} values): ").split()))
}

# Get user input for the solution matrix
print("Enter your solution matrix row by row (each number separated by space):")
user_solution = [[0] * size for _ in range(size)]
for i in range(size):
    user_solution[i] = list(map(int, input().split()))

# Check if the user's matrix meets the limitations
if check_limitation(user_solution, limitation):
    print("Congratulations! Your solution is correct.")
else:
    print("Sorry, your solution is incorrect. Here is the correct solution:")
    answer_matrix = [[0] * size for _ in range(size)]
    if solve_game(limitation, answer_matrix):
        print_index(answer_matrix, limitation)
    else:
        print("Error: No solution found.")

