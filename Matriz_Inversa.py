# Programa para calcular la matriz inversa usando Gauss-Jordan


def mostrar_matriz(M):
    for fila in M:
        print(["{0:8.3f}".format(x) for x in fila])
    print()

def matriz_identidad(n):
    I = []
    for i in range(n):
        fila = [0] * n
        fila[i] = 1
        I.append(fila)
    return I

def invertir_matriz(A):
    n = len(A)
    # Crear una copia de A y una matriz identidad
    M = [fila[:] for fila in A]
    I = matriz_identidad(n)

    for i in range(n):
        # Verificar si el pivote es cero
        if M[i][i] == 0:
            # Buscar una fila para intercambiar
            for k in range(i + 1, n):
                if M[k][i] != 0:
                    M[i], M[k] = M[k], M[i]
                    I[i], I[k] = I[k], I[i]
                    break
            else:
                print("La matriz no tiene inversa (determinante 0).")
                return None

        # Hacer que el pivote sea 1
        pivote = M[i][i]
        for j in range(n):
            M[i][j] /= pivote
            I[i][j] /= pivote

        # Hacer ceros en las demás filas
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n):
                    M[k][j] -= factor * M[i][j]
                    I[k][j] -= factor * I[i][j]

    return I

# Ejemplo de uso
print("Ingrese el tamaño de la matriz:")
n = int(input("n = "))

A = []
print("Ingrese los elementos de la matriz (por filas):")
for i in range(n):
    fila = list(map(float, input(f"Fila {i+1}: ").split()))
    A.append(fila)

print("\nMatriz original:") 
mostrar_matriz(A)

inversa = invertir_matriz(A)

if inversa:
    print("Matriz inversa:")
    mostrar_matriz(inversa)
