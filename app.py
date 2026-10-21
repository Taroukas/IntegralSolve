import streamlit as st
import sympy as sp
import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la fenêtre
st.set_page_config(page_title="IntegralSolve", page_icon="∫", layout="wide")

st.title("∫ IntegralSolve — Solveur d'Intégrales Hybride")
st.markdown("Résolution **symbolique exacte** (`SymPy`) et **numérique haute précision** (`mpmath`).")

# Barre latérale avec des exemples prêts à tester
with st.sidebar:
    st.header("Exemples complexes")
    exemple = st.selectbox(
        "Charger une intégrale type :",
        [
            "Personnalisée",
            "Gaussienne : exp(-x**2)",
            "Oscillante amortie : exp(-x**2) * cos(3*x)",
            "Singularité : ln(x) / sqrt(x)",
            "Fresnel : sin(x**2)",
            "Sinc sur R+ : sin(x) / x"
        ]
    )

    # Valeurs par défaut selon l'exemple choisi
    def_expr, def_a, def_b = "exp(-x**2) * cos(2*x)", "0", "oo"
    if "Gaussienne" in exemple:
        def_expr, def_a, def_b = "exp(-x**2)", "-oo", "oo"
    elif "Singularité" in exemple:
        def_expr, def_a, def_b = "ln(x) / sqrt(x)", "0", "1"
    elif "Fresnel" in exemple:
        def_expr, def_a, def_b = "sin(x**2)", "0", "5"
    elif "Sinc" in exemple:
        def_expr, def_a, def_b = "sin(x) / x", "0", "oo"

    st.divider()
    precision = st.slider("Précision numérique (décimales)", min_value=15, max_value=100, value=30)

# Zone de saisie principale
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

with col1:
    expr_str = st.text_input("Fonction f(x) :", value=def_expr)
with col2:
    var_str = st.text_input("Variable :", value="x")
with col3:
    a_str = st.text_input("Borne inf (vide = primitive) :", value=def_a)
with col4:
    b_str = st.text_input("Borne sup ('oo' = ∞) :", value=def_b)

# Analyse et calcul
if st.button("Résoudre l'intégrale", type="primary"):
    try:
        x = sp.Symbol(var_str)
        f = sp.sympify(expr_str)

        # CAS 1 : Intégrale indéfinie (recherche de primitive)
        if not a_str.strip() or not b_str.strip():
            st.subheader("1. Équation analysée")
            st.latex(r"\int " + sp.latex(f) + r"\, d" + var_str)

            with st.spinner("Recherche d'une primitive exacte..."):
                primitive = sp.integrate(f, x)

            st.subheader("2. Résultat symbolique")
            if not primitive.has(sp.Integral):
                st.success("Primitive exacte trouvée !")
                st.latex(sp.latex(primitive) + " + C")
            else:
                st.warning("Aucune primitive exprimable avec les fonctions élémentaires ou spéciales connues.")

        # CAS 2 : Intégrale définie (avec bornes)
        else:
            a, b = sp.sympify(a_str), sp.sympify(b_str)
            st.subheader("1. Équation analysée")
            st.latex(
                r"\int_{" + sp.latex(a) + r"}^{" + sp.latex(b) + r"} \left(" + sp.latex(f) + r"\right) d" + var_str)

            res_col, plot_col = st.columns([1, 1])

            with res_col:
                st.subheader("2. Résolution Mathématique")
                with st.spinner("Calcul formel en cours..."):
                    sol_exacte = sp.integrate(f, (x, a, b))

                if not sol_exacte.has(sp.Integral):
                    st.success("Formule exacte trouvée (Moteur Symbolique)")
                    st.latex(sp.latex(sol_exacte))
                    mp.dps = precision
                    val_num = sol_exacte.evalf(precision)
                else:
                    st.info("Pas de forme fermée simple — Bascule sur le moteur haute précision (Tanh-Sinh)")
                    mp.dps = precision
                    f_mp = sp.lambdify(x, f, "mpmath")
                    a_mp = mp.inf if a == sp.oo else (-mp.inf if a == -sp.oo else float(a))
                    b_mp = mp.inf if b == sp.oo else (-mp.inf if b == -sp.oo else float(b))
                    val_num = mp.quad(f_mp, [a_mp, b_mp])

                st.markdown("**Évaluation numérique haute précision :**")
                st.code(str(val_num), language="text")

            with plot_col:
                st.subheader("3. Visualisation de l'aire")
                f_np = sp.lambdify(x, f, "numpy")
                x_min = -5.0 if a == -sp.oo else (float(a) + 1e-4 if a == 0 else float(a))
                x_max = 5.0 if b == sp.oo else float(b)

                X = np.linspace(x_min, x_max, 600)
                Y = np.real(f_np(X))

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(X, Y, color="#2563eb", linewidth=2, label=f"$f({var_str})$")
                ax.fill_between(X, Y, color="#60a5fa", alpha=0.35, label="Aire intégrée")
                ax.axhline(0, color="black", linewidth=0.8)
                ax.grid(True, linestyle="--", alpha=0.5)
                ax.legend()
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur d'analyse ou de domaine mathématique : {e}")