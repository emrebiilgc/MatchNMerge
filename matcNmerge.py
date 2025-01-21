import sys

sys.setrecursionlimit(1000000)


def check(board):
    row = len(board)
    col = len(board[0])
    score = 0
    print_board(board, row, col, score)
    print()
    the_game(board, row, col, score)


def the_game(board, row, col, score):
    chosen_row_col = input("Please enter a row and a column number: ")
    crow, ccol = map(int, chosen_row_col.split())  # choosen row = crow and choosen col = ccol
    while crow > row or ccol > col or crow <= 0 or ccol <= 0:
        print()
        print("Please enter a correct size!")
        print()
        chosen_row_col = input("Please enter a row and a column number: ")
        print()
        crow, ccol = map(int, chosen_row_col.split())
    score = check_cells(board, crow - 1, ccol - 1, score)
    print_board(board, row, col, score)
    print()
    result = find_equal_neighbors_all(board, row, col)
    if len(result) == 0:
        print("Game Over")
    else:
        the_game(board, row, col, score)


def check_cells(board, row, col, score):
    def replace_connected_cells(row, col, number, score):
        replaced_cells = set()

        if has_same_number_neighbor(row, col, number):
            # The set of replaced cells should be updated with the result of the recursive function
            replaced_cells.update(search_and_replace(row, col, number))
            print()
        else:
            print()
            print("No movement happened, try again")
            print()
        # The updated score is calculated based on the number of replaced cells and their values.
        return len(replaced_cells) * number + score
    # A recursive function is to be employed for searching and replacing connected cells with the same number.
    def search_and_replace(row, col, number):
        replaced_cells = set()
        # Check if the current cell has the same number
        if board[row][col] != number:
            return replaced_cells
        # The current cell is to be replaced with an empty space and added to the set of replaced cells.
        board[row][col] = ' '
        replaced_cells.add((row, col))
        # Neighboring cells with the same number are to be recursively searched and replaced.
        for i, j in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= i < len(board) and 0 <= j < len(board[i]):
                replaced_cells.update(search_and_replace(i, j, number))
        return replaced_cells

    def has_same_number_neighbor(row, col, number):
        for i, j in [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]:
            if 0 <= i < len(board) and 0 <= j < len(board[i]) and board[i][j] == number:
                return True
        return False

    def shift_numbers_down_and_left(board):
        for col in range(len(board[0])):
            # The column values are to be extracted.
            column_values = [board[row][col] for row in range(len(board))]

            # Empty spaces are to be removed.
            column_values = [value for value in column_values if value != ' ']

            # Empty spaces are to be added to the top of the column to match the original height.
            column_values = [' '] * (len(board) - len(column_values)) + column_values

            # The board is to be updated with the modified column.
            for row in range(len(board)):
                board[row][col] = column_values[row]

        # Empty columns are to be checked for, and columns are to be shifted to the left.
        for col in reversed(range(len(board[0]))):
            # These operations will be performed on the column.

            if all(board[row][col] == ' ' for row in range(len(board))):
                # Columns are to be shifted to the left.
                for c in range(col, len(board[0]) - 1):
                    for row in range(len(board)):
                        board[row][c] = board[row][c + 1]

                # The last column is to be cleared with ''.
                for row in range(len(board)):
                    board[row][-1] = ' '

        # It is to be checked whether the top row is empty, and if so, it is to be removed.
        if all(board[0][col] == ' ' for col in range(len(board[0]))):
            board.pop(0)
            # A new row is to be added at the bottom with ''.
            board.append([' '] * len(board[0]))

    score = replace_connected_cells(row, col, board[row][col], score)
    shift_numbers_down_and_left(board)  # board is edited
    return score


def find_equal_neighbors_all(board, row, col):  # It is checked if there is a neighboring cell.
    equal_neighbors = []

    for i in range(row):
        for j in range(col):
            value = board[i][j]

            if value in ('', ' ', None):
                continue

            neighbors_indices = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]

            has_equal_neighbor = any(
                0 <= ccrow < row and 0 <= ccol < col and board[ccrow][ccol] == value
                for ccrow, ccol in neighbors_indices if
                0 <= ccrow < row and 0 <= ccol < col and board[ccrow][ccol] not in ('', ' ', None)
            )
            if has_equal_neighbor:
                equal_neighbors.append(value)

    return equal_neighbors


def print_board(board, row, col, score):
    for i in range(row):
        if all(board[i][j] in ('', ' ', None) for j in range(col)):
            continue  # Empty line is passed

        row_str = ""
        for j in range(col):
            row_str += str(board[i][j]) + " "
        print(row_str[:-1])
    print()
    print("Your score is: ", score)


def matrix(input_line):
    return [int(number) for number in input_line.strip() if number.isdigit()]


def main():
    input_file = open(sys.argv[1], "r")
    board = [matrix(line) for line in input_file.readlines()]
    check(board)


if __name__ == '__main__':
    main()
