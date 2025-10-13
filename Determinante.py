# Programa para calcular el determinante de una matriz cuadrada


def mostrar_matriz(M):
    for fila in M:
        print(["{0:8.3f}".format(x) for x in fila])
    print()

def determinante(M):
    n = len(M)
    A = [fila[:] for fila in M]  # Copia de la matriz
    det = 1

    for i in range(n):
        # Si el pivote es cero, buscar una fila para intercambiar
        if A[i][i] == 0:
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    det *= -1  # cambiar el signo del determinante
                    break
            else:
                # Si no se encuentra fila, determinante es 0
                return 0

        # Multiplicar por el pivote
        det *= A[i][i]
        pivote = A[i][i]

        # Reducir las filas inferiores
        for k in range(i + 1, n):
            factor = A[k][i] / pivote
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    return det  # Retorna el valor del determinante
# ----------- PROGRAMA PRINCIPAL -----------
print("Ingrese el tamaño de la matriz:")
n = int(input("n = "))

A = []
print("Ingrese los elementos de la matriz (por filas):")
for i in range(n):
    fila = list(map(float, input(f"Fila {i+1}: ").split()))
    A.append(fila)

print("\nMatriz ingresada:")
mostrar_matriz(A)

resultado = determinante(A)
print(f"El determinante de la matriz es: {resultado:.3f}")
