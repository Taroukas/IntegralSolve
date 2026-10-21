import streamlit as st
import sympy as sp
import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="IntegralSolve — Advanced Calculus Engine",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, professional aesthetic (avoiding default AI look)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.title("∫ IntegralSolve")
st.markdown("##### High-Precision Symbolic & Numerical Integration Engine")
st.divider()

# Sidebar - Configuration and Presets
with st.sidebar:
    st.header("Control Panel")

    preset = st.selectbox(
        "Load Example Integrals",
        [
            "Custom Expression",
            "Gaussian Integral: exp(-x**2)",
            "Damped Oscillator: exp(-x**2) * cos(3*x)",
            "Singular Endpoint: ln(x) / sqrt(x)",
            "Fresnel Integral: sin(x**2)",
            "Dirichlet Sinc: sin(x) / x"
        ]
    )

    # Default parameters based on preset
    def_expr, def_a, def_b = "exp(-x**2) * cos(2*x)", "0", "oo"
    if "Gaussian" in preset:
        def_expr, def_a, def_b = "exp(-x**2)", "-oo", "oo"
    elif "Singular" in preset:
        def_expr, def_a, def_b = "ln(x) / sqrt(x)", "0", "1"
    elif "Fresnel" in preset:
        def_expr, def_a, def_b = "sin(x**2)", "0", "5"
    elif "Dirichlet" in preset:
        def_expr, def_a, def_b = "sin(x) / x", "0", "oo"

    st.divider()
    precision = st.slider("Numerical Precision (Digits)", min_value=15, max_value=100, value=30)
    plot_points = st.slider("Plot Resolution (Points)", min_value=100, max_value=2000, value=600, step=100)

# Main input layout
st.markdown("### Expression Parameters")
col_input1, col_input2, col_input3, col_input4 = st.columns([3, 1, 1, 1])

with col_input1:
    expr_str = st.text_input("Integrand f(x)", value=def_expr)
with col_input2:
    var_str = st.text_input("Variable", value="x")
with col_input3:
    a_str = st.text_input("Lower Bound (empty = indefinite)", value=def_a)
with col_input4:
    b_str = st.text_input("Upper Bound ('oo' = ∞)", value=def_b)

st.markdown("")
run_calculation = st.button("Evaluate Integral", type="primary")

# Execution and Render
if run_calculation:
    try:
        x = sp.Symbol(var_str)
        f = sp.sympify(expr_str)

        # CASE 1: Indefinite Integral (Antiderivative)
        if not a_str.strip() or not b_str.strip():
            st.markdown("### 1. Mathematical Formulation")
            st.latex(r"\int " + sp.latex(f) + r"\, d" + var_str)

            with st.spinner("Computing symbolic antiderivative..."):
                primitive = sp.integrate(f, x)

            st.markdown("### 2. Analytical Solution")
            if not primitive.has(sp.Integral):
                st.success("Exact antiderivative successfully derived.")
                st.latex(sp.latex(primitive) + " + C")
            else:
                st.warning(
                    "No closed-form analytical antiderivative found in terms of elementary or standard special functions.")

        # CASE 2: Definite Integral
        else:
            a, b = sp.sympify(a_str), sp.sympify(b_str)

            st.markdown("### 1. Mathematical Formulation")
            st.latex(
                r"\int_{" + sp.latex(a) + r"}^{" + sp.latex(b) + r"} \left(" + sp.latex(f) + r"\right) d" + var_str)

            res_col, plot_col = st.columns([1, 1], gap="large")

            with res_col:
                st.markdown("### 2. Solver Output")
                with st.spinner("Executing symbolic reduction & numerical quadrature..."):
                    sol_exacte = sp.integrate(f, (x, a, b))

                if not sol_exacte.has(sp.Integral):
                    st.success("Exact analytical solution found")
                    st.latex(sp.latex(sol_exacte))
                    mp.dps = precision
                    val_num = sol_exacte.evalf(precision)
                    method_used = "Symbolic Evaluation (Exact)"
                else:
                    st.info("No closed-form solution — Switched to adaptive high-precision quadrature (Tanh-Sinh)")
                    mp.dps = precision
                    f_mp = sp.lambdify(x, f, "mpmath")
                    a_mp = mp.inf if a == sp.oo else (-mp.inf if a == -sp.oo else float(a))
                    b_mp = mp.inf if b == sp.oo else (-mp.inf if b == -sp.oo else float(b))
                    val_num = mp.quad(f_mp, [a_mp, b_mp])
                    method_used = "High-Precision Numerical Quadrature"

                st.markdown(f"**Method:** `{method_used}`")
                st.markdown("**Numerical Value:**")
                st.code(str(val_num), language="text")

            with plot_col:
                st.markdown("### 3. Visual Domain Analysis")
                f_np = sp.lambdify(x, f, "numpy")
                x_min = -5.0 if a == -sp.oo else (float(a) + 1e-4 if a == 0 else float(a))
                x_max = 5.0 if b == sp.oo else float(b)

                X = np.linspace(x_min, x_max, plot_points)
                Y = np.real(f_np(X))

                fig, ax = plt.subplots(figsize=(6, 4.2))
                ax.plot(X, Y, color="#0284c7", linewidth=2, label=f"$f({var_str})$")
                ax.fill_between(X, Y, color="#38bdf8", alpha=0.3, label="Integrated Area")
                ax.axhline(0, color="#64748b", linewidth=0.8, linestyle="--")
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.grid(True, linestyle=":", alpha=0.6)
                ax.legend(frameon=True, facecolor="white", edgecolor="none")
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Computation or parsing error: {e}")