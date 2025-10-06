# Programa para sumar dos matrices

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
        valor = int(input(f"A[{i}][{j}]: "))
        fila.append(valor)
    A.append(fila)

print("\nIngrese los elementos de la matriz B:")
for i in range(filas):
    fila = []
    for j in range(columnas):
        valor = int(input(f"B[{i}][{j}]: "))
        fila.append(valor)
    B.append(fila)

# Sumar matrices
for i in range(filas):
    fila = []
    for j in range(columnas):
        fila.append(A[i][j] + B[i][j])
    C.append(fila)

# Mostrar resultado
print("\nMatriz resultante (A + B):")
for fila in C:
    print(fila)