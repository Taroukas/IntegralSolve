# IntegralSolve ∫

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-ff4b4b.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A high-precision symbolic and numerical integration engine built with Python and Streamlit.**  
*Combines exact algebraic derivations with robust adaptive quadrature for complex and singular calculus problems.*

</div>

---

## 🚀 Key Features

* **Hybrid Architecture Engine:**
  * **Symbolic Evaluation (`SymPy`):** Attempts exact closed-form analytical derivation using Risch algorithms and special functions.
  * **High-Precision Numerical Quadrature (`mpmath`):** Automatically switches to adaptive Tanh-Sinh quadrature when no elementary antiderivative exists, handling infinite bounds and difficult endpoint singularities with up to 100 digits of precision.
* **Interactive Web UI (`Streamlit`):** Clean, modern research-grade interface with real-time LaTeX formula rendering.
* **Visual Domain Analysis (`Matplotlib`):** Instant plotting of integrand functions with dynamically shaded integrated areas.
* **Built-in Advanced Presets:** Ready-to-test configurations including Gaussian integrals, damped oscillators, singular endpoints, Fresnel integrals, and Dirichlet sinc functions.

---

## 🛠️ Project Structure

```text
IntegralSolve/
├── app.py              # Main Streamlit web application & solver pipeline
├── dependencies.txt    # Required Python packages
└── README.md           # Project documentation
