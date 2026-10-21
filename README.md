# IntegralSolve ∫

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/PyQt6-6.6%2B-41cd52.svg)](https://pypi.org/project/PyQt6/)
[![Symbolic Math](https://img.shields.io/badge/SymPy-1.12%2B-3B5526.svg)](https://www.sympy.org/)
[![Numerical Engine](https://img.shields.io/badge/mpmath-1.3%2B-orange.svg)](https://mpmath.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A modular, high-precision symbolic and numerical integration desktop application built with Python and PyQt6.**  
*Combines exact algebraic antiderivative derivation with adaptive Tanh-Sinh quadrature and native dark-mode domain visualization.*

</div>

---

## ✨ Key Features

* **Hybrid Mathematical Engine (`src/engine.py`):**
  * **Indefinite Integrals (Primitives):** Derives exact closed-form analytical antiderivatives ($F(x) + C$) using Risch integration algorithms and special functions via `SymPy`.
  * **Exact Definite Evaluation:** Computes exact symbolic representations over finite or infinite intervals before evaluating floating-point approximations.
  * **High-Precision Numerical Quadrature (`mpmath`):** Automatically falls back to adaptive Tanh-Sinh quadrature (25+ significant digits) when an integrand lacks a closed-form elementary primitive, effortlessly handling endpoint singularities and improper bounds ($\pm\infty$).
* **Wolfram-Style Native Desktop GUI (`src/ui.py`):**
  * **Interactive Math Keypad:** Built-in clickable keypad for inserting true mathematical symbols (`²`, `√`, `π`, `∞`, `·`, `^`) and transcendental functions (`exp`, `sin`, `cos`, `tan`, `ln`) with transparent background translation to Python syntax.
  * **Smart Bound Selectors:** Dedicated dropdown controls for lower and upper bounds supporting **Custom Values**, **$\pm\infty$**, and **No Bound (Indefinite / Primitive mode)**.
  * **Curated Presets:** Instant loading for classic mathematical benchmarks including Gaussian integrals, damped oscillators, singular logarithmic endpoints, Fresnel integrals, and Dirichlet sinc functions.
* **Dark-Mode Visual Domain Analysis (`src/plotter.py`):**
  * Embedded `Matplotlib` QtAgg canvas styled natively in dark mode from startup.
  * Dynamically plots function curves for indefinite primitives and shades integrated areas under the curve for definite integrals.

---

## 🗂️ Project Architecture

The application follows a strict separation of concerns, dividing mathematical computation, visualization, and user interface logic into dedicated modules:

```text
IntegralSolve/
├── src/
│   ├── __init__.py      # Package initialization
│   ├── engine.py        # Core symbolic (SymPy) & numerical (mpmath) solver
│   ├── plotter.py       # Dark-mode Matplotlib canvas & domain shading logic
│   └── ui.py            # PyQt6 desktop window, math keypad & event handlers
├── main.py              # Application entry point
├── dependencies.txt     # Required Python packages
└── README.md            # Project documentation
```

---

## ⚙️ Installation Guide

Follow these steps to set up and run **IntegralSolve** locally on your machine.

### Prerequisites
Make sure you have **Python 3.12+** and **Git** installed on your system.

### 1. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone [https://github.com/Taroukas/IntegralSolve.git](https://github.com/Taroukas/IntegralSolve.git)
cd IntegralSolve
```

### 2. Create a Virtual Environment (Recommended)
* **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Ensure your `dependencies.txt` contains `PyQt6`, `sympy`, `mpmath`, `numpy`, and `matplotlib`, then run:
```bash
pip install -r dependencies.txt
```

### 4. Launch the Desktop Application
Run the main entry point script:
```bash
python main.py
```

---

## 🖥️ Usage Guide

1. **Enter an Integrand:** Type your function directly into the **Integrand $f(x)$** field or use the **Math Keypad** to insert powers (`x²`, `xʸ`), roots (`√x`), constants (`π`), and functions (`exp(`, `sin(`, `ln(`).
2. **Select Integration Mode:**
   * **Definite Integral:** Set **Lower Bound (a)** and **Upper Bound (b)** to `Custom` (e.g., `0` to `5`, or `0` to `π`) or `±∞`.
   * **Indefinite Integral (Primitive):** Set either bound dropdown to `No Bound (Indefinite)` to compute the symbolic antiderivative $F(x) + C$.
3. **Evaluate:** Click **Evaluate Integral** to view the computation method, exact analytical expression, high-precision numerical value, and real-time dark-mode plot.

---

## 🧮 Supported Mathematical Syntax

Thanks to the built-in parser in `src/ui.py`, you can mix natural mathematical symbols and standard Python syntax seamlessly:

| Mathematical Concept | Accepted Input in UI | Internal Engine Translation |
| :--- | :--- | :--- |
| **Square / Power** | `x²` or `x^4` | `x**2`, `x**4` |
| **Square Root** | `√(x)` or `sqrt(x)` | `sqrt(x)` |
| **Multiplication** | `2 · x` or `2 * x` | `2 * x` |
| **Exponential** | `exp(-x²)` | `exp(-x**2)` |
| **Pi & Infinity** | `π`, `-∞`, `+∞` | `pi`, `-oo`, `oo` |
| **Trigonometric & Log** | `sin(x)`, `cos(x)`, `tan(x)`, `ln(x)` | `sin(x)`, `cos(x)`, `tan(x)`, `ln(x)` |

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-capability`).
3. Commit your changes (`git commit -m "Add new capability"`).
4. Push to the branch (`git push origin feature/new-capability`) and open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
