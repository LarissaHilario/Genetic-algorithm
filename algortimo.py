import random
import math

# Parámetros dados por el usuario
poblacion_inicial = 4
a = 3
b = 5
numero_de_puntos = 31
poblacion_maxima = 8
probabilidad_cruza = 0.75
probabilidad_mutacion_gen = 0.35
probabilidad_mutacion_individuo = 0.25
punto_cruza = 3
num_generaciones = 2  # Ajusta según tus necesidades
porcentaje_seleccion = 0.25  # Puedes ajustar este valor según tus necesidades

# Cálculos iniciales
rango = b - a
num_bits = math.ceil(math.log2(numero_de_puntos))
delta_x = rango / (2 ** num_bits)

# Función objetivo f(x)
def f(x):
    return x**3 - 2*x**2*math.cos(math.radians(x)) + 3

# Función para decodificar la cadena de bits a un número decimal
def bin_to_decimal(binary_str):
    return int(binary_str, 2)

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
    mejores_indices = sorted(range(len(evaluaciones)), key=lambda i: evaluaciones[i])[:2]
    return [poblacion[i] for i in mejores_indices]

# Función de cruza (punto de cruza, modificada para evitar combinar los dos mejores)
def crossover(padres, prob_cruza, punto_cruza):
    descendencia = []
    for i in range(0, len(padres), 2):
        padre1 = padres[i]
        padre2 = padres[i + 1]
        if random.random() < prob_cruza:
            hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
            hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]
        else:
            hijo1, hijo2 = padre1, padre2
        descendencia.extend([hijo1, hijo2])
    return descendencia

# Función de mutación
def mutate(descendencia, prob_mut_gen, prob_mut_individuo):
    descendencia_mutada = []
    for individuo in descendencia:
        individuo_original = individuo  # Guardar una copia del individuo original
        individuo_mutado = ''

        for bit in individuo:
            if random.random() < prob_mut_gen:
                bit = '1' if bit == '0' else '0'

            individuo_mutado += bit

        if random.random() < prob_mut_individuo:
            punto_mutacion = random.randint(0, len(individuo_mutado) - 1)
            individuo_mutado = individuo_mutado[:punto_mutacion] + random.choice('01') + individuo_mutado[punto_mutacion + 1:]

        descendencia_mutada.append(individuo_mutado)

        # Verificar si el individuo ha mutado
        if individuo_original != individuo_mutado:
            print(f"Individuo original: {individuo_original}, Individuo mutado: {individuo_mutado}, ¡El individuo ha mutado!")

    return descendencia_mutada

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
poblacion = [generate_random_binary_string(num_bits) for _ in range(poblacion_inicial)]

# Algoritmo genético
for generacion in range(num_generaciones):
    # Evaluación de la función objetivo para cada individuo
    evaluaciones = [f(a + bin_to_decimal(individuo) * delta_x) for individuo in poblacion]

    # Impresión de la tabla
    print(f"\nGeneración {generacion + 1}")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format("ID", "Individuo", "Posición (x)", "f(x)", "Posición Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

    # Selección de individuos para reproducción (modificada para seleccionar un porcentaje de los mejores)
    seleccionados = select_parents_percentage(poblacion, evaluaciones, porcentaje_seleccion)

    # Imprimir las parejas de padres
    print("\nMejores individuos:", seleccionados)
    
    # Inicializar un conjunto para realizar un seguimiento de las combinaciones
    combinaciones_realizadas = set()

    # Generar nuevas parejas de padres sin duplicados y evitando combinaciones consigo mismos
    nuevas_parejas = []

    for i, padre in enumerate(seleccionados):
        for j, individuo in enumerate(poblacion):
            # Evitar combinaciones consigo mismos y duplicados
            if padre != individuo  and ((i, j) not in combinaciones_realizadas and (j, i) not in combinaciones_realizadas):
                nuevas_parejas.append((padre, individuo))
                # Registrar la combinación realizada
                combinaciones_realizadas.add((i, j))

    # Imprimir las nuevas parejas de padres
    for i, pareja in enumerate(nuevas_parejas):
        print(f"Pareja {i + 1}: Padre = {pareja[0]}, Individuo = {pareja[1]}")

    # Aplicar cruza a las nuevas parejas de padres
    descendencia = []
    for pareja in nuevas_parejas:
        descendencia.extend(crossover(pareja, probabilidad_cruza, punto_cruza))

    # Aplicar mutación a la descendencia
    descendencia_mutada = mutate(descendencia, probabilidad_mutacion_gen, probabilidad_mutacion_individuo)

    # Agregar nuevos individuos a la población existente
    poblacion = add_new_individuals(poblacion, descendencia_mutada)

# Obtener el mejor individuo después de todas las generaciones
mejor_individuo_index = best_individual_index(evaluaciones)
if mejor_individuo_index is not None:
    mejor_individuo = poblacion[mejor_individuo_index]
    print("\nMejor individuo después de todas las generaciones:")
    print("{:<10} {:<25} {:<15} {:<15}".format("ID", "Individuo", "Posición (x)", "f(x)"))
    x_mejor = a + bin_to_decimal(mejor_individuo) * delta_x
    print("{:<10} {:<25} {:<15} {:<15}".format(mejor_individuo_index + 1, mejor_individuo, round(x_mejor, 6), round(f(x_mejor), 6)))
else:
    print("\nLa población está vacía después de todas las generaciones.")
