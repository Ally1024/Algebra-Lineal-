import math
import webbrowser
import tempfile
import numpy as np

# Funciones permitidas
allowed_names = {
    "cos": math.cos,
    "sin": math.sin,
    "tan": math.tan,
    "log": math.log,  # ln
    "exp": math.exp,
    "sqrt": math.sqrt,
}

def clean_expression(expr):
    expr = expr.replace("=0", "").strip()
    expr = expr.replace("^", "**")
    return expr

def get_function_from_input():
    expr = input("Ingresa la ecuación f(x) = 0: ")
    expr = clean_expression(expr)
    def f(x):
        local_dict = allowed_names.copy()
        local_dict["x"] = x
        return eval(expr, {"__builtins__": {}}, local_dict)
    return f, expr

def plot_with_geogebra(f_expr):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>GeoGebra Plot</title>
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    </head>
    <body>
        <div id="ggb-element" style="width: 800px; height: 600px;"></div>
        <script>
            var ggbApp = new GGBApplet({{
                "appName": "graphing",
                "width": 800,
                "height": 600,
                "showToolBar": true,
                "showAlgebraInput": true,
                "showMenuBar": true,
                "appletOnLoad": function() {{
                    ggbApp.evalCommand("f(x) = {f_expr}");
                }}
            }}, true);
            window.onload = function() {{ ggbApp.inject('ggb-element'); }};
        </script>
    </body>
    </html>
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_file.write(html_content.encode("utf-8"))
    tmp_file.close()
    webbrowser.open(f"file://{tmp_file.name}")

def find_interval(f, x_min=-10, x_max=10, steps=1000):
    xs = np.linspace(x_min, x_max, steps)
    prev = f(xs[0])
    for x in xs[1:]:
        curr = f(x)
        if prev * curr <= 0:  # Cambio de signo
            return xs[np.where(xs==prev)[0][0]], x
        prev = curr
    raise ValueError("No se encontró un cambio de signo en el rango dado.")

def bisection(f, a, b, tol=1e-4, max_iter=100):
    pasos = []

    fa = f(a)
    fb = f(b)
    for it in range(1, max_iter+1):
        c = (a + b)/2
        fc = f(c)

        pasos.append({
            "iter": it, "a": a, "b": b, "c": c, "fa": fa, "fc": fc, "fb": fb
        })

        print(f"\nPaso {it}: c = ({a} + {b})/2 = {c}")
        print(f"f(c) = {fc}")

        if abs(fc) < tol or (b-a)/2 < tol:
            break

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print("\nTabla de iteraciones:")
    print("Iter |     a      |     b      |     c      |   f(a)     |   f(c)     |   f(b)")
    print("-----+------------+------------+------------+------------+------------+------------")
    for paso in pasos:
        print(f"{paso['iter']:4d} | {paso['a']:10.6f} | {paso['b']:10.6f} | {paso['c']:10.6f} | {paso['fa']:10.6f} | {paso['fc']:10.6f} | {paso['fb']:10.6f}")

    return c, fc, it

if __name__ == "__main__":
    f, f_expr = get_function_from_input()

    print("Mostrando gráfica en GeoGebra...")
    plot_with_geogebra(f_expr)

    print("Buscando automáticamente un intervalo con cambio de signo...")
    try:
        a, b = find_interval(f, x_min=-10, x_max=10)
        print(f"Intervalo encontrado automáticamente: [{a:.6f}, {b:.6f}]")
    except ValueError as e:
        print(e)
        exit()

    tol = 1e-4
    print(f"Tolerancia automática: {tol}")

    root, froot, iters = bisection(f, a, b, tol=tol)

    print("\n-----")
    print(f"Raíz aproximada: x = {root:.6f}")
    print(f"ERROR = {froot:.6e}")
    print(f"Iteraciones: {iters}")
