echo "# IntegralSolve ∫

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/PyQt6-6.6%2B-41cd52.svg)](https://pypi.org/project/PyQt6/)
[![Symbolic Math](https://img.shields.io/badge/SymPy-1.12%2B-3B5526.svg)](https://www.sympy.org/)
[![Numerical Engine](https://img.shields.io/badge/mpmath-1.3%2B-orange.svg)](https://mpmath.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A modular, high-precision symbolic and numerical integration desktop application built with Python and PyQt6.**  
*Combines exact algebraic antiderivative derivation with adaptive Tanh-Sinh quadrature, infinite dynamic plotting, and interactive mouse controls.*

</div>

---

##  Key Features

* **Hybrid Mathematical Engine (\`src/engine.py\`):**
  * **Indefinite Integrals (Primitives):** Derives exact closed-form analytical antiderivatives (\$F(x) + C\$) using Risch integration algorithms and special functions via \`SymPy\`.
  * **Exact Definite Evaluation:** Computes exact symbolic representations over finite or infinite intervals before evaluating floating-point approximations.
  * **High-Precision Numerical Quadrature (\`mpmath\`):** Automatically falls back to adaptive Tanh-Sinh quadrature (25+ significant digits) when an integrand lacks a closed-form elementary primitive, effortlessly handling endpoint singularities and improper bounds (\$\\pm\\infty\$).
* **Wolfram-Style Native Desktop GUI (\`src/ui.py\`):**
  * **Interactive Math Keypad:** Built-in clickable keypad for inserting true mathematical symbols (\`²\`, \`√\`, \`π\`, \`∞\`, \`·\`, \`^\`) and transcendental functions (\`exp\`, \`sin\`, \`cos\`, \`tan\`, \`ln\`).
  * **Smart Bound Selectors:** Dedicated dropdown controls for lower and upper bounds supporting **Custom Values**, **\$\\pm\\infty\$**, and **No Bound (Indefinite / Primitive mode)**.
  * **Curated Presets:** Instant loading for classic mathematical benchmarks including Gaussian integrals, damped oscillators, singular logarithmic endpoints, Fresnel integrals, and Dirichlet sinc functions.
* **Interactive Dark-Mode Visualizer (\`src/plotter.py\` & \`src/ui.py\`):**
  * Embedded \`Matplotlib\` QtAgg canvas styled natively in dark mode from startup.
  * **Infinite Dynamic Resampling:** Automatically re-samples and recalculates points across the visible domain in real time as you pan or zoom.
  * **Live Mouse Controls:** Mouse wheel zoom centered on the cursor, left-click drag panning, and a real-time crosshair with coordinate inspection and curve-snapping.

---

##  Project Architecture

The application follows a strict separation of concerns, dividing mathematical computation, visualization, and user interface logic into dedicated modules:

\`\`\`text
IntegralSolve/
├── src/
│   ├── __init__.py      # Package initialization
│   ├── engine.py        # Core symbolic (SymPy) & numerical (mpmath) solver
│   ├── plotter.py       # Dark-mode Matplotlib canvas & dynamic resampling logic
│   └── ui.py            # PyQt6 desktop window, math keypad & event handlers
├── main.py              # Application entry point
├── dependencies.txt     # Required Python packages
└── README.md            # Project documentation
\`\`\`

---

##  Dependencies (\`dependencies.txt\`)

\`\`\`text
PyQt6>=6.6.0
sympy>=1.12
mpmath>=1.3.0
numpy>=1.26.0
matplotlib>=3.8.0
pyinstaller>=6.0.0
\`\`\`

---

##  Installation & Execution Guide

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/Taroukas/IntegralSolve.git
cd IntegralSolve
\`\`\`

### 2. Create a Virtual Environment (Recommended)
* **Windows:**
  \`\`\`bash
  python -m venv venv
  venv\\Scripts\\activate
  \`\`\`
* **macOS / Linux:**
  \`\`\`bash
  python3 -m venv venv
  source venv/bin/activate
  \`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r dependencies.txt
\`\`\`

### 4. Run from Source
\`\`\`bash
python main.py
\`\`\`

---

##  Building a Standalone Windows Executable (\`.exe\`)

\`\`\`bash
pyinstaller --noconsole --onedir main.py
\`\`\`
*Your compiled executable will be located inside the \`dist/main/\` folder (\`main.exe\`).*

---

##  Usage Guide

1. **Enter an Integrand:** Type your function directly into the **Integrand \$f(x)\$** field or use the **Math Keypad** to insert powers (\`²\`, \`xʸ\`), roots (\`√x\`), constants (\`π\`), and functions (\`exp(\`, \`sin(\`, \`ln(\`).
2. **Select Integration Mode:**
   * **Definite Integral:** Set **Lower Bound (a)** and **Upper Bound (b)** to \`Custom\` or \$\\pm\\infty\$.
   * **Indefinite Integral (Primitive):** Set either bound dropdown to \`No Bound (Indefinite)\` to compute the symbolic antiderivative \$F(x) + C\$.
3. **Evaluate & Interact:** Click **Evaluate Integral** to view the analytical expression, numerical value, and plot. Use your **mouse wheel** to zoom, **click and drag** to pan, and **hover** to inspect exact coordinates via the live crosshair.

---

##  License

This project is open-source and available under the [MIT License](LICENSE)." > README.md
