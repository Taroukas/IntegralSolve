import numpy as np
import sympy as sp


class IntegralPlotter:
    @staticmethod
    def apply_dark_theme(canvas):
        """Applique les couleurs du mode sombre à la figure Matplotlib."""
        canvas.fig.patch.set_facecolor('#1e293b')
        canvas.axes.set_facecolor('#0f172a')
        canvas.axes.tick_params(colors='#e2e8f0', labelsize=9)
        canvas.axes.xaxis.label.set_color('#e2e8f0')
        canvas.axes.yaxis.label.set_color('#e2e8f0')
        canvas.axes.title.set_color('#f8fafc')
        for spine in canvas.axes.spines.values():
            spine.set_edgecolor('#475569')

    @staticmethod
    def init_empty_plot(canvas):
        """Affiche un graphique vide mais stylisé en dark mode au démarrage."""
        canvas.axes.clear()
        IntegralPlotter.apply_dark_theme(canvas)
        canvas.axes.set_title("Function Domain & Integrated Area", color='#f8fafc')
        canvas.axes.grid(True, linestyle=":", alpha=0.4, color='#64748b')
        canvas.fig.tight_layout()
        canvas.draw()

    @staticmethod
    def plot_function_only(canvas, f, x, num_points=600):
        """Trace uniquement f(x) pour les primitives (sans aire)."""
        f_np = sp.lambdify(x, f, "numpy")
        X = np.linspace(-5.0, 5.0, num_points)
        Y = np.real(f_np(X))

        canvas.axes.clear()
        IntegralPlotter.apply_dark_theme(canvas)

        canvas.axes.plot(X, Y, color="#38bdf8", linewidth=2, label="f(x)")
        canvas.axes.axhline(0, color="#64748b", linewidth=1, linestyle="--")
        canvas.axes.grid(True, linestyle=":", alpha=0.4, color='#64748b')

        legend = canvas.axes.legend(loc="upper right", frameon=True)
        legend.get_frame().set_facecolor('#1e293b')
        legend.get_frame().set_edgecolor('#475569')
        for text in legend.get_texts():
            text.set_color('#f8fafc')

        canvas.axes.set_title("Function Curve (Indefinite)")
        canvas.fig.tight_layout()
        canvas.draw()

    @staticmethod
    def plot_integral(canvas, f, x, a, b, num_points=600):
        """Trace la fonction et l'aire sous la courbe en dark mode."""
        f_np = sp.lambdify(x, f, "numpy")
        x_min = -5.0 if a == -sp.oo else (float(a) + 1e-4 if a == 0 else float(a))
        x_max = 5.0 if b == sp.oo else float(b)

        X = np.linspace(x_min, x_max, num_points)
        Y = np.real(f_np(X))

        canvas.axes.clear()
        IntegralPlotter.apply_dark_theme(canvas)

        canvas.axes.plot(X, Y, color="#38bdf8", linewidth=2, label="f(x)")
        canvas.axes.fill_between(X, Y, color="#0284c7", alpha=0.4, label="Integrated Area")
        canvas.axes.axhline(0, color="#64748b", linewidth=1, linestyle="--")
        canvas.axes.grid(True, linestyle=":", alpha=0.4, color='#64748b')

        legend = canvas.axes.legend(loc="upper right", frameon=True)
        legend.get_frame().set_facecolor('#1e293b')
        legend.get_frame().set_edgecolor('#475569')
        for text in legend.get_texts():
            text.set_color('#f8fafc')

        canvas.axes.set_title("Function Domain & Integrated Area")
        canvas.fig.tight_layout()
        canvas.draw()