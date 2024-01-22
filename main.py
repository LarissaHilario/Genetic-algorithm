from customtkinter import CTk, CTkLabel
from customtkinter import *
from algoritmo.algortimo import run_genetic_algorithm
from algoritmo.algortimo import generate_video
class MiVentana(CTk):

    button_a_enabled = True
    button_b_enabled = True

    
    
    def __init__(self):
        super().__init__()

        # Personalizar la apariencia de la ventana
        self.title("Algoritmos Geneticos")
        self.geometry("660x440")  # Tamaño inicial de la ventana
        self.resizable(False, False)  # Evitar que se redimensione

        labelResolucion = CTkLabel(self, text="Resolución", text_color="#FF6EE5")
        labelResolucion.place(x=200, y=20)
        labelResolucion.configure(font=("TkDefaultFont", 16, "bold"))

        labelReso = CTkLabel(self, text="Resolución:", text_color="#000000")
        labelReso.place(x=40, y=60)
        labelReso.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_resolucion = CTkEntry(self, placeholder_text="Resolución", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_resolucion.place(x=120, y=60)
        self.entrada_resolucion.configure(width=220, height=25)

        boton_maximo = CTkButton(self, text="Maximo", fg_color="#FF6EE5", text_color="#FFFFFF", hover_color="#FF85E9")
        boton_maximo.place(x=150, y=95)
        boton_maximo.configure(width=80, height=25, font=("Arial", 12, "bold"))

        boton_minimo = CTkButton(self, text="Minimo", fg_color="#FF6EE5", text_color="#FFFFFF", hover_color="#FF85E9" )
        boton_minimo.place(x=250, y=95)
        boton_minimo.configure(width=80, height=25, font=("Arial", 12, "bold"))
        
        self.resolucion_tipo= "max"

        labelSeleccionMaximo = CTkLabel(self, text="* Seleccionaste Maximo", text_color="#FF85E9")
        labelSeleccionMinimo = CTkLabel(self, text="* Seleccionaste Maximo", text_color="#FF85E9")

        def on_button_a_click():
            if MiVentana.button_b_enabled:  # Acceder a la variable a través de la clase
                MiVentana.button_b_enabled = False
                boton_minimo.configure(state="disabled")
                labelSeleccionMaximo.configure(text="* Seleccionaste Maximo")
                self.resolucion_tipo = "max"
                labelSeleccionMaximo.place(x=340, y=95)
                labelSeleccionMaximo.configure(font=("TkDefaultFont", 8, "bold"))
            else:
                MiVentana.button_b_enabled = True
                boton_minimo.configure(state="normal")
                labelSeleccionMaximo.configure(text="")
       
        boton_maximo.configure(command=on_button_a_click)

        def on_button_b_click():
            if MiVentana.button_a_enabled:  # Acceder a la variable a través de la clase
                MiVentana.button_a_enabled = False
                boton_maximo.configure(state="disabled")
                labelSeleccionMinimo.configure(text="* Seleccionaste Minimo")
                self.resolucion_tipo = "min"
                labelSeleccionMinimo.place(x=340, y=95)
                labelSeleccionMinimo.configure(font=("TkDefaultFont", 8, "bold"))
            else:
                MiVentana.button_a_enabled = True
                boton_maximo.configure(state="normal")
                labelSeleccionMinimo.configure(text="")

        boton_minimo.configure(command=on_button_b_click)

        #POBLACIÓN

        labelPoblacion = CTkLabel(self, text="Población", text_color="#FF6EE5")
        labelPoblacion.place(x=180, y=150)
        labelPoblacion.configure(font=("TkDefaultFont", 16, "bold"))

        labelPob_Min = CTkLabel(self, text="Pob. Minima:", text_color="#000000")
        labelPob_Min.place(x=80, y=185)
        labelPob_Min.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_pob_min = CTkEntry(self, placeholder_text="Población Min.", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_pob_min.place(x=165, y=185)
        self.entrada_pob_min.configure(width=175, height=25)

        def solo_numeros(entrada):
            """Valida que la entrada solo contenga dígitos."""
            if entrada.isdigit():
                return True  # Permitir la entrada
            else:
                return False

        self.solo_numeros = solo_numeros        

        labelPob_Max = CTkLabel(self, text="Pob. Maxima:", text_color="#000000")
        labelPob_Max.place(x=80, y=225)
        labelPob_Max.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_pob_max = CTkEntry(self, placeholder_text="Población Max.", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_pob_max.place(x=165, y=225)
        self.entrada_pob_max.configure(width=175, height=25)
            

        #MUTACIÓN

        labelMutacion = CTkLabel(self, text="Mutación", text_color="#FF6EE5")
        labelMutacion.place(x=480, y=150)
        labelMutacion.configure(font=("TkDefaultFont", 16, "bold"))

        labelMut_Ind = CTkLabel(self, text="%Mut. ind:", text_color="#000000")
        labelMut_Ind.place(x=380, y=185)
        labelMut_Ind.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_mut_ind = CTkEntry(self, placeholder_text="%Mut. Ind.", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_mut_ind.place(x=450, y=185)
        self.entrada_mut_ind.configure(width=170, height=25)

        labelMut_gen = CTkLabel(self, text="%Mut. gen:", text_color="#000000")
        labelMut_gen.place(x=380, y=225)
        labelMut_gen.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_mut_gen = CTkEntry(self, placeholder_text="%Mut. Gen.", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_mut_gen.place(x=450, y=225)
        self.entrada_mut_gen.configure(width=170, height=25)

        #RANGO

        labelRango = CTkLabel(self, text="Rangos", text_color="#FF6EE5")
        labelRango.place(x=500, y=20)
        labelRango.configure(font=("TkDefaultFont", 16, "bold"))

        label_A = CTkLabel(self, text="A:", text_color="#000000")
        label_A.place(x=410, y=60)
        label_A.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_a = CTkEntry(self, placeholder_text="A", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_a.place(x=430, y=60)
        self.entrada_a.configure(width=80, height=25)

        label_B = CTkLabel(self, text="B:", text_color="#000000")
        label_B.place(x=520, y=60)
        label_B.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_b = CTkEntry(self, placeholder_text="B", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_b.place(x=540, y=60)
        self.entrada_b.configure(width=80, height=25)

        #EVALUACIÓN

        labelCriterios = CTkLabel(self, text="Iteraciones", text_color="#FF6EE5")
        labelCriterios.place(x=320, y=280)
        labelCriterios.configure(font=("TkDefaultFont", 16, "bold"))

        labelIteraciones = CTkLabel(self, text="Iteraciones:", text_color="#000000")
        labelIteraciones.place(x=200, y=320)
        labelIteraciones.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada_iteraciones = CTkEntry(self, placeholder_text="Num. iteraciones", border_color="#FF85E9", placeholder_text_color="#FFAFF1", fg_color="#FFFFFF", text_color="#000000")
        self.entrada_iteraciones.place(x=275, y=320)
        self.entrada_iteraciones.configure(width=170, height=25)

        botonAlgoritmos = CTkButton(self, text="Realizar algoritmo", fg_color="#FF6EE5", text_color="#FFFFFF", hover_color="#FF85E9")
        botonAlgoritmos.place(x=260, y=370)
        botonAlgoritmos.configure(width=200, height=30, font=("Arial", 12, "bold"))
        botonAlgoritmos.configure(command=self.ejecutar_algoritmo_genetico)

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
            generate_video(images_path="./utilities", iteraciones= iteraciones, output_path="./utilities/evolution_video.mp4", fps=2)

        
        

mi_ventana = MiVentana() # Crear la instancia de la ventana
mi_ventana.configure(fg_color="#FCF7FB")
mi_ventana.mainloop()  # Iniciar el bucle principal
