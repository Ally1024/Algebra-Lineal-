# PROGRAMA: Resolución de sistemas de ecuaciones lineales
# MÉTODO: Regla de Cramer 

def determinante(matriz):
    n = len(matriz)
    if n == 1:
        return matriz[0][0]
    if n == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
    det = 0
    for j in range(n):
        submatriz = [fila[:j] + fila[j+1:] for fila in matriz[1:]]
        signo = (-1) ** j
        det += signo * matriz[0][j] * determinante(submatriz)
    return det

def reemplazar_columna(matriz, columna, nueva_columna):
    n = len(matriz)
    nueva_matriz = []
    for i in range(n):
        fila = matriz[i][:]
        fila[columna] = nueva_columna[i]
        nueva_matriz.append(fila)
    return nueva_matriz

print("=== SISTEMA DE ECUACIONES - MÉTODO DE CRAMER ===")

n = int(input("Ingrese el número de ecuaciones o incógnitas: "))

A = []
B = []

print("\nIngrese los coeficientes y resultados de cada ecuación:")
for i in range(n):
    print(f"\nEcuación {i+1}:")
    fila = []
    for j in range(n):
        valor = float(input(f"Coeficiente de la incógnita {j+1}: "))
        fila.append(valor)
    resultado = float(input("Resultado de la ecuación: "))
    A.append(fila)
    B.append(resultado)

print("\nMatriz de coeficientes A:")
for fila in A:
    print(fila)
print("Vector de resultados B:", B)

# Determinante principal
D = determinante(A)
print("\nDeterminante principal D =", D)

if D == 0:
    print("El sistema no tiene solución única (D=0).")
else:
    soluciones = []
    for i in range(n):
        print(f"\n--- Resolviendo x{i+1} ---")
        Ai = reemplazar_columna(A, i, B)
        print(f"Matriz A{i+1} (columna {i+1} reemplazada por B):")
        for fila in Ai:
            print(fila)
        Di = determinante(Ai)
        print(f"Determinante D{i+1} =", Di)
        xi = Di / D
        print(f"x{i+1} = D{i+1} / D = {Di} / {D} = {xi}")
        soluciones.append(xi)

    print("\n=== SOLUCIÓN FINAL DEL SISTEMA ===")
    for i, valor in enumerate(soluciones):
        print(f"x{i+1} = {valor}")
