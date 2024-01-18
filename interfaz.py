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

        #POBLACIÓN

        self.label = CTkLabel(self, text="Población")
        self.label.place(x=200, y=30)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="Pob. Minima:")
        self.label.place(x=35, y=65)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_pob_min = CTkEntry(self)
        self.entrada_pob_min.place(x=120, y=65)
        self.entrada_pob_min.configure(width=80, height=25)


        self.label = CTkLabel(self, text="Pob. Maxima:")
        self.label.place(x=235, y=65)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_pob_max = CTkEntry(self)
        self.entrada_pob_max.place(x=325, y=65)
        self.entrada_pob_max.configure(width=80, height=25)

        #MUTACIÓN

        self.label = CTkLabel(self, text="Mutación")
        self.label.place(x=200, y=110)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="%Mut. Ind:")
        self.label.place(x=50, y=140)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_mut_ind = CTkEntry(self)
        self.entrada_mut_ind.place(x=120, y=140)
        self.entrada_mut_ind.configure(width=80, height=25)

        self.label = CTkLabel(self, text="%Mut. gen:")
        self.label.place(x=250, y=140)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_mut_gen = CTkEntry(self)
        self.entrada_mut_gen.place(x=325, y=140)
        self.entrada_mut_gen.configure(width=80, height=25)

        #RESOLUCIÓN
        
        self.label = CTkLabel(self, text="Resolución")
        self.label.place(x=190, y=180)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="Resolución:")
        self.label.place(x=60, y=210)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))
 
        self.entrada_resolucion = CTkEntry(self)
        self.entrada_resolucion.place(x=140, y=210)
        self.entrada_resolucion.configure(width=220, height=25)

        self.boton_maximo = CTkButton(self, text="Maximo", command=self.set_maximo)
        self.boton_maximo.place(x=150, y=250)
        self.boton_maximo.configure(width=80, height=25)

        self.boton_minimo = CTkButton(self, text="Minimo", command=self.set_minimo)
        self.boton_minimo.place(x=250, y=250)
        self.boton_minimo.configure(width=80, height=25)
        self.resolucion_tipo = "max"  # Valor predeterminado

        self.label = CTkLabel(self, text="Rango")
        self.label.place(x=200, y=355)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="a:")
        self.label.place(x=120, y=390)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_a = CTkEntry(self)
        self.entrada_a.place(x=140, y=390)
        self.entrada_a.configure(width=80, height=25)

        self.label = CTkLabel(self, text="b:")
        self.label.place(x=240, y=390)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_b = CTkEntry(self)
        self.entrada_b.place(x=260, y=390)
        self.entrada_b.configure(width=80, height=25)

        #EVALUACIÓN

        self.label = CTkLabel(self, text="Criterios")
        self.label.place(x=200, y=290)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="Iteraciones:")
        self.label.place(x=145, y=325)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_iteraciones = CTkEntry(self)
        self.entrada_iteraciones.place(x=225, y=325)
        self.entrada_iteraciones.configure(width=80, height=25)

        self.boton = CTkButton(self, text="Realizar algoritmo", fg_color="#42B650")
        self.boton.place(x=180, y=440)
        self.boton.configure(width=80, height=25)

        self.boton = CTkButton(self, text="Realizar algoritmo", command=self.ejecutar_algoritmo_genetico, fg_color="#42B650")
        self.boton.place(x=180, y=440)
        self.boton.configure(width=80, height=25)
        
    def set_maximo(self):
        self.resolucion_tipo = "max"

    def set_minimo(self):
        self.resolucion_tipo = "min"


        #RANGO


    def ejecutar_algoritmo_genetico(self):
        # Obtener los valores ingresados por el usuario desde la interfaz
        poblacion_minima = int(self.entrada_pob_min.get())
        poblacion_maxima = int(self.entrada_pob_max.get())
        prob_mut_individuo = float(self.entrada_mut_ind.get())
        prob_mut_gen = float(self.entrada_mut_gen.get())
        resolucion = float(self.entrada_resolucion.get())
        tipo_resolucion = self.resolucion_tipo
        xa = float(self.entrada_a.get())
        xb = float(self.entrada_b.get())
        iteraciones = int(self.entrada_iteraciones.get())

        # Llamar a la función del algoritmo genético con los valores ingresados
        run_genetic_algorithm(poblacion_minima, poblacion_maxima, prob_mut_individuo,
                              prob_mut_gen, resolucion, tipo_resolucion, xa, xb, iteraciones)
        

        
mi_ventana = MiVentana()  # Crear la instancia de la ventana
mi_ventana.mainloop()  # Iniciar el bucle principal
