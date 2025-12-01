# Multiplicacion_de_matrices.py

def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices A y B.
    Devuelve la matriz resultante.
    Permite imprimir los pasos si se desea, pero no usa input().
    """
    if not A or not B:
        raise ValueError("Las matrices no pueden estar vacías.")
    if len(A[0]) != len(B):
        raise ValueError("Las matrices no se pueden multiplicar: columnas de A ≠ filas de B")

    filas_A, columnas_B = len(A), len(B[0])
    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_B):
            suma = 0
            for k in range(len(B)):
                suma += A[i][k] * B[k][j]
            resultado[i][j] = suma
    return resultado
