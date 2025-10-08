def input_int(prompt, min_val=None):
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if min_val is not None and v < min_val:
                print(f"Por favor ingrese un entero >= {min_val}.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Introduzca un número entero.")

def input_float(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except ValueError:
            print("Entrada inválida. Introduzca un número (p. ej. 3.5 o 2).")

def format_number(x):
    """Imprime float sin .0 si es entero."""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)

def crear_arreglo_1D():
    n = input_int("¿Cuántos elementos tendrá el arreglo 1D? ", min_val=0)
    elementos = []
    for i in range(n):
        valor = input_float(f"Ingrese el valor {i+1}: ")
        elementos.append(valor)
    return elementos  # lista 1D

def crear_arreglo_2D():
    filas = input_int("¿Cuántas filas tendrá el arreglo 2D? ", min_val=0)
    columnas = input_int("¿Cuántas columnas tendrá el arreglo 2D? ", min_val=0)
    elementos = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = input_float(f"Ingrese valor en posición [{i}][{j}]: ")
            fila.append(valor)
        elementos.append(fila)
    return elementos  # lista de listas

def crear_arreglo_3D():
    profundidad = input_int("¿Cuántas capas tendrá el arreglo 3D? ", min_val=0)
    filas = input_int("¿Cuántas filas por capa? ", min_val=0)
    columnas = input_int("¿Cuántas columnas por fila? ", min_val=0)

    elementos = []
    for k in range(profundidad):
        print(f"-- Capa {k} --")
        capa = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor = input_float(f"Ingrese valor en [{k}][{i}][{j}]: ")
                fila.append(valor)
            capa.append(fila)
        elementos.append(capa)
    return elementos  # lista de capas (cada capa es lista 2D)

def imprimir_1d(arr):
    print("[ " + "  ".join(format_number(x) for x in arr) + " ]")

def imprimir_2d(mat):
    for fila in mat:
        print(" ".join(format_number(x) for x in fila))

def imprimir_3d(capas):
    for k, capa in enumerate(capas):
        print(f"--- Capa {k} ---")
        imprimir_2d(capa)
        print()

def obtener_forma_1d(arr):
    return (len(arr),)

def obtener_forma_2d(mat):
    if not mat:
        return (0, 0)
    return (len(mat), len(mat[0]) if mat[0] is not None else 0)

def obtener_forma_3d(capas):
    if not capas:
        return (0, 0, 0)
    profundidad = len(capas)
    filas = len(capas[0]) if capas[0] else 0
    columnas = len(capas[0][0]) if (capas[0] and capas[0][0]) else 0
    return (profundidad, filas, columnas)

# ------------------ MENÚ PRINCIPAL ------------------
def main():
    while True:
        print("\n--- CREACIÓN DE ARREGLOS---")
        print("1. Crear arreglo 1D")
        print("2. Crear arreglo 2D")
        print("3. Crear arreglo 3D")
        print("4. Salir")

        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            arr1 = crear_arreglo_1D()
            print("\nArreglo 1D creado:")
            imprimir_1d(arr1)
            print("Forma:", obtener_forma_1d(arr1))

        elif opcion == "2":
            arr2 = crear_arreglo_2D()
            print("\nArreglo 2D creado:")
            imprimir_2d(arr2)
            print("Forma:", obtener_forma_2d(arr2))

        elif opcion == "3":
            arr3 = crear_arreglo_3D()
            print("\nArreglo 3D creado:")
            imprimir_3d(arr3)
            print("Forma:", obtener_forma_3d(arr3))

        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()

