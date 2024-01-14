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
num_generaciones = 5  # Ajusta según tus necesidades

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

# Función de selección de padres (ruleta)
def select_parents(poblacion, evaluaciones):
    total_evaluaciones = sum(evaluaciones)
    prob_seleccion = [evaluacion / total_evaluaciones for evaluacion in evaluaciones]
    seleccionados_indices = random.choices(range(len(poblacion)), weights=prob_seleccion, k=len(poblacion))
    return [poblacion[i] for i in seleccionados_indices]

# Función de cruza (punto de cruza)
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
        individuo_mutado = ''
        for bit in individuo:
            if random.random() < prob_mut_gen:
                bit = '1' if bit == '0' else '0'
            individuo_mutado += bit
        if random.random() < prob_mut_individuo:
            punto_mutacion = random.randint(0, len(individuo_mutado) - 1)
            individuo_mutado = individuo_mutado[:punto_mutacion] + random.choice('01') + individuo_mutado[punto_mutacion + 1:]
        descendencia_mutada.append(individuo_mutado)
    return descendencia_mutada

# Función de reemplazo de población (reemplazo generacional)
def replace_population(poblacion, descendencia_mutada):
    return descendencia_mutada

# Función para encontrar el índice del mejor individuo
def best_individual_index(evaluaciones):
    return evaluaciones.index(min(evaluaciones))

# Inicialización de la población
poblacion = [generate_random_binary_string(num_bits) for _ in range(poblacion_inicial)]

# Algoritmo genético
for generacion in range(num_generaciones):
    # Evaluación de la función objetivo para cada individuo
    evaluaciones = [f(a + bin_to_decimal(individuo) * delta_x) for individuo in poblacion]

    # Impresión de la tabla
    print(f"Generación {generacion + 1}")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format("ID", "Individuo", "Posición (x)", "f(x)", "Posición Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

    # Selección de individuos para reproducción (ruleta)
    seleccionados = select_parents(poblacion, evaluaciones)

    # Aplicar cruza a los seleccionados
    descendencia = crossover(seleccionados, probabilidad_cruza, punto_cruza)

    # Aplicar mutación a la descendencia
    descendencia_mutada = mutate(descendencia, probabilidad_mutacion_gen, probabilidad_mutacion_individuo)

    # Reemplazar la población actual con la nueva generación
    poblacion = replace_population(poblacion, descendencia_mutada)

# Obtener el mejor individuo después de todas las generaciones
mejor_individuo = poblacion[best_individual_index(evaluaciones)]

# Mostrar resultados finales
print("\nMejor individuo después de todas las generaciones:")
print("{:<10} {:<25} {:<15} {:<15}".format("ID", "Individuo", "Posición (x)", "f(x)"))
x_mejor = a + bin_to_decimal(mejor_individuo) * delta_x
print("{:<10} {:<25} {:<15} {:<15}".format(1, mejor_individuo, round(x_mejor, 6), round(f(x_mejor), 6)))
