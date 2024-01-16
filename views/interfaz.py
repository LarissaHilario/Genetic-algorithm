from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry
from algortimo import run_genetic_algorithm

class MiVentana(CTk):

    def __init__(self):
        super().__init__()

        # Personalizar la apariencia de la ventana
        self.title("Algoritmos Geneticos")
        self.configure(background="lightblue") 
        self.geometry("460x500")  # Tamaño inicial de la ventana
        self.resizable(False, False)  # Evitar que se redimensione

        self.boton = CTkButton(self, text="Realizar algoritmo", command=self.ejecutar_algoritmo, fg_color="#42B650")
        self.boton.place(x=180, y=440)
        self.boton.configure(width=80, height=25)

    def ejecutar_algoritmo(self):
        # Obtener valores del usuario
        poblacion_minima = int(self.entrada_pob_minima.get())
        poblacion_maxima = int(self.entrada_pob_maxima.get())
        prob_mut_individuo = float(self.entrada_mut_ind.get())
        prob_mut_gen = float(self.entrada_mut_gen.get())
        resolucion = int(self.entrada_resolucion.get())
        tipo_resolucion = "Maximo" if self.boton_maximo.is_selected() else "Minimo"
        a = float(self.entrada_a.get())
        b = float(self.entrada_b.get())

        # Run the genetic algorithm
        result = run_genetic_algorithm(poblacion_minima, poblacion_maxima, prob_mut_individuo, prob_mut_gen, resolucion, tipo_resolucion, a, b)

        # Handle the result as needed (e.g., display it in the GUI)
        print("\nMejor individuo después de todas las generaciones:")
        print("{:<10} {:<25} {:<15} {:<15}".format("ID", "Individuo", "Posición (x)", "f(x)"))
        print("{:<10} {:<25} {:<15} {:<15}".format(*result))

# Crear la instancia de la ventana
mi_ventana = MiVentana()
# Iniciar el bucle principal
mi_ventana.mainloop()