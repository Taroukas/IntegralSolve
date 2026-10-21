import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QComboBox, QSplitter
)
from PyQt6.QtCore import Qt

import matplotlib

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.engine import IntegralEngine
from src.plotter import IntegralPlotter


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class IntegralSolveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IntegralSolve — Wolfram-Style Desktop Edition")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # --- LEFT PANEL: Controls & Math Keypad ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        # Presets Group
        preset_group = QGroupBox("Quick Presets")
        preset_layout = QVBoxLayout()
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Gaussian Integral: exp(-x²)",
            "Damped Oscillator: exp(-x²) · cos(3x)",
            "Singular Endpoint: ln(x) / √x",
            "Fresnel Integral: sin(x²)",
            "Dirichlet Sinc: sin(x) / x"
        ])
        self.preset_combo.currentIndexChanged.connect(self.load_preset)
        preset_layout.addWidget(self.preset_combo)
        preset_group.setLayout(preset_layout)
        left_layout.addWidget(preset_group)

        # Inputs Group
        input_group = QGroupBox("Integral Parameters")
        input_layout = QGridLayout()

        input_layout.addWidget(QLabel("Integrand f(x):"), 0, 0)
        self.input_expr = QLineEdit("exp(-x²)")
        input_layout.addWidget(self.input_expr, 0, 1, 1, 3)

        input_layout.addWidget(QLabel("Variable:"), 1, 0)
        self.input_var = QLineEdit("x")
        input_layout.addWidget(self.input_var, 1, 1, 1, 3)

        # Lower Bound Controls
        input_layout.addWidget(QLabel("Lower Bound (a):"), 2, 0)
        self.bound_a_combo = QComboBox()
        self.bound_a_combo.addItems(["Custom", "-∞ (-oo)", "No Bound (Indefinite)"])
        self.bound_a_combo.currentIndexChanged.connect(self.toggle_bound_a)
        input_layout.addWidget(self.bound_a_combo, 2, 1)

        self.input_a_custom = QLineEdit("-∞")
        input_layout.addWidget(self.input_a_custom, 2, 2, 1, 2)

        # Upper Bound Controls
        input_layout.addWidget(QLabel("Upper Bound (b):"), 3, 0)
        self.bound_b_combo = QComboBox()
        self.bound_b_combo.addItems(["Custom", "+∞ (oo)", "No Bound (Indefinite)"])
        self.bound_b_combo.currentIndexChanged.connect(self.toggle_bound_b)
        input_layout.addWidget(self.bound_b_combo, 3, 1)

        self.input_b_custom = QLineEdit("+∞")
        input_layout.addWidget(self.input_b_custom, 3, 2, 1, 2)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        # --- MATH KEYPAD (Wolfram Style Buttons) ---
        keypad_group = QGroupBox("Math Keypad (Click to insert)")
        keypad_layout = QGridLayout()

        buttons = [
            ("x²", "²"), ("√x", "√("), ("π", "π"), ("exp", "exp("),
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("ln", "ln("),
            ("+", " + "), ("-", " - "), ("·", " · "), ("/", " / "),
            ("(", "("), (")", ")"), ("xʸ", "^"), ("∞", "∞")
        ]

        row, col = 0, 0
        for label, snippet in buttons:
            btn = QPushButton(label)
            btn.setStyleSheet("background-color: #334155; color: white; font-weight: bold; padding: 6px;")
            btn.clicked.connect(lambda checked, s=snippet: self.insert_symbol(s))
            keypad_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        keypad_group.setLayout(keypad_layout)
        left_layout.addWidget(keypad_group)

        # Solve Button
        self.btn_solve = QPushButton("Evaluate Integral")
        self.btn_solve.setStyleSheet(
            "background-color: #0284c7; color: white; font-weight: bold; padding: 10px; font-size: 14px;")
        self.btn_solve.clicked.connect(self.solve_integral)
        left_layout.addWidget(self.btn_solve)

        # Output Box
        output_group = QGroupBox("Solver Output")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        left_layout.addWidget(output_group)

        splitter.addWidget(left_container)

        # --- RIGHT PANEL: Graph ---
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        right_layout.addWidget(self.canvas)

        IntegralPlotter.init_empty_plot(self.canvas)

        splitter.addWidget(right_container)
        splitter.setSizes([500, 700])

        self.load_preset()

    def insert_symbol(self, snippet):
        self.input_expr.insert(snippet)
        self.input_expr.setFocus()

    def format_for_sympy(self, text):
        """Convertit les symboles de l'interface en syntaxe compréhensible par SymPy."""
        python_code = text.replace("²", "**2").replace("³", "**3")
        python_code = python_code.replace("^", "**")
        python_code = python_code.replace("√", "sqrt")
        python_code = python_code.replace("π", "pi")
        python_code = python_code.replace("·", "*")
        python_code = python_code.replace("∞", "oo")
        return python_code

    def format_bound_for_sympy(self, text):
        text = text.replace("−", "-").replace("+", "").strip()
        if "∞" in text or "oo" in text:
            return "-oo" if text.startswith("-") else "oo"
        return text

    def toggle_bound_a(self):
        idx = self.bound_a_combo.currentIndex()
        if idx == 0:
            self.input_a_custom.setEnabled(True)
            self.input_a_custom.setText("0")
        elif idx == 1:
            self.input_a_custom.setEnabled(False)
            self.input_a_custom.setText("-∞")
        else:
            self.input_a_custom.setEnabled(False)
            self.input_a_custom.setText("")

    def toggle_bound_b(self):
        idx = self.bound_b_combo.currentIndex()
        if idx == 0:
            self.input_b_custom.setEnabled(True)
            self.input_b_custom.setText("1")
        elif idx == 1:
            self.input_b_custom.setEnabled(False)
            self.input_b_custom.setText("+∞")
        else:
            self.input_b_custom.setEnabled(False)
            self.input_b_custom.setText("")

    def load_preset(self):
        idx = self.preset_combo.currentIndex()
        if idx == 0:
            self.input_expr.setText("exp(-x²)")
            self.bound_a_combo.setCurrentIndex(1)
            self.bound_b_combo.setCurrentIndex(1)
        elif idx == 1:
            self.input_expr.setText("exp(-x²) · cos(3*x)")
            self.bound_a_combo.setCurrentIndex(0)
            self.input_a_custom.setText("0")
            self.bound_b_combo.setCurrentIndex(1)
        elif idx == 2:
            self.input_expr.setText("ln(x) / √x")
            self.bound_a_combo.setCurrentIndex(0)
            self.input_a_custom.setText("0")
            self.bound_b_combo.setCurrentIndex(0)
            self.input_b_custom.setText("1")
        elif idx == 3:
            self.input_expr.setText("sin(x²)")
            self.bound_a_combo.setCurrentIndex(0)
            self.input_a_custom.setText("0")
            self.bound_b_combo.setCurrentIndex(0)
            self.input_b_custom.setText("5")
        elif idx == 4:
            self.input_expr.setText("sin(x) / x")
            self.bound_a_combo.setCurrentIndex(0)
            self.input_a_custom.setText("0")
            self.bound_b_combo.setCurrentIndex(1)

    def solve_integral(self):
        try:
            raw_expr = self.input_expr.text().strip()
            sympy_expr = self.format_for_sympy(raw_expr)

            raw_a = self.input_a_custom.text().strip()
            sympy_a = self.format_bound_for_sympy(raw_a)

            raw_b = self.input_b_custom.text().strip()
            sympy_b = self.format_bound_for_sympy(raw_b)

            res = IntegralEngine.evaluate(
                sympy_expr,
                self.input_var.text().strip(),
                sympy_a,
                sympy_b
            )

            if res["is_indefinite"]:
                report = (
                    f"<b>Status:</b> Success<br>"
                    f"<b>Type:</b> Indefinite Integral (Antiderivative / Primitive)<br>"
                    f"<b>Method:</b> {res['method']}<br>"
                    f"<b>Primitive:</b> {res['analytical']}"
                )
                self.output_text.setHtml(report)
                IntegralPlotter.plot_function_only(self.canvas, res['sympy_expr'], res['symbol_var'])
            else:
                report = (
                    f"<b>Status:</b> Success<br>"
                    f"<b>Type:</b> Definite Integral<br>"
                    f"<b>Method:</b> {res['method']}<br>"
                    f"<b>Analytical Result:</b> {res['analytical']}<br>"
                    f"<b>Numerical Value:</b> {res['numerical']:.12f}"
                )
                self.output_text.setHtml(report)
                IntegralPlotter.plot_integral(
                    self.canvas, res['sympy_expr'], res['symbol_var'],
                    res['bounds'][0], res['bounds'][1]
                )

        except Exception as e:
            self.output_text.setHtml(f"<b style='color: red;'>Error:</b> {str(e)}")