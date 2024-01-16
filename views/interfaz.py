from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry


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

        self.entrada = CTkEntry(self)
        self.entrada.place(x=120, y=65)
        self.entrada.configure(width=80, height=25)

        self.label = CTkLabel(self, text="Pob. Maxima:")
        self.label.place(x=235, y=65)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=325, y=65)
        self.entrada.configure(width=80, height=25)

        #MUTACIÓN

        self.label = CTkLabel(self, text="Mutación")
        self.label.place(x=200, y=110)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="%Mut. Ind:")
        self.label.place(x=50, y=140)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=120, y=140)
        self.entrada.configure(width=80, height=25)

        self.label = CTkLabel(self, text="%Mut. gen:")
        self.label.place(x=250, y=140)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=325, y=140)
        self.entrada.configure(width=80, height=25)

        #RESOLUCIÓN
        
        self.label = CTkLabel(self, text="Resolución")
        self.label.place(x=190, y=180)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="Resolución:")
        self.label.place(x=60, y=210)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))
 
        self.entrada = CTkEntry(self)
        self.entrada.place(x=140, y=210)
        self.entrada.configure(width=220, height=25)

        self.boton = CTkButton(self, text="Maximo")
        self.boton.place(x=150, y=250)
        self.boton.configure(width=80, height=25)

        self.boton = CTkButton(self, text="Minimo")
        self.boton.place(x=250, y=250)
        self.boton.configure(width=80, height=25)

        #RANGO

        self.label = CTkLabel(self, text="Rango")
        self.label.place(x=200, y=355)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="a:")
        self.label.place(x=120, y=390)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=140, y=390)
        self.entrada.configure(width=80, height=25)

        self.label = CTkLabel(self, text="b:")
        self.label.place(x=240, y=390)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=260, y=390)
        self.entrada.configure(width=80, height=25)

        #EVALUACIÓN

        self.label = CTkLabel(self, text="Criterios")
        self.label.place(x=200, y=290)
        self.label.configure(font=("TkDefaultFont", 16, "bold"))

        self.label = CTkLabel(self, text="Iteraciones:")
        self.label.place(x=145, y=325)
        self.label.configure(font=("TkDefaultFont", 12, "bold"))

        self.entrada = CTkEntry(self)
        self.entrada.place(x=225, y=325)
        self.entrada.configure(width=80, height=25)

        self.boton = CTkButton(self, text="Realizar algoritmo", fg_color="#42B650")
        self.boton.place(x=180, y=440)
        self.boton.configure(width=80, height=25)

mi_ventana = MiVentana()  # Crear la instancia de la ventana
mi_ventana.mainloop()  # Iniciar el bucle principal
