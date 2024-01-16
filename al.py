import math
import random
import pandas as pd  

# Parámetros dados por el usuario
poblacion_inicial = 5
a = -8
b = -6
delta_x = 2/31
numero_saltos= 2/delta_x
numero_de_puntos = numero_saltos+1
poblacion_maxima = 10
probabilidad_mutacion_gen = 0.2
probabilidad_mutacion_individuo = 0.4
num_generaciones = 3  # Ajusta según tus necesidades
porcentaje_seleccion = 0.25  # Puedes ajustar este valor según tus necesidades
todas_generaciones = []
datos_estadisticos = []
tipo_problema = "max"  

mejor_individuo_global = None
mejor_evaluacion_global = float('inf') 

# Cálculos iniciales
rango = b - a
num_bits = math.ceil(math.log2(numero_de_puntos))

# Función objetivo f(x)
def f(x):
    return x**3 - x**3*math.cos(math.radians(5*x)) 

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




def evaluar_individuo(individuo, a, delta_x, tipo_problema):
    x = a + bin_to_decimal(individuo) * delta_x
    resultado = f(x)
    return resultado if tipo_problema == "min" else -resultado



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

def prune_population(poblacion, evaluaciones, poblacion_maxima):
    # Obtener índice del mejor individuo antes de la poda
    mejor_individuo_index = best_individual_index(evaluaciones, tipo_problema)

    # Eliminar individuos duplicados
    poblacion_ordenada = list(set(poblacion))

    # Mantener al mejor individuo después de la poda
    if mejor_individuo_index is not None:
        poblacion_ordenada.append(poblacion_ordenada.pop(mejor_individuo_index))

    # Realizar la poda para mantener el máximo número de individuos permitidos
    poblacion_final = poblacion_ordenada[:poblacion_maxima]

    return poblacion_final







def add_new_individuals(poblacion, nuevos_individuos):
    return poblacion + nuevos_individuos

def best_individual_index(evaluaciones, tipo_problema):
    if evaluaciones:
        if tipo_problema == "min":
            return evaluaciones.index(min(evaluaciones))
        elif tipo_problema == "max":
            return evaluaciones.index(max(evaluaciones))
    return None





# Inicialización de la población
poblacion = [generate_random_binary_string(
    num_bits) for _ in range(poblacion_inicial)]


# Algoritmo genético
for generacion in range(num_generaciones):
    evaluaciones = [evaluar_individuo(individuo, a, delta_x, tipo_problema) for individuo in poblacion]
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

# Seguimiento del mejor individuo en esta generación
    mejor_individuo_generacion = poblacion[best_individual_index(evaluaciones, tipo_problema)]
    if tipo_problema == "min":
        mejor_evaluacion_generacion = min(evaluaciones)
    else:
        mejor_evaluacion_generacion = max(evaluaciones)
        
        


          
    # Actualización del mejor individuo global si es necesario
    if tipo_problema == "min" and mejor_evaluacion_generacion < mejor_evaluacion_global:
        mejor_individuo_global = mejor_individuo_generacion
        mejor_evaluacion_global = mejor_evaluacion_generacion
    elif tipo_problema == "max" and mejor_evaluacion_generacion > mejor_evaluacion_global:
        mejor_individuo_global = mejor_individuo_generacion
        mejor_evaluacion_global = mejor_evaluacion_generacion




    print(f"Mejor individuo en esta generación: {mejor_individuo_generacion}, f(x): {mejor_evaluacion_generacion}")
    print(f"Mejor individuo global hasta ahora: {mejor_individuo_global}, f(x): {mejor_evaluacion_global}")


    

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
    # Almacena el mejor individuo y su evaluación antes de la mutación
    mejor_individuo_antes_mutacion = poblacion[best_individual_index(evaluaciones, tipo_problema)]
    mejor_evaluacion_antes_mutacion = min(evaluaciones) if tipo_problema == "min" else max(evaluaciones)


        # Evalúa la descendencia mutada
    evaluaciones_descendencia_mutada = [evaluar_individuo(individuo, a, delta_x, tipo_problema) for individuo in descendencia_mutada]

    # Encuentra el mejor individuo después de la mutación
    mejor_individuo_despues_mutacion = descendencia_mutada[best_individual_index(evaluaciones_descendencia_mutada, tipo_problema)]
    mejor_evaluacion_despues_mutacion = min(evaluaciones_descendencia_mutada) if tipo_problema == "min" else max(evaluaciones_descendencia_mutada)

    # Conserva el mejor individuo entre antes y después de la mutación
    if tipo_problema == "min" and mejor_evaluacion_despues_mutacion < mejor_evaluacion_antes_mutacion:
        mejor_individuo_global = mejor_individuo_despues_mutacion
        mejor_evaluacion_global = mejor_evaluacion_despues_mutacion
    elif tipo_problema == "max" and mejor_evaluacion_despues_mutacion > mejor_evaluacion_antes_mutacion:
       mejor_individuo_global = mejor_individuo_despues_mutacion
       mejor_evaluacion_global = mejor_evaluacion_despues_mutacion



    print("\nDescendencia después de mutación:")
    for i, individuo_mutado in enumerate(descendencia_mutada):
        x = a + bin_to_decimal(individuo_mutado) * delta_x
        posicion_individuo = bin_to_decimal(individuo_mutado)

        if descendencia[i] != individuo_mutado:
            print(f"{i + 1}: Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")
        else:
            print(f"{i + 1}: No Mutado - {individuo_mutado}, Posición (x): {round(x, 6)}, f(x): {round(f(x), 6)}, Posición Individuo: {posicion_individuo}")
    
    # Imprimir la tabla después de agregar nuevos descendientes
    print("\nPoblación después de mutación:")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
        "ID", "Individuo", "Posicion (x)", "f(x)", "Posicion Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))

        datos_generacion = {
            'ID': i + 1,
            'Individuo': individuo,
            'I': posicion_individuo,
            'x': round(x, 6),
            'f(x)': round(f(x), 6)
        }

        datos_estadisticos.append(datos_generacion)

    # DataFrame 
    df = pd.DataFrame(datos_estadisticos)
    
    if generacion == 0:
        # Guardar la generación 1 en el primer ciclo
        df.to_csv('datos_estadisticos_geneticos.csv', index=False)
    else:
        # Agregar las nuevas generaciones mutadas
        df.to_csv('datos_estadisticos_geneticos.csv', mode='a', header=False, index=False)
   
    # Poda de la población después de la mutación
    poblacion = prune_population(poblacion, evaluaciones, poblacion_maxima)

    # Imprimir la tabla después de la poda
    print("\nPoblación después de la poda:")
    print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
        "ID", "Individuo", "Posicion (x)", "f(x)", "Posicion Individuo"))

    for i, individuo in enumerate(poblacion):
        x = a + bin_to_decimal(individuo) * delta_x
        posicion_individuo = bin_to_decimal(individuo)
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))



# Después de todas las generaciones, imprimir el mejor individuo global
print("\nMejor individuo después de todas las generaciones:")
print("{:<10} {:<25} {:<15} {:<15}".format(
    "ID", "Individuo", "Posición (x)", "f(x)"))

# Ajusta la impresión según el tipo de problema
if mejor_individuo_global is not None:
    x_mejor_global = a + bin_to_decimal(mejor_individuo_global) * delta_x
    resultado_mejor_global = evaluar_individuo(mejor_individuo_global, a, delta_x, tipo_problema)

    if tipo_problema == "min":
        print("{:<10} {:<25} {:<15} {:<15}".format(1, mejor_individuo_global, round(x_mejor_global, 6), resultado_mejor_global))
    else:
        print("{:<10} {:<25} {:<15} {:<15}".format(1, mejor_individuo_global, round(x_mejor_global, 6), -resultado_mejor_global))
else:
    print("\nLa población está vacía después de todas las generaciones.")