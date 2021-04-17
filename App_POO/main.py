# pylint: disable=import-error

import bbdd.bbdd as base
import clases.clases as clase
import tkinter as tk

class InicioSesion(tk.Frame):

    def __init__(self,root):
        self.root = root
        self.root.title("Inicio sesion")
        self.root.geometry("300x150")
        self.usuario = tk.StringVar(self.root)
        self.contrasenia = tk.StringVar(self.root)
        tk.Label(self.root,text="Usuario: ").pack()
        tk.Entry(self.root, textvariable=self.usuario).pack()
        tk.Label(self.root,text="Contraseña: ").pack()
        tk.Entry(self.root, show="*",textvariable=self.contrasenia).pack()
        tk.Button(self.root,text="Iniciar sesion",command=lambda:self.obtenerDatos()).pack()
    
    def iniciar(self):
        self.root.mainloop()
    
    def cerrar(self):
        self.root.destroy()
        return True
    
    def obtenerDatos(self):
        datos = {}
        datos["usuario"] = self.usuario.get()
        datos["contraseña"] = self.contrasenia.get()
        print(datos)
        if datos["usuario"] == "emiliano" and datos["contraseña"] == "emi123":
            self.cerrar()

raiz = tk.Tk()
sesion = InicioSesion(raiz)
sesion.iniciar()