#Programa que calcula el determinante de una matriz cuadradao mas de una matriz 
# usando ya sea la regla de Sarrus , la regla de Cramer o el método de eliminación de Gauss, mostrando los pasos intermedios.

def mostrar_matriz(M):
    for fila in M:
        print("│", end=" ")
        print(" ".join("{:4.0f}".format(x) for x in fila), end=" │\n")
    print()

#  función  para mostrar pasos (eliminación)
def determinante_pasos(A):
    n = len(A)
    M = [fila[:] for fila in A] 
    det = 1
    pivotes = []

    print("Calcule det A, donde:\n")
    print("A = ")
    mostrar_matriz(M)

    for i in range(n):
        pivote = M[i][i]
        if abs(pivote) < 1e-12:
            for k in range(i + 1, n):
                if abs(M[k][i]) > 1e-12:
                    M[i], M[k] = M[k], M[i]
                    det *= -1
                    pivote = M[i][i]
                    print(f"Se intercambió la fila {i+1} con la fila {k+1}\n")
                    mostrar_matriz(M)
                    break
            else:
                print("La matriz tiene determinante 0 (no se puede continuar).")
                return 0

        pivotes.append(pivote)
        det *= pivote

        # Crear submatriz para mostrar (lo que queda bajo y a la derecha del pivote)
        submatriz = [fila[i+1:] for fila in M[i+1:]]
        # Eliminar los ceros inferiores del pivote (operaciones fila)
        for k in range(i + 1, n):
            factor = M[k][i] / pivote
            for j in range(i, n):
                M[k][j] -= factor * M[i][j]

        # Mostrar paso
        if i == 0:
            print(f"det A = {int(round(pivote))} ·", end=" ")
        elif i < n - 1 and len(submatriz) > 1:
            print(f"\ndet A = {' × '.join(str(int(round(p)) )for p in pivotes)} ·", end=" ")

        if len(submatriz) > 0:
            print()
            mostrar_matriz(submatriz)

    # Mostrar resultado final
    det_int = int(round(det)) if abs(det - round(det)) < 1e-9 else det
    print(f"det A = {' × '.join(str(int(round(p))) for p in pivotes)} = {det_int}")
    return det

# ---------- Determinante por la fórmula de Leibniz (permutações) ----------
# Genera permutaciones recursivamente 
def generar_permutaciones(n):
    perms = []
    used = [False]*n
    p = [0]*n

    def backtrack(pos):
        if pos == n:
            perms.append(p[:])
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                p[pos] = i
                backtrack(pos+1)
                used[i] = False
    backtrack(0)
    return perms

def signo_permutacion(perm):
    inv = 0
    n = len(perm)
    for i in range(n):
        for j in range(i+1, n):
            if perm[i] > perm[j]:
                inv += 1
    return -1 if (inv % 2) else 1

def determinante_leibniz(A, mostrar_pasos=True):
    n = len(A)
    if n == 0:
        return 1
    perms = generar_permutaciones(n)
    suma_pos = 0.0
    suma_neg = 0.0
    total = 0.0
    if mostrar_pasos:
        print("-"*60)
        print(f"Calculando determinante por la fórmula de Leibniz (n={n}) mostrando permutaciones:")
        mostrar_matriz(A)
    for perm in perms:
        sgn = signo_permutacion(perm)
        prod = 1.0
        term_str = []
        for row_idx, col_idx in enumerate(perm):
            val = A[row_idx][col_idx]
            prod *= val
            term_str.append(f"a{row_idx+1}{col_idx+1}({int(round(val))})")
        if mostrar_pasos:
            signo_text = "+" if sgn==1 else "-"
            print(f"{signo_text} Perm {perm} -> producto = {' * '.join(term_str)} = {int(round(prod)) if abs(prod-round(prod))<1e-9 else prod}")
        if sgn == 1:
            suma_pos += prod
        else:
            suma_neg += prod
        total += sgn * prod

    if mostrar_pasos:
        pos = int(round(suma_pos)) if abs(suma_pos-round(suma_pos))<1e-9 else suma_pos
        neg = int(round(suma_neg)) if abs(suma_neg-round(suma_neg))<1e-9 else suma_neg
        tot = int(round(total)) if abs(total-round(total))<1e-9 else total
        print(f"Suma positivas = {pos}")
        print(f"Suma negativas = {neg}")
        print(f"Determinante = {pos} - {neg} = {tot}")
        print("-"*60)
    return total

def sarrus_generalizado(A):
    n = len(A)
    if n == 3:
        a = A
        print("-"*60)
        print("Aplicando regla de Sarrus (3x3):")
        mostrar_matriz(A)
        d1 = a[0][0]*a[1][1]*a[2][2]
        d2 = a[0][1]*a[1][2]*a[2][0]
        d3 = a[0][2]*a[1][0]*a[2][1]
        s1 = a[0][2]*a[1][1]*a[2][0]
        s2 = a[0][0]*a[1][2]*a[2][1]
        s3 = a[0][1]*a[1][0]*a[2][2]
        suma = d1 + d2 + d3
        resta = s1 + s2 + s3
        print(f"Diagonales principales: {int(round(d1))}, {int(round(d2))}, {int(round(d3))} -> suma = {int(round(suma))}")
        print(f"Diagonales secundarias: {int(round(s1))}, {int(round(s2))}, {int(round(s3))} -> suma = {int(round(resta))}")
        det = suma - resta
        print(f"det(A) = {int(round(suma))} - {int(round(resta))} = {int(round(det))}")
        print("-"*60)
        return det
    else:
        print(f"Sarrus generalizado para n={n} (usando la definición por permutaciones):")
        return determinante_leibniz(A, mostrar_pasos=True)

def cramer_pasos(A, b):
    n = len(A)
    print("-"*60)
    print("Aplicando regla de Cramer para resolver Ax = b")
    print("Matriz A:")
    mostrar_matriz(A)
    print("Vector b:", [int(round(x)) if abs(x-round(x))<1e-9 else x for x in b])
    detA = determinante_pasos(A)
    if abs(detA) < 1e-12:
        print("det(A) = 0 -> No existe solución única (Cramer no aplica).")
        return None
    soluciones = []
    for i in range(n):
        Ai = [row[:] for row in A]
        for r in range(n):
            Ai[r][i] = b[r]
        print(f"\nCalculando det(A_{i+1}) (reemplazando columna {i+1} por b):")
        mostrar_matriz(Ai)
        detAi = determinante_pasos(Ai)
        xi = detAi / detA
        xi_out = int(round(xi)) if abs(xi-round(xi))<1e-9 else xi
        detAi_out = int(round(detAi)) if abs(detAi-round(detAi))<1e-9 else detAi
        detA_out = int(round(detA)) if abs(detA-round(detA))<1e-9 else detA
        print(f"x{i+1} = det(A_{i+1}) / det(A) = {detAi_out} / {detA_out} = {xi_out}")
        soluciones.append(xi)
    print("\nSolución por Cramer (vector x):", [int(round(v)) if abs(v-round(v))<1e-9 else v for v in soluciones])
    print("-"*60)
    return soluciones

def leer_entero(mensaje):
    while True:
        try:
            val = int(input(mensaje))
            return val
        except:
            print("Entrada no válida. Ingresa un entero.")

def leer_fila_esperada(n, prompt):
    while True:
        entrada = input(prompt).strip().split()
        if len(entrada) != n:
            print(f"Se esperaban {n} valores. Intenta de nuevo.")
            continue
        try:
            return [float(x) for x in entrada]
        except:
            print("Valores no válidos. Usa números (enteros o decimales).")

def main():
    print("¿Cuántas matrices deseas ingresar? (1,2,3,...):")
    m = leer_entero("Cantidad de matrices = ")
    if m < 1:
        print("Cantidad mínima 1. Se usará 1.")
        m = 1

    for idx in range(1, m+1):
        print("\n" + "="*60)
        print(f"MATRIZ #{idx}")
        n = leer_entero("Ingrese el tamaño de la matriz (n para n x n): n = ")
        if n < 1:
            print("n debe ser >= 1. Se usará n=1.")
            n = 1
        print("Ingrese los elementos de la matriz (por filas):")
        A = []
        for i in range(n):
            fila = leer_fila_esperada(n, f"Fila {i+1}: ")
            A.append(fila)

        while True:
            print("\n¿Qué método deseas aplicar a esta matriz?")
            print(" 1) Sarrus ")
            print(" 2) Cramer ")
            print(" 3) Gauss ")
            print(" 4) Combinar Sarrus + Cramer (calcula det(A) con Sarrus y luego resuelve por Cramer)")
            print(" 5) Volver a elegir otro método para esta misma matriz / terminar con esta matriz")
            print(" 6) Salir del programa completamente")
            opcion = input("Elige 1, 2, 3, 4, 5 o 6: ").strip()

            if opcion not in ("1","2","3","4","5","6"):
                print("Opción no válida. Intenta de nuevo.")
                continue

            if opcion == "1":
                sarrus_generalizado(A)
            elif opcion == "2":
                print("Has elegido Cramer. Ingresa vector b (n valores):")
                b = leer_fila_esperada(n, "Vector b: ")
                cramer_pasos(A, b)
            elif opcion == "3":
                determinante_pasos(A)
            elif opcion == "4":
                detA = sarrus_generalizado(A)
                if detA is None:
                    print("No se obtuvo det(A) con Sarrus. No se puede aplicar Cramer.")
                elif abs(detA) < 1e-12:
                    print("det(A) = 0 según Sarrus -> No existe solución única; Cramer no aplica.")
                else:
                    print("det(A) calculado por Sarrus =", int(round(detA)) if abs(detA-round(detA))<1e-9 else detA)
                    print("Ahora ingresa el vector b para aplicar Cramer:")
                    b = leer_fila_esperada(n, "Vector b: ")
                    soluciones = []
                    for i in range(n):
                        Ai = [row[:] for row in A]
                        for r in range(n):
                            Ai[r][i] = b[r]
                        print(f"\nCalculando det(A_{i+1}) (reemplazando columna {i+1} por b):")
                        mostrar_matriz(Ai)
                        detAi = determinante_pasos(Ai)
                        xi = detAi / detA
                        xi_out = int(round(xi)) if abs(xi-round(xi))<1e-9 else xi
                        detAi_out = int(round(detAi)) if abs(detAi-round(detAi))<1e-9 else detAi
                        detA_out = int(round(detA)) if abs(detA-round(detA))<1e-9 else detA
                        print(f"x{i+1} = det(A_{i+1}) / det(A) = {detAi_out} / {detA_out} = {xi_out}")
                        soluciones.append(xi)
                    print("\nSolución por Cramer usando det(A) calculado por Sarrus/generalizado:")
                    print([int(round(v)) if abs(v-round(v))<1e-9 else v for v in soluciones])
            elif opcion == "5":
                print("Finalizando operaciones sobre la matriz actual. Pasando a la siguiente (si la hay).")
                break
            elif opcion == "6":
                print("Saliendo del programa. !")
                return

    print("\nProceso finalizado.")

if __name__ == "__main__":
    main()
