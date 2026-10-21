import sympy as sp
import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt


def resoudre_et_tracer(expr_str, a_str, b_str):
    x = sp.Symbol('x')
    f = sp.sympify(expr_str)
    a, b = sp.sympify(a_str), sp.sympify(b_str)

    print(f"\n--- Analyse de l'intégrale de {expr_str} entre {a} et {b} ---")

    # 1. Tentative de calcul exact (Symbolique)
    res_exact = sp.integrate(f, (x, a, b))
    if not res_exact.has(sp.Integral):
        print(f"Résultat exact (formule) : {res_exact}")
        print(f"Résultat exact (LaTeX)   : {sp.latex(res_exact)}")
        val_num = float(res_exact.evalf())
    else:
        # 2. Bascule automatique en haute précision si pas de primitive
        print("Aucune primitive simple trouvée. Passage au calcul haute précision...")
        mp.dps = 25
        f_mp = sp.lambdify(x, f, 'mpmath')
        a_mp = mp.inf if a == sp.oo else (-mp.inf if a == -sp.oo else float(a))
        b_mp = mp.inf if b == sp.oo else (-mp.inf if b == -sp.oo else float(b))
        val_num = float(mp.quad(f_mp, [a_mp, b_mp]))

    print(f"Valeur numérique         : {val_num:.10f}")

    # 3. Tracé graphique de la fonction et de l'aire
    f_np = sp.lambdify(x, f, 'numpy')
    x_min = -5 if a == -sp.oo else float(a)
    x_max = 5 if b == sp.oo else float(b)

    X = np.linspace(x_min, x_max, 500)
    Y = f_np(X)

    plt.figure(figsize=(8, 4.5))
    plt.plot(X, Y, label=f"$f(x) = {sp.latex(f)}$", color="royalblue", linewidth=2)
    plt.fill_between(X, Y, color="skyblue", alpha=0.4, label=f"Aire $\\approx {val_num:.5f}$")
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Résolution et visualisation de l'intégrale")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


if __name__ == "__main__":
    # Test avec une intégrale difficile sans primitive élémentaire
    resoudre_et_tracer("exp(-x**2) * cos(2*x)", "0", "oo")