# multiplicación de matrices 
def leer_matriz(nombre):
    filas = int(input(f"Ingrese el número de filas de la matriz {nombre}: "))
    columnas = int(input(f"Ingrese el número de columnas de la matriz {nombre}: "))
    print(f"\nIngrese las filas de la matriz {nombre}, separando los números con espacios:")
    matriz = []
    for i in range(filas):
        fila = list(map(int, input(f"Fila {i+1}: ").split()))
        if len(fila) != columnas:
            raise ValueError("El número de elementos no coincide con las columnas indicadas.")
        matriz.append(fila)
    return matriz

def imprimir_matriz(M, nombre="Matriz"):
    print(f"\n{nombre}:")
    for fila in M:
        print(fila)

def multiplicar_matrices(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Las matrices no se pueden multiplicar: columnas de A ≠ filas de B")

    filas_A, columnas_B = len(A), len(B[0])
    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    print("\n--- Pasos de la multiplicación ---")
    for i in range(filas_A):
        for j in range(columnas_B):
            suma = 0
            print(f"\nCalculando elemento C[{i+1},{j+1}]:")
            for k in range(len(B)):
                producto = A[i][k] * B[k][j]
                suma += producto
                print(f"  A[{i+1},{k+1}] * B[{k+1},{j+1}] = {A[i][k]} * {B[k][j]} = {producto}")
            resultado[i][j] = suma
            print(f"  → Suma total = {suma}")
    return resultado

# Programa principal
if __name__ == "__main__":
    print("=== Multiplicación de Matrices ===")
    A = leer_matriz("A")
    B = leer_matriz("B")

    imprimir_matriz(A, "Matriz A")
    imprimir_matriz(B, "Matriz B")

    try:
        C = multiplicar_matrices(A, B)
        imprimir_matriz(C, "Resultado A x B")
    except ValueError as e:
        print(e)