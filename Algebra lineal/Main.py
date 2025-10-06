from interfazgrafica import ejecutar_interfaz

def main():
    print("=== Calculadora de Matrices ===")
    print("1. Abrir interfaz gráfica")
    print("2. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        ejecutar_interfaz()
    elif opcion == "2":
        print("Saliendo del programa...")
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
