import sympy as sp
import mpmath as mp


class IntegralEngine:
    @staticmethod
    def evaluate(expr_str, var_str, a_str, b_str, precision=25):
        x = sp.Symbol(var_str)
        f = sp.sympify(expr_str)

        # CAS 1 : Si les bornes sont vides -> Calcul de la primitive (intégrale indéfinie)
        if not a_str.strip() or not b_str.strip():
            primitive = sp.integrate(f, x)
            if not primitive.has(sp.Integral):
                analytical_str = str(primitive) + " + C"
                method = "Symbolic Antiderivative (Exact)"
            else:
                analytical_str = "No closed-form antiderivative found."
                method = "Failed"
            return {
                "is_indefinite": True,
                "method": method,
                "analytical": analytical_str,
                "numerical": None,
                "sympy_expr": f,
                "symbol_var": x
            }

        # CAS 2 : Intégrale définie avec bornes
        a = sp.sympify(a_str)
        b = sp.sympify(b_str)
        sol_exacte = sp.integrate(f, (x, a, b))

        if not sol_exacte.has(sp.Integral):
            method = "Symbolic Evaluation (Exact)"
            val_num = float(sol_exacte.evalf())
            result_display = str(sol_exacte)
        else:
            method = "High-Precision Numerical Quadrature (Tanh-Sinh)"
            mp.dps = precision
            f_mp = sp.lambdify(x, f, "mpmath")
            a_mp = mp.inf if a == sp.oo else (-mp.inf if a == -sp.oo else float(a))
            b_mp = mp.inf if b == sp.oo else (-mp.inf if b == -sp.oo else float(b))
            val_num = float(mp.quad(f_mp, [a_mp, b_mp]))
            result_display = "No closed-form expression"

        return {
            "is_indefinite": False,
            "method": method,
            "analytical": result_display,
            "numerical": val_num,
            "sympy_expr": f,
            "symbol_var": x,
            "bounds": (a, b)
        }