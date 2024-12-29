# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.sudokuGUI import SudokuGUI

def main():
    """Main function to start the Sudoku Solver GUI."""
    app = QApplication(sys.argv)
    gui = SudokuGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
