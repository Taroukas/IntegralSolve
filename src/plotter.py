import numpy as np
import sympy as sp


class IntegralPlotter:
    @staticmethod
    def apply_dark_theme(canvas):
        """Applies dark mode colors to the Matplotlib figure."""
        canvas.fig.patch.set_facecolor('#1e293b')
        canvas.axes.set_facecolor('#0f172a')
        canvas.axes.tick_params(colors='#e2e8f0', labelsize=9)
        canvas.axes.xaxis.label.set_color('#e2e8f0')
        canvas.axes.yaxis.label.set_color('#e2e8f0')
        canvas.axes.title.set_color('#f8fafc')
        for spine in canvas.axes.spines.values():
            spine.set_edgecolor('#475569')

    @staticmethod
    def _init_crosshair_artists(canvas):
        """Creates the crosshair lines, curve-snapping dot, and coordinate readout box."""
        canvas.vline = canvas.axes.axvline(0, color='#94a3b8', linestyle='--', linewidth=0.8, alpha=0.7, visible=False)
        canvas.hline = canvas.axes.axhline(0, color='#94a3b8', linestyle='--', linewidth=0.8, alpha=0.7, visible=False)
        canvas.curve_dot, = canvas.axes.plot([0], [0], marker='o', markersize=6, color='#f43f5e',
                                             markeredgecolor='white', visible=False, zorder=5)

        canvas.coord_text = canvas.axes.text(
            0.02, 0.95, "", transform=canvas.axes.transAxes,
            color='#f8fafc', fontsize=9, fontweight='bold', verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#475569', alpha=0.9),
            visible=False, zorder=6
        )

    @staticmethod
    def update_crosshair(canvas, x_mouse, y_mouse):
        """Updates the crosshair position and evaluates f(x) at the mouse X coordinate."""
        if not hasattr(canvas, 'vline') or canvas.vline is None:
            return

        if x_mouse is None or y_mouse is None:
            canvas.vline.set_visible(False)
            canvas.hline.set_visible(False)
            canvas.curve_dot.set_visible(False)
            canvas.coord_text.set_visible(False)
            canvas.draw_idle()
            return

        canvas.vline.set_xdata([x_mouse, x_mouse])
        canvas.hline.set_ydata([y_mouse, y_mouse])
        canvas.vline.set_visible(True)
        canvas.hline.set_visible(True)

        # Evaluate exact function value f(x_mouse) if a function is loaded
        if getattr(canvas, 'current_plot_data', None):
            f_np = canvas.current_plot_data['f_np']
            y_curve_arr = IntegralPlotter._safe_eval(f_np, np.array([x_mouse]))
            y_curve = float(y_curve_arr[0])

            if np.isfinite(y_curve):
                canvas.curve_dot.set_data([x_mouse], [y_curve])
                canvas.curve_dot.set_visible(True)
                canvas.coord_text.set_text(
                    f"Cursor: ({x_mouse:.4f}, {y_mouse:.4f})\n"
                    f"Curve:  f({x_mouse:.4f}) = {y_curve:.6f}"
                )
            else:
                canvas.curve_dot.set_visible(False)
                canvas.coord_text.set_text(
                    f"Cursor: ({x_mouse:.4f}, {y_mouse:.4f})\n"
                    f"Curve:  Undefined"
                )
        else:
            canvas.curve_dot.set_visible(False)
            canvas.coord_text.set_text(f"Cursor: ({x_mouse:.4f}, {y_mouse:.4f})")

        canvas.coord_text.set_visible(True)
        canvas.draw_idle()

    @staticmethod
    def init_empty_plot(canvas):
        """Displays an empty dark-mode plot at startup."""
        canvas.current_plot_data = None
        canvas.axes.clear()
        IntegralPlotter.apply_dark_theme(canvas)
        canvas.axes.set_title("Function Domain & Integrated Area", color='#f8fafc')
        canvas.axes.grid(True, linestyle=":", alpha=0.4, color='#64748b')
        IntegralPlotter._init_crosshair_artists(canvas)
        canvas.fig.tight_layout()
        canvas.draw()

    @staticmethod
    def _safe_eval(f_np, X):
        """Safely evaluates f(X) on arbitrary domains."""
        with np.errstate(all='ignore'):
            Y = f_np(X + 0j)
            if np.isscalar(Y):
                Y = np.full_like(X, float(np.real(Y)))
            else:
                Y = np.where(np.abs(np.imag(Y)) < 1e-9, np.real(Y), np.nan)
        return Y

    @staticmethod
    def update_dynamic_view(canvas, num_points=1000):
        """Re-generates the curve and shaded area for the current visible [xmin, xmax] window."""
        if not getattr(canvas, 'current_plot_data', None):
            return

        data = canvas.current_plot_data
        f_np = data['f_np']
        is_indefinite = data['is_indefinite']
        a_val = data['a_val']
        b_val = data['b_val']

        cur_xlim = canvas.axes.get_xlim()
        cur_ylim = canvas.axes.get_ylim()

        X = np.linspace(cur_xlim[0], cur_xlim[1], num_points)
        Y = IntegralPlotter._safe_eval(f_np, X)

        canvas.axes.clear()
        IntegralPlotter.apply_dark_theme(canvas)

        canvas.axes.plot(X, Y, color="#38bdf8", linewidth=2, label="f(x)")

        if not is_indefinite:
            fill_min = max(cur_xlim[0], a_val)
            fill_max = min(cur_xlim[1], b_val)
            if fill_max > fill_min:
                X_fill = np.linspace(fill_min, fill_max, 600)
                Y_fill = IntegralPlotter._safe_eval(f_np, X_fill)
                canvas.axes.fill_between(X_fill, Y_fill, color="#0284c7", alpha=0.4, label="Integrated Area")

        canvas.axes.axhline(0, color="#64748b", linewidth=1, linestyle="--")
        canvas.axes.axvline(0, color="#64748b", linewidth=0.8, linestyle=":")
        canvas.axes.grid(True, linestyle=":", alpha=0.4, color='#64748b')

        legend = canvas.axes.legend(loc="upper right", frameon=True)
        legend.get_frame().set_facecolor('#1e293b')
        legend.get_frame().set_edgecolor('#475569')
        for text in legend.get_texts():
            text.set_color('#f8fafc')

        title = "Function Curve (Indefinite)" if is_indefinite else "Function Domain & Integrated Area"
        canvas.axes.set_title(title, color='#f8fafc')

        # Re-initialize crosshair overlay after clearing axes
        IntegralPlotter._init_crosshair_artists(canvas)

        canvas.axes.set_xlim(cur_xlim)
        canvas.axes.set_ylim(cur_ylim)
        canvas.draw_idle()

    @staticmethod
    def plot_function_only(canvas, f, x, num_points=1000):
        f_np = sp.lambdify(x, f, "numpy")
        canvas.current_plot_data = {
            'f_np': f_np,
            'is_indefinite': True,
            'a_val': None,
            'b_val': None
        }

        X = np.linspace(-5.0, 5.0, num_points)
        Y = IntegralPlotter._safe_eval(f_np, X)
        valid_Y = Y[np.isfinite(Y)]
        y_min = float(np.min(valid_Y)) if len(valid_Y) > 0 else -5.0
        y_max = float(np.max(valid_Y)) if len(valid_Y) > 0 else 5.0
        pad = max((y_max - y_min) * 0.15, 1.0)

        canvas.axes.set_xlim(-5.0, 5.0)
        canvas.axes.set_ylim(y_min - pad, y_max + pad)
        IntegralPlotter.update_dynamic_view(canvas, num_points)

    @staticmethod
    def plot_integral(canvas, f, x, a, b, num_points=1000):
        f_np = sp.lambdify(x, f, "numpy")
        a_val = -np.inf if a == -sp.oo else (np.inf if a == sp.oo else float(a))
        b_val = np.inf if b == sp.oo else (-np.inf if b == -sp.oo else float(b))
        if a_val > b_val:
            a_val, b_val = b_val, a_val

        canvas.current_plot_data = {
            'f_np': f_np,
            'is_indefinite': False,
            'a_val': a_val,
            'b_val': b_val
        }

        view_min = -5.0 if np.isinf(a_val) else float(a_val) - 1.5
        view_max = 5.0 if np.isinf(b_val) else float(b_val) + 1.5
        if view_max <= view_min:
            view_min, view_max = -5.0, 5.0

        X = np.linspace(view_min, view_max, num_points)
        Y = IntegralPlotter._safe_eval(f_np, X)
        valid_Y = Y[np.isfinite(Y)]
        y_min = float(np.min(valid_Y)) if len(valid_Y) > 0 else -5.0
        y_max = float(np.max(valid_Y)) if len(valid_Y) > 0 else 5.0
        pad = max((y_max - y_min) * 0.15, 1.0)

        canvas.axes.set_xlim(view_min, view_max)
        canvas.axes.set_ylim(min(0.0, y_min) - pad, max(0.0, y_max) + pad)
        IntegralPlotter.update_dynamic_view(canvas, num_points)
