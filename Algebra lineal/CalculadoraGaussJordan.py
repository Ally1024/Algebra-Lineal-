from fractions import Fraction  # Para trabajar con fracciones exactas

# Función para convertir un string en número fracción (soporta enteros, decimales y fracciones)
def parse_num(x: str) -> Fraction:
    x = x.strip().replace(",", ".")  # Cambia comas por puntos (ej: 0,5 -> 0.5)
    if "/" in x:  # Si es fracción
        num, den = x.split("/", 1)
        return Fraction(int(num), int(den))
    if "." in x:  # Si es decimal
        return Fraction(x)
    return Fraction(int(x))  # Si es entero

# Función para leer la matriz aumentada [A|b] ingresada por el usuario
def leer_matriz_aumentada(m: int, n: int):
    print(f"Introduce la matriz aumentada [A|b] de tamaño {m} x {n+1}.")
    print("Puedes usar enteros (2), fracciones (3/4) o decimales (0.5).")
    aug = []
    for i in range(m):  # Para cada fila
        while True:
            fila_raw = input(f"Fila {i+1} (separa {n+1} valores por espacio): ")
            partes = fila_raw.strip().split()
            if len(partes) != n+1:  # Validación de número de valores
                print(f"Se esperaban {n+1} valores. Recibidos: {len(partes)}.")
                continue
            try:
                fila = [parse_num(p) for p in partes]  # Convertir cada número
                aug.append(fila)
                break
            except Exception as e:
                print("Entrada inválida en la fila. Detalle:", e)
    return aug

# Formatear fracciones para mostrar: enteros como "2", fracciones como "3/4"
def format_frac(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"

# Mostrar la matriz por pantalla
def mostrar_matriz(aug):
    for fila in aug:
        print("  ".join(format_frac(x) for x in fila))
    print()

# Método de Gauss-Jordan paso a paso
def gauss_jordan_eliminacion(aug):
    m = len(aug)          # Número de filas
    n = len(aug[0]) - 1   # Número de incógnitas
    matriz = [fila[:] for fila in aug]  # Copiar matriz para no modificar original
    pivotes = []          # Lista de pivotes (fila, columna)
    pivotes_valores = {}  # Guarda el valor original de cada pivote antes de normalizar

    print("\n=== Proceso de Gauss-Jordan paso a paso (eliminación de filas) ===")
    mostrar_matriz(matriz)

    fila = 0
    for col in range(n):  # Recorremos columnas
        # Buscar un pivote en la columna col a partir de la fila actual
        pivot_row = None
        for r in range(fila, m):
            if matriz[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:  # Si no hay pivote en esta columna, continuar
            continue

        # Intercambiar filas si el pivote no está en la fila actual
        if pivot_row != fila:
            matriz[fila], matriz[pivot_row] = matriz[pivot_row], matriz[fila]
            print(f"Intercambio: fila {fila+1} <-> fila {pivot_row+1}")
            mostrar_matriz(matriz)

        # Guardar valor del pivote antes de normalizar
        piv_val = matriz[fila][col]
        pivotes.append((fila, col))
        pivotes_valores[(fila, col)] = piv_val
        print(f"Pivote encontrado en fila {fila+1}, columna {col+1} con valor {format_frac(piv_val)}")

        # Normalizar fila pivote (hacer que el pivote sea 1)
        if piv_val != 1:
            print(f"Normalizar fila {fila+1} dividiendo por {format_frac(piv_val)}")
            matriz[fila] = [x / piv_val for x in matriz[fila]]
            mostrar_matriz(matriz)

        # Eliminar valores en la columna col en todas las demás filas
        for r in range(m):
            if r != fila and matriz[r][col] != 0:
                factor = matriz[r][col]  # Como el pivote ya es 1
                print(f"Fila {r+1} ← Fila {r+1} - ({format_frac(factor)}) * Fila {fila+1}")
                matriz[r] = [x - factor * y for x, y in zip(matriz[r], matriz[fila])]
                mostrar_matriz(matriz)

        fila += 1  # Pasamos a la siguiente fila
        if fila == m:
            break

    # Calcular rangos de A y de [A|b]
    rangoA = sum(1 for r in range(m) if any(matriz[r][c] != 0 for c in range(n)))
    rangoAug = sum(1 for r in range(m) if any(matriz[r][c] != 0 for c in range(n+1)))

    # Identificar columnas pivote y variables libres
    pivot_cols = [col for (_, col) in pivotes]
    variables_libres = [j for j in range(n) if j not in pivot_cols]

    print("\n=== Resultados finales ===")
    print("Pivotes (fila, columna) y valor original:")
    for (r, c) in pivotes:
        print(f" - fila {r+1}, columna {c+1} ; pivote original = {format_frac(pivotes_valores[(r,c)])}")
    print(f"Columnas pivote (índices 1..n): {[c+1 for c in pivot_cols]}")
    print(f"Variables libres (índices 1..n): {[j+1 for j in variables_libres]}")
    print(f"rank(A) = {rangoA}, rank([A|b]) = {rangoAug}, n = {n}")

    # Clasificación del sistema según los rangos
    print("\n--- Clasificación según rangos ---")
    if rangoA < rangoAug:
        # Caso 3: sistema inconsistente
        print("Sistema inconsistente → no tiene solución (rank(A) < rank([A|b]))")
        return
    if rangoA == n:
        # Caso 1: solución única
        print("Sistema compatible determinado → solución única (rank(A) = rank([A|b]) = n)")
        solucion = [None] * n
        for (r, c) in pivotes:
            solucion[c] = matriz[r][-1]
        for j in range(n):
            if solucion[j] is None:
                solucion[j] = Fraction(0)  # Seguridad
        print("\nSolución única:")
        for j, val in enumerate(solucion):
            print(f"x{j+1} = {format_frac(val)}")
        return
    # Caso 2: infinitas soluciones (variables libres)
    print("Sistema compatible indeterminado → existen infinitas soluciones (variables libres presentes).")
    print("\nSolución en forma paramétrica:")

    ecuaciones = {}
    for (r, c) in pivotes:
        termino = format_frac(matriz[r][-1])
        expr = f"{termino}"
        for j in variables_libres:
            coef = matriz[r][j]
            if coef != 0:
                expr += f" - ({format_frac(coef)})*t{j+1}"
        ecuaciones[c] = expr

    # Mostrar variables libres como parámetros
    for j in variables_libres:
        print(f"x{j+1} = t{j+1}  (parámetro libre)")

    # Mostrar variables básicas en función de parámetros
    for col in sorted(ecuaciones):
        print(f"x{col+1} = {ecuaciones[col]}")

    # Resumen final de condiciones
    print("\n--- Resumen de las 3 condiciones de existencia/unicidad ---")
    print("1) rank(A) = rank([A|b]) = n  -> solución única.")
    print("2) rank(A) = rank([A|b]) < n  -> soluciones infinitas (variables libres).")
    print("3) rank(A) < rank([A|b])      -> sistema inconsistente (sin solución).")

# Función principal
def main():
    print("=== Resolución de sistemas lineales por Gauss-Jordan (RREF) ===")
    m = int(input("Número de ecuaciones (filas): "))
    n = int(input("Número de incógnitas (columnas): "))
    aug = leer_matriz_aumentada(m, n)  # Leer matriz del usuario
    print("\nMatriz inicial:")
    mostrar_matriz(aug)  # Mostrar matriz ingresada
    gauss_jordan_eliminacion(aug)  # Resolver sistema

# Punto de entrada
if __name__ == "__main__":
    main()
