# pylint: disable=import-error
import bbdd.bbdd as base
import tkinter as tk

class Programa():

    def __init__(self,p_titulo,p_tamanio):
        self.raiz = tk.Tk()
        self.raiz.title(p_titulo)
        self.raiz.geometry(p_tamanio)
    
    def _iniciar(self):
        self._menu()
        self.raiz.mainloop()
    
    def _finalizar(self):
        self.raiz.destroy()

    def _menu(self):
        tk.Button(self.raiz,text="Iniciar",command=lambda:iniciar()).pack()

class interfazInicial(Programa):
    def __init__(self,p_titulo,p_tamanio):
        super().__init__(p_titulo,p_tamanio)
        self.usuario = tk.StringVar()
        self.contrasenia = tk.StringVar()

    def _menu(self):
        tk.Label(self.raiz,text="Usuario").pack()
        tk.Entry(self.raiz,textvalue=usuario).pack()
        tk.Label(self.raiz,text="Contraseña").pack()
        tk.Entry(self.raiz,textvalue=contrasenia).pack()
        tk.Button(self.raiz,text="Iniciar")

class interfazAlumno(Programa):
    def __init__(self,p_titulo,p_tamanio):
        super().__init__(p_titulo,p_tamanio)
    
    def _menu(self):
        tk.Button(self.raiz,text="Mis Datos").pack()
        tk.Button(self.raiz,text="Info Materias").pack()
        tk.Button(self.raiz,text="Info Docentes").pack()
        tk.Button(self.raiz,text="Cerrar sesion").pack()

class interfazDocente(Programa):
    def __init__(self,p_titulo,p_tamanio):
        super().__init__(p_titulo,p_tamanio)
    
    def _menu(self):
        tk.Button(self.raiz,text="Mis Datos").pack()
        tk.Button(self.raiz,text="Info Materias").pack()
        tk.Button(self.raiz,text="Info Estudiantes").pack()
        tk.Button(self.raiz,text="Cerrar sesion").pack()

def iniciar():
    inicioSesion = interfazInicial("Iniciar sesion","200x200")
    inicioSesion._iniciar()

programa = Programa("Inicio","100x100")
programa._iniciar()