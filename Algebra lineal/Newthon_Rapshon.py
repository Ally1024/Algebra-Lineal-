import math 
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# --- seguridad para eval ---
allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
allowed_names.update({"x": 0})

def parse_function(s):
    s = s.replace("^", "**")
    def f(x):
        return eval(s, {"__builtins__": {}}, {**allowed_names, "x": x})
    return f

# ===============================================================
#                MÉTODO NEWTON-RAPHSON
# ===============================================================
def newton_raphson(f, df, x0, tol=1e-6, max_iter=50):
    rows = []
    x = x0

    for it in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if dfx == 0:
            raise ValueError("La derivada se volvió cero. No se puede dividir.")

        x_new = x - fx / dfx
        error = abs(x_new - x)

        rows.append((it, x, fx, dfx, x_new, error))

        if error <= tol:
            return x_new, rows

        x = x_new

    return x, rows

# ===============================================================
#                GUI COMPLETA
# ===============================================================
class AppNewton:
    def __init__(self, root):
        self.root = root
        root.title("Newton–Raphson — Interfaz Completa")

        # ------- Entrada -------
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="f(x):").grid(row=0, column=0)
        self.entry_f = ttk.Entry(top, width=40)
        self.entry_f.grid(row=0, column=1)
        self.entry_f.insert(0, "x**3 + 4*x**2 - 10")

        ttk.Label(top, text="f'(x):").grid(row=1, column=0)
        self.entry_df = ttk.Entry(top, width=40)
        self.entry_df.grid(row=1, column=1)
        self.entry_df.insert(0, "3*x**2 + 8*x")

        ttk.Label(top, text="x0").grid(row=2, column=0)
        self.entry_x0 = ttk.Entry(top, width=20)
        self.entry_x0.grid(row=2, column=1, sticky="w")
        ttk.Button(top, text="Dibujar gráfica", command=self.draw_plot).grid(row=0, column=2, padx=6)
        ttk.Button(top, text="Limpiar", command=self.clear_all).grid(row=1, column=2, padx=6)

        # ------- Canvas -------
        mid = ttk.Frame(root, padding=6)
        mid.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(mid, bg="white", width=600, height=360)
        self.canvas.grid(row=0, column=0, rowspan=6)

        # ------- Tolerancia -------
        ttk.Label(mid, text="Tolerancia 10^k").grid(row=0, column=1)
        self.tol_scale = ttk.Scale(mid, from_=-1, to=-8, orient="vertical",
                                   command=self._update_tol_label)
        self.tol_scale.set(-6)
        self.tol_scale.grid(row=1, column=1, sticky="ns")

        self.tol_label = ttk.Label(mid, text="1e-6")
        self.tol_label.grid(row=2, column=1)

        ttk.Button(mid, text="Ejecutar Newton-Raphson",
                   command=self.run_newton).grid(row=3, column=1, pady=10)

        # ------- Tabla -------
        right = ttk.Frame(root, padding=6)
        right.pack(fill="both")

        ttk.Label(right, text="Tabla de iteraciones:").pack(anchor="w")
        cols = ("#", "xi", "f(xi)", "f'(xi)", "xi+1", "Error")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        ttk.Label(right, text="Paso a paso:").pack(anchor="w")
        self.steps = scrolledtext.ScrolledText(right, width=50, height=12)
        self.steps.pack(fill="both", expand=True)

        # estado gráfico
        self.f = None
        self.df = None
        self.x_min = -5
        self.x_max = 5
        self.y_min = -10
        self.y_max = 10
        self.root_approx = None

    # =======================
    # UTILS
    # =======================
    def _update_tol_label(self, val):
        k = int(float(val))
        self.tol_label.config(text=f"1e{k}")

    def clear_all(self):
        self.canvas.delete("all")
        self.tree.delete(*self.tree.get_children())
        self.steps.delete("1.0", tk.END)
        self.root_approx = None

    def set_exercise(self, fx, dfx, x0):
        self.entry_f.delete(0, tk.END)
        self.entry_f.insert(0, fx)
        self.entry_df.delete(0, tk.END)
        self.entry_df.insert(0, dfx)
        self.entry_x0.delete(0, tk.END)
        self.entry_x0.insert(0, x0)

    # =======================
    # GRAFICACIÓN
    # =======================
    def safe_eval(self, fn, x):
        try:
            y = fn(x)
            if y is None or not math.isfinite(y):
                return None
            return y
        except:
            return None

    def draw_plot(self):
        try:
            self.f = parse_function(self.entry_f.get())
            self.df = parse_function(self.entry_df.get())
        except:
            messagebox.showerror("Error", "Error interpretando funciones.")
            return

        xs = [i/10 for i in range(-100, 101)]
        ys = [self.safe_eval(self.f, x) for x in xs]
        ys_ok = [v for v in ys if v is not None]

        if ys_ok:
            ymin, ymax = min(ys_ok), max(ys_ok)
            margin = (ymax - ymin)*0.2 if ymax != ymin else 1
            self.x_min, self.x_max = xs[0], xs[-1]
            self.y_min, self.y_max = ymin - margin, ymax + margin

        self._redraw(xs, ys)

    def _redraw(self, xs, ys):
        self.canvas.delete("all")
        W = int(self.canvas["width"])
        H = int(self.canvas["height"])

        def tx(x): return (x - self.x_min) / (self.x_max - self.x_min) * W
        def ty(y): return H - (y - self.y_min) / (self.y_max - self.y_min) * H

        # ejes
        if self.x_min < 0 < self.x_max:
            x0 = tx(0)
            self.canvas.create_line(x0, 0, x0, H, width=2)
        if self.y_min < 0 < self.y_max:
            y0 = ty(0)
            self.canvas.create_line(0, y0, W, y0, width=2)

        # curva
        prev = None
        for x, y in zip(xs, ys):
            if y is None:
                prev = None
                continue
            cx, cy = tx(x), ty(y)
            if prev:
                self.canvas.create_line(prev[0], prev[1], cx, cy, fill="blue", width=2)
            prev = (cx, cy)

        # punto aproximado con texto
        if self.root_approx is not None:
            cx = tx(self.root_approx)
            cy = ty(self.f(self.root_approx))
            self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="green")
            self.canvas.create_text(cx + 50, cy - 10, text=f"Punto aproximado:\n{self.root_approx:.6f}", fill="green", font=("Arial", 10, "bold"))

    # =======================
    # NEWTON-RAPHSON COMPLETO
    # =======================
    def run_newton(self):
        if not self.f or not self.df:
            messagebox.showwarning("Función", "Primero dibuja la gráfica.")
            return

        # tolerancia
        k = int(float(self.tol_scale.get()))
        tol = 10**k

        # punto inicial
        txt = self.entry_x0.get().strip()
        if txt == "":
            x0 = 0
        else:
            try:
                x0 = float(txt)
            except:
                messagebox.showerror("Error", "x0 inválido.")
                return

        try:
            xr, rows = newton_raphson(self.f, self.df, x0, tol=tol)
            self.root_approx = xr
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # limpieza
        self.tree.delete(*self.tree.get_children())
        self.steps.delete("1.0", tk.END)

        # llenar tabla y pasos
        for it, xi, fx, dfx, xn, err in rows:
            self.tree.insert("", "end", values=(
                it, f"{xi:.6f}", f"{fx:.3e}", f"{dfx:.3e}",
                f"{xn:.6f}", f"{err:.3e}"
            ))

            self.steps.insert(tk.END, f"Iteración {it}:\n")
            self.steps.insert(tk.END, f"  xi       = {xi:.12f}\n")
            self.steps.insert(tk.END, f"  f(xi)    = {fx:.12e}\n")
            self.steps.insert(tk.END, f"  f'(xi)   = {dfx:.12e}\n")
            self.steps.insert(tk.END, f"  xi+1     = {xn:.12f}\n")
            self.steps.insert(tk.END, f"  Error    = {err:.12e}\n\n")

        # datos finales
        final_fx = self.f(self.root_approx)
        last_error = rows[-1][5]
        total_iter = rows[-1][0]

        self.steps.insert(tk.END, "----------------------------------------\n")
        self.steps.insert(tk.END, f"RAÍZ APROXIMADA:\n  x = {self.root_approx:.12f}\n\n")
        self.steps.insert(tk.END, f"TOTAL DE ITERACIONES: {total_iter}\n")
        self.steps.insert(tk.END, f"ERROR DE CONVERGENCIA FINAL: {last_error:.12e}\n\n")
        self.steps.insert(tk.END, f"VERIFICACIÓN FINAL:\n  f(x) = {final_fx:.12e}\n")
        self.steps.insert(tk.END, "----------------------------------------\n")

        # actualizar gráfica
        xs = [i/10 for i in range(-100, 101)]
        ys = [self.safe_eval(self.f, x) for x in xs]
        self._redraw(xs, ys)

        messagebox.showinfo(
            "Cálculo completo",
            f"Raíz encontrada: {self.root_approx:.12f}\n"
            f"Iteraciones: {total_iter}\n"
            f"Error final: {last_error:.3e}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    AppNewton(root)
    root.mainloop()
