#Determinante de una matriz cuadrada usando eliminación de Gauss con paso a paso
def mostrar_matriz(M):
    """Imprime la matriz de forma legible"""
    for fila in M:
        print("│", end=" ")
        print(" ".join(f"{x:8.2f}" for x in fila), end=" ")
        print("│")
    print()

def determinante_gauss(M):
    """Calcula el determinante usando eliminación de Gauss mostrando pasos"""
    n = len(M)
    det = 1
    matriz = [fila[:] for fila in M]

    print("\nMatriz inicial:")
    mostrar_matriz(matriz)

    for i in range(n):
        if matriz[i][i] == 0:
            for j in range(i + 1, n):
                if matriz[j][i] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    det *= -1
                    print(f"Intercambiamos filas {i + 1} y {j + 1}:")
                    mostrar_matriz(matriz)
                    break
            else:
                return 0

        for j in range(i + 1, n):
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            print(f"Restamos {factor:.2f} veces fila {i + 1} a fila {j + 1}:")
            mostrar_matriz(matriz)

    for i in range(n):
        det *= matriz[i][i]

    return det


# --- PROGRAMA PRINCIPAL ---
print("=== Cálculo del Determinante ")

n = int(input("Ingrese el tamaño de la matriz cuadrada : "))

A = []
print("\nIngrese los valores de la matriz :")
for i in range(n):
    fila = list(map(float, input(f"Fila {i+1}: ").split()))
    if len(fila) != n:
        print("  Error: Debe ingresar exactamente", n, "números por fila.")
        exit()
    A.append(fila)

resultado = determinante_gauss(A)
print(f"\nEl determinante de la matriz es: {resultado:.2f}")
