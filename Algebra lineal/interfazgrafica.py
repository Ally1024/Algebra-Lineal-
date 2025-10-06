import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from fractions import Fraction

# ------------------ FUNCIONES DE PARSEO ------------------

def parse_token_to_number(tok: str, as_fraction=True):
    """Convierte un token a int, float o Fraction."""
    tok = tok.strip()
    if not tok:
        return None
    try:
        return int(tok)
    except:
        pass
    try:
        return float(tok)
    except:
        pass
    if as_fraction:
        try:
            return Fraction(tok)
        except:
            pass
    raise ValueError(f"No se pudo interpretar el número: {tok}")

def parse_matrix_text_to_list_of_lists(text: str, use_fraction=True):
    """Convierte un texto en matriz (lista de listas)."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip() != ""]
    if not lines:
        return None
    mat = []
    for line in lines:
        toks = line.replace(",", " ").split()
        row = [parse_token_to_number(tok, as_fraction=use_fraction) for tok in toks if tok.strip()!=""]
        mat.append(row)
    return mat

def matrix_to_string(mat):
    """Convierte lista o matriz en string formateado."""
    if isinstance(mat, list):
        if not mat:
            return "[]"
        if isinstance(mat[0], list):
            return "\n".join([" ".join(str(x) for x in row) for row in mat])
        else:
            return "[" + ", ".join(str(x) for x in mat) + "]"
    return str(mat)

# ------------------ OPERACIONES MATRICIALES ------------------

def suma_matrices(A, B):
    if len(A)!=len(B) or len(A[0])!=len(B[0]):
        raise ValueError("Dimensiones incompatibles para suma.")
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta_matrices(A, B):
    if len(A)!=len(B) or len(A[0])!=len(B[0]):
        raise ValueError("Dimensiones incompatibles para resta.")
    return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplica_matrices(A, B):
    if len(A[0])!=len(B):
        raise ValueError("Dimensiones incompatibles para multiplicación.")
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def transpuesta(A):
    return list(map(list, zip(*A)))

def determinante(M):
    n = len(M)
    if any(len(row)!=n for row in M):
        raise ValueError("La matriz no es cuadrada.")
    if n==1:
        return M[0][0]
    if n==2:
        return M[0][0]*M[1][1]-M[0][1]*M[1][0]
    det = 0
    for c in range(n):
        minor = [row[:c]+row[c+1:] for row in M[1:]]
        det += ((-1)**c)*M[0][c]*determinante(minor)
    return det

def inversa(M):
    n = len(M)
    if any(len(row)!=n for row in M):
        raise ValueError("La matriz no es cuadrada.")
    A = [[Fraction(M[i][j]) for j in range(n)] for i in range(n)]
    I = [[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
    for i in range(n):
        if A[i][i] == 0:
            for r in range(i+1, n):
                if A[r][i] != 0:
                    A[i], A[r] = A[r], A[i]
                    I[i], I[r] = I[r], I[i]
                    break
            else:
                raise ValueError("La matriz no es invertible.")
        pivote = A[i][i]
        A[i] = [aij/pivote for aij in A[i]]
        I[i] = [iij/pivote for iij in I[i]]
        for r in range(n):
            if r != i:
                factor = A[r][i]
                A[r] = [a - factor*b for a,b in zip(A[r], A[i])]
                I[r] = [a - factor*b for a,b in zip(I[r], I[i])]
    return I

# ------------------ ARREGLOS SIN NUMPY ------------------

def parse_1d_list(text: str):
    vals = [parse_token_to_number(t) for t in text.replace("\n", " ").split() if t.strip()!=""]
    return vals

def parse_2d_list(text: str):
    return parse_matrix_text_to_list_of_lists(text, use_fraction=False)

def parse_3d_list(text: str):
    raw = text.strip()
    if not raw:
        return None
    capas_raw = [cap.strip() for cap in raw.split("\n\n") if cap.strip() != ""]
    capas = []
    for cap in capas_raw:
        mat = parse_matrix_text_to_list_of_lists(cap, use_fraction=False)
        capas.append(mat)
    return capas

# ------------------ CLASE APLICACIÓN ------------------

class App:
    def __init__(self, root):
        self.root = root
        root.title("Operaciones de Álgebra Lineal")
        self.opciones = [
            "Vectores",
            "Matrices - Operaciones básicas",
            "Matrices - Determinante",
            "Matrices - Inversa",
            "Arreglos NumPy (1D/2D/3D)"
        ]
        self.widgets = {}
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Seleccione opción:").grid(row=0, column=0, sticky="w")
        self.widgets['combo'] = ttk.Combobox(frame, values=self.opciones, state="readonly", width=40)
        self.widgets['combo'].grid(row=0, column=1, sticky="ew")
        self.widgets['combo'].bind("<<ComboboxSelected>>", self.update_input_area)

        self.input_area = ttk.Frame(frame)
        self.input_area.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.widgets['btn'] = ttk.Button(frame, text="Resolver", command=self.resolver)
        self.widgets['btn'].grid(row=2, column=0, columnspan=2)

        self.output_text = scrolledtext.ScrolledText(frame, width=60, height=15)
        self.output_text.grid(row=3, column=0, columnspan=2, pady=10)

    def update_input_area(self, event=None):
        for w in self.input_area.winfo_children():
            w.destroy()
        sel = self.widgets['combo'].get()

        if sel=="Vectores":
            ttk.Label(self.input_area, text="Vector A:").grid(row=0, column=0, sticky="w")
            self.widgets['va'] = tk.Entry(self.input_area, width=40)
            self.widgets['va'].grid(row=0, column=1)
            ttk.Label(self.input_area, text="Vector B:").grid(row=1, column=0, sticky="w")
            self.widgets['vb'] = tk.Entry(self.input_area, width=40)
            self.widgets['vb'].grid(row=1, column=1)

        elif sel=="Matrices - Operaciones básicas":
            ttk.Label(self.input_area, text="Matriz A:").grid(row=0, column=0, sticky="w")
            self.widgets['ma'] = scrolledtext.ScrolledText(self.input_area, width=30, height=5)
            self.widgets['ma'].grid(row=0, column=1)
            ttk.Label(self.input_area, text="Matriz B:").grid(row=1, column=0, sticky="w")
            self.widgets['mb'] = scrolledtext.ScrolledText(self.input_area, width=30, height=5)
            self.widgets['mb'].grid(row=1, column=1)

        elif sel in ["Matrices - Determinante", "Matrices - Inversa"]:
            ttk.Label(self.input_area, text="Matriz:").grid(row=0, column=0, sticky="w")
            self.widgets['ma'] = scrolledtext.ScrolledText(self.input_area, width=30, height=5)
            self.widgets['ma'].grid(row=0, column=1)

        elif sel=="Arreglos NumPy (1D/2D/3D)":
            ttk.Label(self.input_area, text="Tipo (1D/2D/3D):").grid(row=0, column=0, sticky="w")
            self.widgets['tipo_var'] = tk.StringVar(value="1D")
            ttk.Combobox(self.input_area, textvariable=self.widgets['tipo_var'],
                         values=["1D","2D","3D"], state="readonly").grid(row=0, column=1, sticky="ew")
            ttk.Label(self.input_area, text="Contenido:").grid(row=1, column=0, sticky="nw")
            self.widgets['ta'] = scrolledtext.ScrolledText(self.input_area, width=40, height=8)
            self.widgets['ta'].grid(row=1, column=1)

    def resolver(self):
        self.output_text.delete("1.0", tk.END)
        sel = self.widgets['combo'].get()
        try:
            if sel=="Vectores":
                va = [parse_token_to_number(x) for x in self.widgets['va'].get().split()]
                vb = [parse_token_to_number(x) for x in self.widgets['vb'].get().split()]
                if len(va)!=len(vb):
                    raise ValueError("Los vectores deben tener la misma dimensión.")
                suma = [a+b for a,b in zip(va,vb)]
                self.output_text.insert(tk.END, "Suma: "+str(suma)+"\n")
                escalar = sum(a*b for a,b in zip(va,vb))
                self.output_text.insert(tk.END, "Producto escalar: "+str(escalar)+"\n")

            elif sel=="Matrices - Operaciones básicas":
                A = parse_matrix_text_to_list_of_lists(self.widgets['ma'].get("1.0", tk.END))
                B = parse_matrix_text_to_list_of_lists(self.widgets['mb'].get("1.0", tk.END))
                self.output_text.insert(tk.END, "A+B:\n"+matrix_to_string(suma_matrices(A,B))+"\n\n")
                self.output_text.insert(tk.END, "A-B:\n"+matrix_to_string(resta_matrices(A,B))+"\n\n")
                self.output_text.insert(tk.END, "A*B:\n"+matrix_to_string(multiplica_matrices(A,B))+"\n\n")
                self.output_text.insert(tk.END, "Transpuesta(A):\n"+matrix_to_string(transpuesta(A))+"\n")

            elif sel=="Matrices - Determinante":
                A = parse_matrix_text_to_list_of_lists(self.widgets['ma'].get("1.0", tk.END))
                det = determinante(A)
                self.output_text.insert(tk.END, "Determinante: "+str(det)+"\n")

            elif sel=="Matrices - Inversa":
                A = parse_matrix_text_to_list_of_lists(self.widgets['ma'].get("1.0", tk.END))
                inv = inversa(A)
                self.output_text.insert(tk.END, "Inversa:\n"+matrix_to_string(inv)+"\n")

            elif sel=="Arreglos NumPy (1D/2D/3D)":
                tipo = self.widgets['tipo_var'].get()
                text = self.widgets['ta'].get("1.0", tk.END)
                if tipo=="1D":
                    arr = parse_1d_list(text)
                    self.output_text.insert(tk.END, "Arreglo 1D:\n"+matrix_to_string(arr)+"\n")
                elif tipo=="2D":
                    mat = parse_2d_list(text)
                    self.output_text.insert(tk.END, "Arreglo 2D:\n"+matrix_to_string(mat)+"\n")
                elif tipo=="3D":
                    capas = parse_3d_list(text)
                    self.output_text.insert(tk.END, "Arreglo 3D:\n"+matrix_to_string(capas)+"\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# ------------------ MAIN ------------------

if __name__=="__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
