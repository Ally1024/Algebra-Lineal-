# Programa para sumar dos matrices con expresiones algebraicas

# Pedir dimensiones
filas = int(input("Ingrese el número de filas: "))
columnas = int(input("Ingrese el número de columnas: "))

# Inicializar matrices
A = []
B = []
C = []

print("\nIngrese los elementos de la matriz A:")
for i in range(filas):
    fila = []
    for j in range(columnas):
        valor = input(f"A[{i}][{j}]: ")  # ahora es string
        fila.append(valor)
    A.append(fila)

print("\nIngrese los elementos de la matriz B:")
for i in range(filas):
    fila = []
    for j in range(columnas):
        valor = input(f"B[{i}][{j}]: ")  # ahora es string
        fila.append(valor)
    B.append(fila)

# Sumar matrices algebraicas
for i in range(filas):
    fila = []
    for j in range(columnas):
        # Concatenar con " + " si ambos valores no están vacíos
        if A[i][j] and B[i][j]:
            fila.append(f"{A[i][j]} + {B[i][j]}")
        elif A[i][j]:
            fila.append(A[i][j])
        else:
            fila.append(B[i][j])
    C.append(fila)

# Mostrar resultado
print("\nMatriz resultante (A + B):")
for fila in C:
    print(fila)
