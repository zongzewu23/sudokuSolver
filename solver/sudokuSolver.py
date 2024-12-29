import numpy as np

class SudokuSolver:
    def __init__(self, board):
        """
        Initialize the Sudoku board.
        :param board: 2D list or NumPy array representing the Sudoku puzzle
        """
        self.board = np.array(board)

    def is_valid(self, num, row, col):
        """
        Check if placing `num` in `board[row][col]` is valid.
        :param num: Number to place (1-9)
        :param row: Row index
        :param col: Column index
        :return: True if valid, False otherwise
        """
        # Check row
        if num in self.board[row, :]:
            return False
        # Check column
        if num in self.board[:, col]:
            return False
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.board[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

    def solve(self):
        """
        Solve the Sudoku puzzle using backtracking.
        :return: True if solvable, False otherwise
        """
        # Find the first empty cell
        empty = np.where(self.board == 0)
        if len(empty[0]) == 0:  # No empty cell left, puzzle is solved
            return True
        row, col = empty[0][0], empty[1][0]

        for num in range(1, 10):  # Try numbers 1-9
            if self.is_valid(num, row, col):
                self.board[row, col] = num  # Place number
                if self.solve():  # Recursively try to solve the rest
                    return True
                self.board[row, col] = 0  # Undo placement (backtrack)
        return False

    def get_board(self):
        """Return the current state of the Sudoku board."""
        return self.board.tolist()

    def print_board(self):
        """Print the Sudoku board."""
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))