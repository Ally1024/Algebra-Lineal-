# FalsaPosicion_tk_vfinal.py
import math
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# --- seguridad para eval ---
allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
allowed_names.update({"x": 0})  # placeholder

def parse_function(s):
    """Devuelve un callable f(x) a partir del string s. Reemplaza ^ por **."""
    s = s.replace("^", "**")
    def f(x):
        local = {"x": x}
        return eval(s, {"__builtins__": {}}, {**allowed_names, **local})
    return f

# --- Método de la falsa posición ---
def falsa_posicion(f, a, b, tol=1e-6, max_iter=100, min_iter=5):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    it = 0
    rows = []
    while it < max_iter:
        # Fórmula corregida según pizarra
        xr = b - (fb * (a - b)) / (fa - fb)
        fxr = f(xr)

        rows.append((it + 1, a, b, xr, fa, fb, fxr, abs(fxr)))

        if abs(fxr) <= tol and it + 1 >= min_iter:
            return xr, rows

        # Actualización correcta según signo
        if fa * fxr < 0:
            b = xr
            fb = fxr
        elif fa * fxr > 0:
            a = xr
            fa = fxr
        else:
            # Si fxr = 0 exactamente
            return xr, rows

        it += 1
    return xr, rows

# --- GUI ---
class App:
    def __init__(self, root):
        self.root = root
        root.title("Falsa Posición (Regula Falsi) — Gráfica y tabla")

        # Top frame: entrada
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Función f(x):").grid(row=0, column=0, sticky="w")
        self.entry_f = ttk.Entry(top, width=40)
        self.entry_f.grid(row=0, column=1, sticky="w")
        self.entry_f.insert(0, "x**3 + 4*x**2 - 10")  # ejemplo

        ttk.Button(top, text="Dibujar gráfica", command=self.draw_plot).grid(row=0, column=2, padx=6)
        ttk.Button(top, text="Limpiar selección", command=self.clear_selection).grid(row=0, column=3, padx=6)

        # Middle: canvas + controls
        mid = ttk.Frame(root, padding=6)
        mid.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(mid, bg="white", width=600, height=360)
        self.canvas.grid(row=0, column=0, rowspan=6, sticky="nsew")
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(0, weight=1)

        lbl_tol = ttk.Label(mid, text="Tolerancia (10^k):")
        lbl_tol.grid(row=0, column=1, sticky="w", padx=6)
        self.tol_scale = ttk.Scale(mid, from_=-1, to=-8, orient="vertical", command=self._update_tol_label)
        self.tol_scale.set(-6)
        self.tol_scale.grid(row=1, column=1, sticky="ns", padx=6, pady=4)
        self.tol_label = ttk.Label(mid, text="1e-6")
        self.tol_label.grid(row=2, column=1, sticky="n", padx=6)

        ttk.Button(mid, text="Ejecutar Falsa Posición", command=self.run_false_position).grid(row=3, column=1, padx=6, pady=8)

        # Right side: tabla y paso a paso
        right = ttk.Frame(root, padding=6)
        right.pack(fill="both", expand=False)
        ttk.Label(right, text="Tabla de iteraciones:").pack(anchor="w")
        cols = ("#","a","b","xr","f(a)","f(b)","f(xr)","|f(xr)|")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)
        ttk.Label(right, text="Paso a paso:").pack(anchor="w", pady=(6,0))
        self.steps = scrolledtext.ScrolledText(right, width=40, height=12)
        self.steps.pack(fill="both", expand=True)

        # estado de la gráfica y selección
        self.f = None
        self.x_min = -5
        self.x_max = 5
        self.y_min = -10
        self.y_max = 10
        self.root_approx = None

    # --- Utilidades ---
    def _update_tol_label(self, val):
        try:
            k = int(float(val))
        except:
            k = -6
        tol = 10 ** k
        self.tol_label.config(text=f"{tol:.0e}")

    def clear_selection(self):
        self.canvas.delete("all")
        self.tree.delete(*self.tree.get_children())
        self.steps.delete("1.0", tk.END)
        self.root_approx = None

    def safe_eval(self, x):
        try:
            y = self.f(x)
            if y is None or not math.isfinite(y):
                return None
            return y
        except Exception:
            return None

    # --- Dibujo ---
    def draw_plot(self):
        s = self.entry_f.get().strip()
        if not s:
            messagebox.showwarning("Entrada", "Ingresa una función en f(x).")
            return
        try:
            self.f = parse_function(s)

            # buscar automáticamente intervalo de cambio de signo
            interval = self.get_auto_interval()
            if interval:
                self.auto_a, self.auto_b = interval
            else:
                self.auto_a, self.auto_b = -5, 5

            # puntos para graficar
            xs = [self.auto_a + i*(self.auto_b-self.auto_a)/200 for i in range(201)]
            ys = [self.safe_eval(x) for x in xs]
            ys_valid = [y for y in ys if y is not None]
            if ys_valid:
                ymin, ymax = min(ys_valid), max(ys_valid)
                margin = (ymax - ymin) * 0.2 if ymax != ymin else 1
                self.x_min, self.x_max = min(xs), max(xs)
                self.y_min, self.y_max = ymin - margin, ymax + margin
            else:
                self.x_min, self.x_max = -5, 5
                self.y_min, self.y_max = -10, 10

            self._redraw(xs, ys)
        except Exception as e:
            messagebox.showerror("Error", f"Al parsear la función: {e}")

    def _redraw(self, xs, ys, show_root=True):
        self.canvas.delete("all")
        W, H = int(self.canvas["width"]), int(self.canvas["height"])
        def tx(x): return (x - self.x_min) / (self.x_max - self.x_min) * W
        def ty(y): return H - (y - self.y_min) / (self.y_max - self.y_min) * H

        # ejes
        if self.x_min < 0 < self.x_max:
            x0 = tx(0)
            self.canvas.create_line(x0, 0, x0, H, fill="black", width=2)
        if self.y_min < 0 < self.y_max:
            y0 = ty(0)
            self.canvas.create_line(0, y0, W, y0, fill="black", width=2)

        # curva azul
        prev = None
        for x,y in zip(xs, ys):
            if y is None:
                prev = None
                continue
            cx, cy = tx(x), ty(y)
            if prev:
                self.canvas.create_line(prev[0], prev[1], cx, cy, width=2, fill="blue")
            prev = (cx, cy)

        # textos: min/max X y Y
        self.canvas.create_text(10, 10, anchor="nw",
                                text=f"Valor mínimo X: {self.x_min:.3f}   Valor máximo X: {self.x_max:.3f}")
        self.canvas.create_text(10, 26, anchor="nw",
                                text=f"Valor mínimo Y: {self.y_min:.3f}   Valor máximo Y: {self.y_max:.3f}")
        # mostrar intervalo detectado automáticamente
        self.canvas.create_text(10, 42, anchor="nw",
                                text=f"Intervalo detectado: a={self.auto_a:.6f}, b={self.auto_b:.6f}")

        # dibujar raíz si ya existe
        if show_root and self.root_approx is not None:
            cx, cy = tx(self.root_approx), ty(self.safe_eval(self.root_approx))
            self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="green", outline="black", width=2, tags="root")
            self.canvas.create_text(cx+10, cy, text=f"xr≈{self.root_approx:.6f}", anchor="w", fill="green")

    # --- Ejecutar Falsa Posición ---
    def run_false_position(self):
        if not self.f:
            messagebox.showwarning("Función", "Primero dibuja la gráfica.")
            return

        a, b = self.auto_a, self.auto_b
        k = int(round(float(self.tol_scale.get())))
        tol = 10 ** k

        try:
            xr, rows = falsa_posicion(self.f, a, b, tol=tol, max_iter=100, min_iter=5)
            self.root_approx = xr
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # mostrar tabla y pasos
        self.tree.delete(*self.tree.get_children())
        self.steps.delete("1.0", tk.END)
        for r in rows:
            it, a_, b_, xr, fa, fb, fxr, abse = r
            self.tree.insert("", "end", values=(it, f"{a_:.6f}", f"{b_:.6f}", f"{xr:.6f}",
                                                f"{fa:.3e}", f"{fb:.3e}", f"{fxr:.3e}", f"{abse:.3e}"))
            self.steps.insert(tk.END, f"Iter {it}: a={a_:.6f}, b={b_:.6f}\n")
            self.steps.insert(tk.END, f"    xr = (a*f(b)-b*f(a))/(f(b)-f(a)) = {xr:.12f}\n")
            self.steps.insert(tk.END, f"    f(xr) = {fxr:.12e}, |f(xr)| = {abse:.12e}\n\n")

        self.steps.insert(tk.END, f"Raíz aproximada: {self.root_approx:.12f} (tolerancia {tol})\n")

        # redibujar para mostrar raíz
        xs = [self.x_min + i*(self.x_max-self.x_min)/200 for i in range(201)]
        ys = [self.safe_eval(x) for x in xs]
        self._redraw(xs, ys)

        messagebox.showinfo("Listo", f"Encontrada raíz aproximada: {self.root_approx:.12f}")

    def get_auto_interval(self, start=-20, end=20, step=0.1):
        x = start
        last_val = self.safe_eval(x)
        while x <= end:
            y = self.safe_eval(x)
            if y is not None and last_val is not None:
                if y * last_val < 0:
                    return x-step, x
            last_val = y
            x += step
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
