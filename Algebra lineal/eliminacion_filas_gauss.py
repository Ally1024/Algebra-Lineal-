
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa interactivo de Álgebra Lineal:
- Eliminación de filas (Gauss-Jordan) paso a paso sobre matriz aumentada [A|b]
- Cálculo de rango(A), rango([A|b]), determinante(A) si A es cuadrada
- Clasificación del sistema y solución (única / infinitas / ninguna)
- Inversa de A (opcional) si A es cuadrada y no singular

"""

from fractions import Fraction
from typing import List, Tuple, Optional

def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except Exception:
            print("Entrada inválida. Intenta nuevamente.")

def parse_num(x: str) -> Fraction:
    """
    Acepta enteros, decimales o fracciones tipo 'a/b' y devuelve Fraction.
    """
    x = x.strip().replace(",", ".")
    if "/" in x:
        num, den = x.split("/", 1)
        return Fraction(int(num), int(den))
    if "." in x:
        # Convertir decimal a Fraction con limit_denominator
        return Fraction(x).limit_denominator()
    return Fraction(int(x))

def leer_matriz_aumentada(m: int, n: int) -> List[List[Fraction]]:
    """
    Lee una matriz aumentada de tamaño m x (n+1): A|b
    """
    print(f"Introduce la matriz aumentada [A|b] de tamaño {m} x {n+1}.")
    print("Puedes usar enteros (2), fracciones (3/4) o decimales (0.5).")
    aug = []
    for i in range(m):
        while True:
            fila_raw = input(f"Fila {i+1} (separa {n+1} entradas por espacio): ")
            partes = fila_raw.strip().split()
            if len(partes) != n+1:
                print(f"Se esperaban {n+1} entradas. Recibidas: {len(partes)}.")
                continue
            try:
                fila = [parse_num(p) for p in partes]
                aug.append(fila)
                break
            except Exception as e:
                print("Entrada inválida en la fila. Detalle:", e)
    return aug

def clonar(mat: List[List[Fraction]]) -> List[List[Fraction]]:
    return [fila[:] for fila in mat]

def pretty(mat: List[List[Fraction]]) -> str:
    def fmt(x: Fraction) -> str:
        if x.denominator == 1:
            return f"{x.numerator}"
        return f"{x.numerator}/{x.denominator}"
    rows = ["[" + "  ".join(f"{fmt(x):>8}" for x in fila) + "]" for fila in mat]
    return "\n".join(rows)

def rref(aug: List[List[Fraction]]) -> Tuple[List[List[Fraction]], List[str], int, int, Fraction]:
    """
    Devuelve:
      - Matriz reducida por filas (RREF) de la aumentada
      - Lista de pasos como strings
      - rango(A), rango([A|b])
      - producto de pivotes (para determinante si A es cuadrada)
    Nota: El determinante = (producto de pivotes) * (-1)^{#swaps} sólo válido para A cuadrada.
    """
    A = clonar(aug)
    m = len(A)
    n_aug = len(A[0])    # n + 1
    n = n_aug - 1        # columnas de A
    pasos = []
    row = 0
    col = 0
    num_swaps = 0
    prod_pivotes = Fraction(1,1)

    while row < m and col < n:
        # Buscar pivote en (row..m-1, col)
        piv = None
        for r in range(row, m):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            pasos.append(f"No hay pivote en la columna {col+1}. Avanzar a la siguiente columna.")
            col += 1
            continue

        # Intercambio si el pivote no está en 'row'
        if piv != row:
            A[row], A[piv] = A[piv], A[row]
            num_swaps += 1
            pasos.append(f"Intercambiar filas R{row+1} ↔ R{piv+1}")
        
        piv_val = A[row][col]
        prod_pivotes *= piv_val if piv_val != 0 else 1

        # Normalizar fila pivote
        if piv_val != 1:
            factor = piv_val
            A[row] = [x / factor for x in A[row]]
            pasos.append(f"R{row+1} ← R{row+1} / {factor}")

        # Hacer ceros sobre y bajo el pivote
        for r in range(m):
            if r == row:
                continue
            factor = A[r][col]
            if factor != 0:
                A[r] = [x - factor*y for x, y in zip(A[r], A[row])]
                pasos.append(f"R{r+1} ← R{r+1} - ({factor})·R{row+1}")

        row += 1
        col += 1

    # Calcular rangos
    def rango(mat: List[List[Fraction]]) -> int:
        rank = 0
        for fila in mat:
            if any(x != 0 for x in fila):
                rank += 1
        return rank

    rango_A = rango([fila[:-1] for fila in A])
    rango_aug = rango(A)

    # Guardar metadatos de swaps para determinante
    A_meta = {
        "num_swaps": num_swaps,
        "prod_pivotes": prod_pivotes
    }
    pasos.append(f"Rango(A) = {rango_A}, Rango([A|b]) = {rango_aug}")
    return A, pasos, rango_A, rango_aug, Fraction((-1)**num_swaps) * prod_pivotes

def clasificar_y_resolver(A_rref: List[List[Fraction]]) -> Tuple[str, Optional[List[Fraction]], Optional[List[Tuple[int, Fraction]]]]:
    """
    Clasifica el sistema y si es posible devuelve solución única.
    Si hay infinitas soluciones, devuelve información básica de variables libres.
    """
    m = len(A_rref)
    n = len(A_rref[0]) - 1
    # Verificar inconsistencia: fila de la forma [0 ... 0 | c] con c != 0
    for fila in A_rref:
        if all(x == 0 for x in fila[:-1]) and fila[-1] != 0:
            return ("Sistema inconsistente (sin solución).", None, None)

    # Identificar pivotes por columna
    piv_col = []
    for j in range(n):
        col_vals = [A_rref[i][j] for i in range(m)]
        if col_vals.count(1) == 1 and all(v in (0,1) for v in col_vals):
            piv_col.append(j)

    if len(piv_col) == n:
        # Solución única: leer directamente
        sol = [Fraction(0,1)] * n
        for i in range(m):
            row = A_rref[i]
            # encontrar columna con 1
            col_ones = [j for j in range(n) if row[j] == 1]
            if col_ones:
                j = col_ones[0]
                sol[j] = row[-1]
        return ("Solución única.", sol, None)
    else:
        # Infinitas soluciones (variables libres)
        libres = [j for j in range(n) if j not in piv_col]
        # Devolver una descripción mínima: qué columnas son libres (1-indexadas con coeficiente 1)
        desc = [(j+1, Fraction(1,1)) for j in libres]
        return ("Infinitas soluciones (variables libres presentes).", None, desc)

def determinante_por_gauss(A: List[List[Fraction]]) -> Tuple[Fraction, int]:
    """
    Determinante via eliminación (sin preservar A original).
    Devuelve (det, swaps). Si A es singular, det=0.
    """
    n = len(A)
    M = [fila[:] for fila in A]
    det = Fraction(1,1)
    swaps = 0
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0,1), swaps
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            swaps += 1
        piv_val = M[col][col]
        det *= piv_val
        # eliminar abajo
        for r in range(col+1, n):
            if M[r][col] != 0:
                factor = M[r][col] / piv_val
                for c in range(col, n):
                    M[r][c] -= factor * M[col][c]
    if swaps % 2 == 1:
        det = -det
    return det, swaps

def inversa_por_gauss(A: List[List[Fraction]]) -> Optional[List[List[Fraction]]]:
    """
    Calcula la inversa de A (si existe) mediante [A|I] -> RREF -> [I|A^-1]
    """
    n = len(A)
    # Construir [A | I]
    aug = [A[i][:] + [Fraction(1 if i==j else 0,1) for j in range(n)] for i in range(n)]
    # Gauss-Jordan
    row = 0
    col = 0
    while row < n and col < n:
        piv = None
        for r in range(row, n):
            if aug[r][col] != 0:
                piv = r
                break
        if piv is None:
            col += 1
            continue
        if piv != row:
            aug[row], aug[piv] = aug[piv], aug[row]
        piv_val = aug[row][col]
        aug[row] = [x / piv_val for x in aug[row]]
        for r in range(n):
            if r == row:
                continue
            factor = aug[r][col]
            if factor != 0:
                aug[r] = [x - factor*y for x, y in zip(aug[r], aug[row])]
        row += 1
        col += 1
    # comprobar si lado izquierdo es identidad
    for i in range(n):
        for j in range(n):
            if aug[i][j] != (1 if i==j else 0):
                return None
    # extraer inversa
    inv = [fila[n:] for fila in aug]
    return inv

def imprimir_solucion(sol: Optional[List[Fraction]]):
    if sol is None:
        print("No se imprime solución concreta (infinitas o ninguna).")
        return
    def fmt(x: Fraction) -> str:
        return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    print("Solución:")
    for idx, val in enumerate(sol, start=1):
        print(f"x{idx} = {fmt(val)}")

def guardar_pasos(nombre: str, pasos: List[str], rref_mat: List[List[Fraction]]):
    def fmt(x: Fraction) -> str:
        if x.denominator == 1:
            return f"{x.numerator}"
        return f"{x.numerator}/{x.denominator}"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write("=== Pasos de Gauss-Jordan ===\n")
        for p in pasos:
            f.write(p + "\n")
        f.write("\n=== Matriz en RREF ===\n")
        for fila in rref_mat:
            f.write("[" + "  ".join(f"{fmt(x):>8}" for x in fila) + "]\n")
    print(f"Pasos guardados en: {nombre}")

def menu():
    print("\n=== Programa de Eliminación de Filas (Gauss-Jordan) ===")
    print("1) Resolver sistema lineal (RREF con pasos)")
    print("2) Calcular determinante de A (si A es cuadrada)")
    print("3) Calcular inversa de A (si existe)")
    print("4) Salir")

def leer_matriz(m: int, n: int) -> List[List[Fraction]]:
    print(f"Introduce la matriz A de tamaño {m} x {n}.")
    A = []
    for i in range(m):
        while True:
            fila_raw = input(f"Fila {i+1} ({n} entradas separadas por espacio): ")
            partes = fila_raw.strip().split()
            if len(partes) != n:
                print(f"Se esperaban {n} entradas.")
                continue
            try:
                fila = [parse_num(p) for p in partes]
                A.append(fila)
                break
            except Exception as e:
                print("Entrada inválida en la fila. Detalle:", e)
    return A

def main():
    while True:
        menu()
        op = input("Elige una opción: ").strip()
        if op == "1":
            m = leer_entero("Número de ecuaciones (filas, m): ")
            n = leer_entero("Número de incógnitas (columnas, n): ")
            aug = leer_matriz_aumentada(m, n)
            rref_mat, pasos, rA, rAug, prod_piv = rref(aug)
            print("\n=== Matriz RREF ===")
            print(pretty(rref_mat))
            print(f"Rango(A) = {rA}, Rango([A|b]) = {rAug}")
            clasif, sol, libres = clasificar_y_resolver(rref_mat)
            print("\n=== Clasificación del sistema ===")
            print(clasif)
            if sol is not None:
                imprimir_solucion(sol)
            elif libres is not None:
                print("Variables libres (índices 1-based):", [i for i,_ in libres])
            # Guardar pasos
            g = input("¿Guardar pasos en archivo? (s/n): ").strip().lower()
            if g == "s":
                nombre = input("Nombre del archivo .txt (sin espacios, opcional): ").strip() or "pasos_gauss.txt"
                guardar_pasos(nombre, pasos, rref_mat)

            # Determinante si A es cuadrada
            if m == n:
                A = [fila[:-1] for fila in aug]
                det, _ = determinante_por_gauss(A)
                print(f"\nDeterminante de A: {det if det.denominator==1 else f'{det.numerator}/{det.denominator}'}")

        elif op == "2":
            n = leer_entero("Orden de A (n x n): ")
            A = leer_matriz(n, n)
            det, _ = determinante_por_gauss(A)
            if det.denominator == 1:
                print(f"det(A) = {det.numerator}")
            else:
                print(f"det(A) = {det.numerator}/{det.denominator}")
        elif op == "3":
            n = leer_entero("Orden de A (n x n): ")
            A = leer_matriz(n, n)
            inv = inversa_por_gauss(A)
            if inv is None:
                print("A no es invertible (singular).")
            else:
                print("A^{-1} =")
                print(pretty(inv))
        elif op == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
