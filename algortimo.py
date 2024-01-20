import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Función
def f(x):
    return x**3 - x**3 * math.cos(math.radians(5 * x))

# decodificar la cadena de bits a un número decimal
def bin_to_decimal(binary_str):
    if binary_str:
        return int(binary_str, 2)
    else:
        return 0  # Cambiar a un valor predeterminado o lanzar una excepción si es necesario

# generar una cadena de bits aleatoria de longitud de bits
def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))

# Función para ordenar la población según las evaluaciones
def sort_population(poblacion, evaluaciones):
    return [individuo for _, individuo in sorted(zip(evaluaciones, poblacion))]

# Función para seleccionar un porcentaje de los mejores individuos como padres
def select_parents_percentage(poblacion, evaluaciones, porcentaje, tipo_problema):
    poblacion_ordenada = sort_population(poblacion, evaluaciones)

    if tipo_problema == "min":
        num_padres = int(porcentaje * len(poblacion_ordenada))
        # Selecciona los primeros num_padres individuos (los de evaluaciones más bajas)
        return poblacion_ordenada[:num_padres]
    else:
        num_padres = int(porcentaje * len(poblacion_ordenada))
        # Selecciona los últimos num_padres individuos (los de evaluaciones más altas)
        return poblacion_ordenada[-num_padres:]

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
                individuo_mutado[bits_intercambiados], individuo_mutado[
                    posicion1] = individuo_mutado[posicion1], individuo_mutado[bits_intercambiados]
                individuo_mutado = ''.join(individuo_mutado)

            print(
                f"Individuo original: {individuo_original}, Individuo mutado: {individuo_mutado}, Bits intercambiados: {', '.join(map(str, posiciones_mutadas))}")
        else:
            print(
                f"Individuo original: {individuo_original}, No ocurrió mutación de genes")
    else:
        individuo_mutado = individuo_original
        print(
            f"Individuo original: {individuo_original}, No ocurrió mutación de individuo")

    return individuo_mutado

def prune_population(poblacion, evaluaciones, poblacion_maxima, tipo_problema):
    mejor_individuo_mutado_index = best_individual_index(
        evaluaciones, tipo_problema)
    mejor_individuo_mutado = poblacion[mejor_individuo_mutado_index]

    poblacion_ordenada = list(set(poblacion))
    poblacion_ordenada.remove(mejor_individuo_mutado)

    # Si la población es mayor al límite permitido, eliminar individuos al azar
    if len(poblacion_ordenada) > poblacion_maxima - 1:
        num_individuos_a_eliminar = len(
            poblacion_ordenada) - (poblacion_maxima - 1)
        poblacion_ordenada = random.sample(
            poblacion_ordenada, poblacion_maxima - 1)

    # Añadir de nuevo al mejor individuo después de la mutación
    poblacion_ordenada.append(mejor_individuo_mutado)

    return poblacion_ordenada

def add_new_individuals(poblacion, nuevos_individuos):
    return poblacion + nuevos_individuos

def best_individual_index(evaluaciones, tipo_problema):
    if tipo_problema == "min":
        return evaluaciones.index(min(evaluaciones))
    else:
        return evaluaciones.index(max(evaluaciones))

def plot_population(todas_generaciones, a, b, delta_x, f, mejor_individuo_global, evolucion_mejor, evolucion_promedio, evolucion_peor, tipo_problema):
    # Crear puntos x y y para la función objetivo
    x_vals = np.arange(1, len(todas_generaciones) + 1)  # Números de generación en el eje x

    # Obtener los valores de fitness para cada generación
    fitness_mejor = [min([f(a + bin_to_decimal(individuo) * delta_x) for individuo in generacion]) if tipo_problema == "min" else max([f(a + bin_to_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones]
    fitness_promedio = [np.mean([f(a + bin_to_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones]
    fitness_peor = [max([f(a + bin_to_decimal(individuo) * delta_x) for individuo in generacion]) if tipo_problema == "min" else min([f(a + bin_to_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones]

    # Añadir los valores a las listas de evolución
    evolucion_mejor.append(fitness_mejor)
    evolucion_promedio.append(fitness_promedio)
    evolucion_peor.append(fitness_peor)

    # Graficar la evolución del mejor, promedio y peor
    plt.plot(x_vals, evolucion_mejor[-1], label='Mejor Individuo', color='green', marker='o')
    plt.plot(x_vals, evolucion_promedio[-1], label='Promedio Individuos', color='blue', marker='s')
    plt.plot(x_vals, evolucion_peor[-1], label='Peor Individuo', color='red', marker='^')

    # Resaltar el mejor individuo global
    mejor_x = a + bin_to_decimal(mejor_individuo_global) * delta_x
    mejor_y = f(mejor_x)
    plt.scatter(len(todas_generaciones), mejor_y, color='red', marker='*', label='Mejor Individuo Global')

    # Añadir etiquetas y leyenda
    plt.xlabel('Generación')
    plt.ylabel('f(x)')
    plt.xticks(x_vals)  # Mostrar solo números enteros en el eje x
    plt.legend()

    # Mostrar la gráfica
    plt.show()




def run_genetic_algorithm(poblacion_minima, poblacion_maxima, prob_mut_individuo, prob_mut_gen, resolucion, tipo_resolucion, xa, xb, iteraciones):
    a = xa
    b = xb
    poblacion_inicial = poblacion_minima
    poblacion_maxima = poblacion_maxima
    delta_x = resolucion
    porcentaje_seleccion = 0.25
    num_generaciones = iteraciones
    tipo_problema = tipo_resolucion
    rango = b - a
    num_saltos = rango/delta_x
    numero_de_puntos = num_saltos + 1
    todas_generaciones = []
    datos_estadisticos = []
    probabilidad_mutacion_individuo = prob_mut_individuo
    probabilidad_mutacion_gen = prob_mut_gen
    mejor_individuo_global = None
    mejor_evaluacion_global = float('inf')
    evolucion_mejor = []
    evolucion_promedio = []
    evolucion_peor = []
    num_bits = math.ceil(math.log2(num_saltos))
    delta_x1 = rango / ((2**num_bits) - 1)
    mejor_individuo_global = None
    mejor_evaluacion_global = float('inf')

    if delta_x1 < delta_x:
        delta_x = delta_x1

    poblacion = [generate_random_binary_string(num_bits) for _ in range(poblacion_inicial)]

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

        seleccionados = list(set(select_parents_percentage(
            poblacion, evaluaciones, porcentaje_seleccion, tipo_problema)))
        print("\nMejores individuos:", seleccionados)

        mejor_individuo_generacion_index = best_individual_index(
            evaluaciones, tipo_problema)
        mejor_individuo_generacion = poblacion[mejor_individuo_generacion_index]
        mejor_evaluacion_generacion = evaluaciones[mejor_individuo_generacion_index]

        # Actualización del mejor individuo global si es necesario
        if tipo_problema == "min" and mejor_evaluacion_generacion < mejor_evaluacion_global:
            mejor_individuo_global = mejor_individuo_generacion
            mejor_evaluacion_global = mejor_evaluacion_generacion
        elif tipo_problema == "max" and mejor_evaluacion_generacion > mejor_evaluacion_global:
            mejor_individuo_global = mejor_individuo_generacion
            mejor_evaluacion_global = mejor_evaluacion_generacion

        print(
            f"Mejor individuo en esta generación: {mejor_individuo_generacion}, f(x): {mejor_evaluacion_generacion}")
        print(
            f"Mejor individuo global hasta ahora: {mejor_individuo_global}, f(x): {mejor_evaluacion_global}")

        combinaciones_realizadas = set()
        nuevas_parejas = []

        for i, padre in enumerate(seleccionados):
            for j, individuo in enumerate(poblacion):
                if padre != individuo and ((i, j) not in combinaciones_realizadas and (j, i) not in combinaciones_realizadas):
                    nuevas_parejas.append((padre, individuo))
                    combinaciones_realizadas.add((i, j))

        for i, pareja in enumerate(nuevas_parejas):
            print(
                f"Pareja {i + 1}: Padre = {pareja[0]}, Individuo = {pareja[1]}")

        descendencia = crossover_multiple_points(
            nuevas_parejas, probabilidad_mutacion_gen, num_bits)

        print("\nDescendencia después de cruza:")
        for i, ind in enumerate(descendencia):
            print(f"Descendiente {i + 1}: {ind}")

        descendencia_mutada = [mutate_sequence_swap_positions(
            individuo, probabilidad_mutacion_individuo, probabilidad_mutacion_gen) for individuo in descendencia]
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
            df.to_csv('datos_estadisticos_geneticos.csv',
                      mode='a', header=False, index=False)

        poblacion = prune_population(
            poblacion, evaluaciones, poblacion_maxima, tipo_problema)


        print("\nPoblación después de la poda:")
        print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
            "ID", "Individuo", "Posicion (x)", "f(x)", "Posicion Individuo"))

        for i, individuo in enumerate(poblacion):
            x = a + bin_to_decimal(individuo) * delta_x
            posicion_individuo = bin_to_decimal(individuo)
            print("{:<10} {:<25} {:<15} {:<15} {:<15}".format(
                i + 1, individuo, round(x, 6), round(f(x), 6), posicion_individuo))
        # Llamar a la función plot_population con el mejor individuo global
    plot_population(todas_generaciones, a, b, delta_x, f, mejor_individuo_global, evolucion_mejor, evolucion_promedio, evolucion_peor, tipo_problema)

            
