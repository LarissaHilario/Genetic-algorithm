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
    mejores_indices = sorted(range(len(evaluaciones)),
                             key=lambda i: evaluaciones[i])[:2]

    nuevos_indices = random.sample(range(len(poblacion)), len(poblacion))
    while nuevos_indices[:2] == mejores_indices:
        nuevos_indices = random.sample(range(len(poblacion)), len(poblacion))

    return [poblacion[i] for i in nuevos_indices[:2]]

def crossover_multiple_points(nuevas_parejas, prob_mut_gen, num_bits):
    descendencia = []
    for i, pareja in enumerate(nuevas_parejas):
        padre, individuo = pareja
        num_cortes = random.randint(1, min(len(padre), len(individuo)))
        posiciones_cortes = sorted(random.sample(
            range(1, min(len(padre), len(individuo)) + 1), num_cortes))
        subcadena_padre = ''
        subcadena_individuo = ''
        alternar = True

        for j in range(len(posiciones_cortes) + 1):
            posicion_corte_inicial = 0 if j == 0 else posiciones_cortes[j - 1]
            posicion_corte_final = posiciones_cortes[j] if j < len(
                posiciones_cortes) else len(padre)

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

        descendencia.extend([subcadena_padre, subcadena_individuo])

        print(f"Pareja {i + 1}: Cortes en posición {posiciones_cortes} de Padre ({padre}) e Individuo ({individuo}) con {num_cortes} cortes")

    return descendencia

def mutate_sequence_swap_positions(individuo, prob_mut_individuo, prob_mut_gen):
    individuo_original = individuo
    individuo_mutado = ''
    posiciones_mutadas = []

    if random.random() < prob_mut_individuo:
        for i, bit in enumerate(individuo):
            if random.random() < prob_mut_gen:
                bit = '1' if bit == '0' else '0'
                posiciones_mutadas.append(i)

            individuo_mutado += bit

        if posiciones_mutadas:
            for bits_intercambiados in posiciones_mutadas:
                posicion1 = random.randint(0, len(individuo_mutado) - 1)
                print(f"Posición aleatoria para intercambio: {posicion1}")

                individuo_mutado = list(individuo_mutado)
                individuo_mutado[bits_intercambiados], individuo_mutado[posicion1] = individuo_mutado[posicion1], individuo_mutado[bits_intercambiados]
                individuo_mutado = ''.join(individuo_mutado)

            print(f"Individuo original: {individuo_original}, Individuo mutado: {individuo_mutado}, Bits intercambiados: {', '.join(map(str, posiciones_mutadas))}")
        else:
            print(f"Individuo original: {individuo_original}, No ocurrió mutación de genes")
    else:
        individuo_mutado = individuo_original
        print(f"Individuo original: {individuo_original}, No ocurrió mutación de individuo")

    return individuo_mutado

def add_new_individuals(poblacion, nuevos_individuos):
    return poblacion + nuevos_individuos

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
    evaluaciones = [f(a + bin_to_decimal(individuo) * delta_x) for individuo in poblacion]
    todas_generaciones.append(poblacion.copy())

    print(f"\nGeneración {generacion + 1}")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
        "ID", "Individuo", "Posicion (x)", "f(x)", "Posicion Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

    seleccionados = list(set(select_parents_percentage(poblacion, evaluaciones, porcentaje_seleccion)))
    print("\nMejores individuos:", seleccionados)

    combinaciones_realizadas = set()
    nuevas_parejas = []

    for i, padre in enumerate(seleccionados):
        for j, individuo in enumerate(poblacion):
            if padre != individuo and ((i, j) not in combinaciones_realizadas and (j, i) not in combinaciones_realizadas):
                nuevas_parejas.append((padre, individuo))
                combinaciones_realizadas.add((i, j))

    for i, pareja in enumerate(nuevas_parejas):
        print(f"Pareja {i + 1}: Padre = {pareja[0]}, Individuo = {pareja[1]}")

    descendencia = crossover_multiple_points(nuevas_parejas, probabilidad_mutacion_gen, num_bits)

    print("\nDescendencia después de cruza:")
    for i, ind in enumerate(descendencia):
        print(f"Descendiente {i + 1}: {ind}")

    descendencia_mutada = [mutate_sequence_swap_positions(individuo, probabilidad_mutacion_individuo, probabilidad_mutacion_gen) for individuo in descendencia]
 # Agregar nuevos individuos a la población existente
    poblacion = add_new_individuals(poblacion, descendencia_mutada)

    print("\nDescendencia después de mutación:")
    for i, individuo_mutado in enumerate(descendencia_mutada):
        x = a + bin_to_decimal(individuo_mutado) * delta_x
        posicion_individuo = bin_to_decimal(individuo_mutado)

        if descendencia[i] != individuo_mutado:
            print(f"{i + 1}: Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")
        else:
            print(f"{i + 1}: No Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")



#tabla de toda la población
    print(f"\nGeneración {generacion + 1}")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            "ID", "Individuo", "Posicion (x)", "f(x)", "Posicion Individuo"))

    for i, individuo in enumerate(poblacion):
            x = a + bin_to_decimal(individuo) * delta_x
            posicion_individuo = bin_to_decimal(individuo)
            print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
                i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

# Obtener el mejor individuo después de todas las generaciones
mejor_individuo_index = best_individual_index(evaluaciones)
if mejor_individuo_index is not None:
    mejor_individuo = poblacion[mejor_individuo_index]
    print("\nMejor individuo después de todas las generaciones:")
    print("{:<10} {:<25} {:<15} {:<15}".format(
        "ID", "Individuo", "Posición (x)", "f(x)"))
    x_mejor = a + bin_to_decimal(mejor_individuo) * delta_x
    print("{:<10} {:<25} {:<15} {:<15}".format(mejor_individuo_index , mejor_individuo, round(x_mejor, 6), round(f(x_mejor), 6)))
else:
    print("\nLa población está vacía después de todas las generaciones.")



# Poda después de todas las generaciones
mejor_individuo_index = best_individual_index(evaluaciones)
poblacion = [poblacion[mejor_individuo_index]]
evaluaciones = [evaluaciones[mejor_individuo_index]]

poblacion = list(set(poblacion))
while len(poblacion) < poblacion_maxima:
    nuevo_individuo = generate_random_binary_string(num_bits)
    if nuevo_individuo not in poblacion:
        poblacion.append(nuevo_individuo)
        evaluaciones.append(f(a + bin_to_decimal(nuevo_individuo) * delta_x))

print("\nPoblación después de la poda:")
print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
    "ID", "Individuo", "Posición (x)", "f(x)", "Posición Individuo"))

for i, individuo in enumerate(poblacion):
    x = a + bin_to_decimal(individuo) * delta_x
    posicion_individuo = bin_to_decimal(individuo)
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
        i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))
