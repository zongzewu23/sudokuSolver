# gui/sudoku_gui.py

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QMessageBox, QLabel
)
from solver.sudokuSolver import SudokuSolver
import sys
import os

class SudokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI layout and widgets."""
        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(600, 700)

        # Apply stylesheet
        style_path = os.path.join(os.path.dirname(__file__), '../resources/style.qss')
        with open(style_path, 'r') as f:
            self.setStyleSheet(f.read())

        # Create grid layout
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        self.cells = [[QLineEdit(self) for _ in range(9)] for _ in range(9)]

        # Configure cells
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                cell.setFixedSize(50, 50)
                cell.setAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(QtGui.QFont("Arial", 20))
                # Set background color for 3x3 subgrids
                if (row // 3 + col // 3) % 2 == 0:
                    cell.setStyleSheet("background-color: #F0F0F0;")
                else:
                    cell.setStyleSheet("background-color: #FFFFFF;")
                # Set input mask to accept only digits 1-9
                cell.setValidator(QtGui.QIntValidator(1,9))
                grid.addWidget(cell, row, col)

        # Solve button
        solve_btn = QPushButton("Solve", self)
        solve_btn.setFixedSize(100, 40)
        solve_btn.clicked.connect(self.solve_puzzle)
        grid.addWidget(solve_btn, 9, 0, 1, 4)

        # Clear button
        clear_btn = QPushButton("Clear", self)
        clear_btn.setFixedSize(100, 40)
        clear_btn.clicked.connect(self.clear_puzzle)
        grid.addWidget(clear_btn, 9, 5, 1, 4)

        # Instruction Label
        instruction = QLabel("Enter numbers (1-9) and click 'Solve'", self)
        instruction.setAlignment(QtCore.Qt.AlignCenter)
        instruction.setFont(QtGui.QFont("Arial", 12))
        grid.addWidget(instruction, 10, 0, 1, 9)

    def get_puzzle(self):
        """
        Retrieve the puzzle from the GUI cells.
        :return: 2D list representing the Sudoku puzzle or None if invalid input
        """
        puzzle = []
        for row in range(9):
            current_row = []
            for col in range(9):
                text = self.cells[row][col].text()
                if text == '':
                    current_row.append(0)
                else:
                    try:
                        num = int(text)
                        if 1 <= num <= 9:
                            current_row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        QMessageBox.critical(
                            self, "Input Error",
                            f"Invalid input at row {row+1}, column {col+1}. Please enter digits 1-9."
                        )
                        return None
            puzzle.append(current_row)
        return puzzle

    def set_board(self, board):
        """
        Set the GUI cells based on the solved board.
        :param board: 2D list representing the solved Sudoku puzzle
        """
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    self.cells[row][col].setText(str(num))
                    self.cells[row][col].setStyleSheet("background-color: #D1FFD1;")
                else:
                    self.cells[row][col].setText('')
                    # Reset to original background
                    if (row // 3 + col // 3) % 2 == 0:
                        self.cells[row][col].setStyleSheet("background-color: #F0F0F0;")
                    else:
                        self.cells[row][col].setStyleSheet("background-color: #FFFFFF;")

    def solve_puzzle(self):
        """Handle the solve button click."""
        puzzle = self.get_puzzle()
        if puzzle is None:
            return  # Invalid input encountered

        solver = SudokuSolver(puzzle)
        if solver.solve():
            solved_board = solver.get_board()
            self.set_board(solved_board)
            QMessageBox.information(self, "Success", "Sudoku Solved Successfully!")
        else:
            QMessageBox.warning(self, "No Solution", "This Sudoku puzzle has no solution.")

    def clear_puzzle(self):
        """Clear all cells in the GUI."""
        for row in range(9):
            for col in range(9):
                self.cells[row][col].clear()
                # Reset to original background
                if (row // 3 + col // 3) % 2 == 0:
                    self.cells[row][col].setStyleSheet("background-color: #F0F0F0;")
                else:
                    self.cells[row][col].setStyleSheet("background-color: #FFFFFF;")
