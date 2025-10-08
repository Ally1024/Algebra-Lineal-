def gauss_eliminacion(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    rango = 0

    for c in range(columnas):
        # Buscar fila con pivote no nulo
        pivote = None
        for f in range(rango, filas):
            if matriz[f][c] != 0:
                pivote = f
                break

        if pivote is None:
            continue  # No hay pivote en esta columna

        # Intercambiar filas
        matriz[rango], matriz[pivote] = matriz[pivote], matriz[rango]

        # Normalizar la fila del pivote
        pivote_valor = matriz[rango][c]
        matriz[rango] = [x / pivote_valor for x in matriz[rango]]

        # Hacer ceros en las demás filas
        for f in range(filas):
            if f != rango and matriz[f][c] != 0:
                factor = matriz[f][c]
                matriz[f] = [matriz[f][i] - factor * matriz[rango][i] for i in range(columnas)]

        rango += 1

    return rango

def es_linealmente_independiente(vectores):
    # Clonamos la matriz para no modificar el original
    matriz = [fila[:] for fila in vectores]
    rango = gauss_eliminacion(matriz)
    return rango == len(vectores)

# Ejemplo de uso
n = int(input("¿Cuántos vectores vas a ingresar? "))
m = int(input("¿De cuántos elementos es cada vector? "))

vectores = []
for i in range(n):
    vector = list(map(float, input(f"Ingrese los {m} valores del vector {i+1}, separados por espacio: ").split()))
    vectores.append(vector)

if es_linealmente_independiente(vectores):
    print("\n Los vectores son linealmente independientes.")
else:
    print("\n Los vectores son linealmente dependientes.")
