import math
import random

# Parámetros dados por el usuario
poblacion_inicial = 4
a = 3
b = 5
numero_de_puntos = 31
poblacion_maxima = 8
probabilidad_mutacion_gen = 0.35
probabilidad_mutacion_individuo = 0.25
num_generaciones = 2  # Ajusta según tus necesidades
porcentaje_seleccion = 0.25  # Puedes ajustar este valor según tus necesidades
todas_generaciones = []
# Cálculos iniciales
rango = b - a
num_bits = math.ceil(math.log2(numero_de_puntos))
delta_x = rango / (2 ** num_bits)

# Función objetivo f(x)


def f(x):
    return x**3 - 2*x**2*math.cos(math.radians(x)) + 3

# Función para decodificar la cadena de bits a un número decimal


def bin_to_decimal(binary_str):
    if binary_str:
        return int(binary_str, 2)
    else:
        return 0  # Cambiar a un valor predeterminado o lanzar una excepción si es necesario

# Función para generar una cadena de bits aleatoria de longitud dada


def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))

# Función para ordenar la población según las evaluaciones


def sort_population(poblacion, evaluaciones):
    return [individuo for _, individuo in sorted(zip(evaluaciones, poblacion))]

# Función para seleccionar un porcentaje de los mejores individuos como padres


def select_parents_percentage(poblacion, evaluaciones, porcentaje):
    poblacion_ordenada = sort_population(poblacion, evaluaciones)
    num_padres = int(porcentaje * len(poblacion_ordenada))
    return poblacion_ordenada[:num_padres]

# Función de selección de padres (modificada para seleccionar siempre los dos mejores)


def select_parents(poblacion, evaluaciones, porcentaje):
    # Obtener los índices de los dos mejores individuos
    mejores_indices = sorted(range(len(evaluaciones)),
                             key=lambda i: evaluaciones[i])[:2]

    # Asegurarse de que los índices no se repitan
    nuevos_indices = random.sample(range(len(poblacion)), len(poblacion))
    while nuevos_indices[:2] == mejores_indices:
        nuevos_indices = random.sample(range(len(poblacion)), len(poblacion))

    return [poblacion[i] for i in nuevos_indices[:2]]


def crossover_multiple_points(nuevas_parejas, prob_mut_gen, num_bits):
    descendencia = []
    for i, pareja in enumerate(nuevas_parejas):
        padre, individuo = pareja

        # Obtener la cantidad aleatoria de cortes
        num_cortes = random.randint(1, min(len(padre), len(individuo)))

        # Seleccionar aleatoriamente las posiciones de los cortes
        posiciones_cortes = sorted(random.sample(
            range(1, min(len(padre), len(individuo)) + 1), num_cortes))

        # Inicializar las subcadenas de los padres
        subcadena_padre = ''
        subcadena_individuo = ''

        # Variable para alternar entre padres
        alternar = True

        # Realizar la cruza utilizando los cortes y posiciones seleccionados
        for j in range(len(posiciones_cortes) + 1):
            posicion_corte_inicial = 0 if j == 0 else posiciones_cortes[j - 1]
            posicion_corte_final = posiciones_cortes[j] if j < len(
                posiciones_cortes) else len(padre)

            # Alternar entre los padres para cada subcadena
            if alternar:
                subcadena_padre += str(
                    padre[posicion_corte_inicial:posicion_corte_final])
                subcadena_individuo += str(
                    individuo[posicion_corte_inicial:posicion_corte_final])
            else:
                subcadena_padre += str(
                    individuo[posicion_corte_inicial:posicion_corte_final])
                subcadena_individuo += str(
                    padre[posicion_corte_inicial:posicion_corte_final])

            alternar = not alternar

        # Combinar las subcadenas obtenidas de los padres
        descendencia.extend([subcadena_padre, subcadena_individuo])

        # Imprimir las posiciones y cortes realizados
        print(f"Pareja {i + 1}: Cortes en posición {posiciones_cortes} de Padre ({padre}) e Individuo ({individuo}) con {num_cortes} cortes")

    return descendencia


# Función de mutación con intercambio de posición de bits
def mutate_sequence_swap_positions(individuo, prob_mut_individuo, prob_mut_gen):
    individuo_original = individuo  # Guardar una copia del individuo original
    individuo_mutado = ''
    bits_intercambiados = None

    # Evaluación si el individuo debe mutar en su totalidad
    if random.random() < prob_mut_individuo:
        # Si el individuo debe mutar en su totalidad, realiza la mutación de genes
        # Evaluación para cada gen si debe mutar
        for i, bit in enumerate(individuo):
            if random.random() < prob_mut_gen:
                bit = '1' if bit == '0' else '0'

                # Si ocurre una mutación, registra las posiciones de bits intercambiados
                if bits_intercambiados is None:
                    bits_intercambiados = i

            individuo_mutado += bit

        if bits_intercambiados is not None:
            # Si ocurrió una mutación, intercambia bits en posiciones aleatorias
            posicion1 = random.randint(0, len(individuo_mutado) - 1)
            individuo_mutado = list(individuo_mutado)
            individuo_mutado[bits_intercambiados], individuo_mutado[
                posicion1] = individuo_mutado[posicion1], individuo_mutado[bits_intercambiados]
            individuo_mutado = ''.join(individuo_mutado)

            # Imprimir información de la mutación
            print(
                f"Individuo original: {individuo_original}, Individuo mutado: {individuo_mutado}, Bits intercambiados: {bits_intercambiados} y {posicion1}")
        else:
            # Imprimir información de la mutación
            print(
                f"Individuo original: {individuo_original}, No ocurrió mutación de genes")

    else:
        # Si el individuo no debe mutar en su totalidad, mantenerlo sin cambios
        individuo_mutado = individuo_original
        print(
            f"Individuo original: {individuo_original}, No ocurrió mutación de individuo")

    return individuo_mutado


# Función para agregar nuevos individuos a la población existente
def add_new_individuals(poblacion, nuevos_individuos):
    return poblacion + nuevos_individuos

# Función para encontrar el índice del mejor individuo


def best_individual_index(evaluaciones):
    if evaluaciones:
        return evaluaciones.index(min(evaluaciones))
    else:
        return None


# Inicialización de la población
poblacion = [generate_random_binary_string(
    num_bits) for _ in range(poblacion_inicial)]

# Algoritmo genético
for generacion in range(num_generaciones):
    # Evaluación de la función objetivo para cada individuo
    evaluaciones = [f(a + bin_to_decimal(individuo) * delta_x)
                    for individuo in poblacion]
    todas_generaciones.append(poblacion.copy())
    # Impresión de la tabla
    print(f"\nGeneración {generacion + 1}")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
        "ID", "Individuo", "Posición (x)", "f(x)", "Posición Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

    # Selección de individuos para reproducción (modificada para seleccionar un porcentaje de los mejores)
    # Modificación para eliminar duplicados de la lista de mejores individuos
    seleccionados = list(set(select_parents_percentage(
        poblacion, evaluaciones, porcentaje_seleccion)))

    # Imprimir las parejas de padres
    print("\nMejores individuos:", seleccionados)

    # Inicializar un conjunto para realizar un seguimiento de las combinaciones
    combinaciones_realizadas = set()

    # Generar nuevas parejas de padres sin duplicados y evitando combinaciones consigo mismos
    nuevas_parejas = []

    for i, padre in enumerate(seleccionados):
        for j, individuo in enumerate(poblacion):
            # Evitar combinaciones consigo mismos y duplicados
            if padre != individuo and ((i, j) not in combinaciones_realizadas and (j, i) not in combinaciones_realizadas):
                nuevas_parejas.append((padre, individuo))
                # Registrar la combinación realizada
                combinaciones_realizadas.add((i, j))

    # Imprimir las nuevas parejas de padres
    for i, pareja in enumerate(nuevas_parejas):
        print(f"Pareja {i + 1}: Padre = {pareja[0]}, Individuo = {pareja[1]}")

    # Aplicar cruza a las nuevas parejas de padres con múltiples puntos de cruza
    descendencia = crossover_multiple_points(
        nuevas_parejas, probabilidad_mutacion_gen, num_bits)

    # Imprimir la descendencia y los puntos de cruza seleccionados
    print("\nDescendencia después de cruza:")
    for i, ind in enumerate(descendencia):
        print(f"Descendiente {i + 1}: {ind}")

    # Aplicar mutación a la descendencia
    descendencia_mutada = [mutate_sequence_swap_positions(
        individuo, probabilidad_mutacion_individuo, probabilidad_mutacion_gen) for individuo in descendencia]

 # Agregar nuevos individuos a la población existente
    poblacion = add_new_individuals(poblacion, descendencia_mutada)
    # Impresión de la descendencia después de la mutación
    print("\nDescendencia después de mutación:")
    for i, individuo_mutado in enumerate(descendencia_mutada):
        x = a + bin_to_decimal(individuo_mutado) * delta_x
        posicion_individuo = bin_to_decimal(individuo_mutado)

        if descendencia[i] != individuo_mutado:
            print(f"{i + 1}: Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")
        else:
            print(f"{i + 1}: No Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")

    # Obtener el mejor individuo después de todas las generaciones
    mejor_individuo_index = best_individual_index(evaluaciones)
    if mejor_individuo_index is not None:
        mejor_individuo = poblacion[mejor_individuo_index]
        print("\nMejor individuo después de todas las generaciones:")
        print("{:<10} {:<25} {:<15} {:<15}".format(
            "ID", "Individuo", "Posición (x)", "f(x)"))
        x_mejor = a + bin_to_decimal(mejor_individuo) * delta_x
        print("{:<10} {:<25} {:<15} {:<15}".format(mejor_individuo_index +
              1, mejor_individuo, round(x_mejor, 6), round(f(x_mejor), 6)))
    else:
        print("\nLa población está vacía después de todas las generaciones.")
