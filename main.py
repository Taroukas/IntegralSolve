import sys
from PyQt6.QtWidgets import QApplication
from src.ui import IntegralSolveWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegralSolveWindow()
    window.show()
    sys.exit(app.exec())