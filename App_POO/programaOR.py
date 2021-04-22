# pylint: disable=import-error
import bbdd.bbdd as base
import tkinter as tk
import clases.clases as clase

class Programa(tk.Frame):

    def __init__(self,p_titulo,p_tamanio,p_sesion):
        self.raiz = tk.Tk()
        self.raiz.title(p_titulo)
        self.raiz.geometry(p_tamanio)
        self.sesion = p_sesion
    
    def _iniciar(self):
        self._menu()
        self.raiz.mainloop()
    
    def _finalizar(self,p_salida):
        self.raiz.destroy()

    def _menu(self):
        pass  

class interfazInicial(Programa):
    def __init__(self,p_titulo,p_tamanio,p_sesion):
        super().__init__(p_titulo,p_tamanio,p_sesion)
        self.usuario = tk.StringVar()
        self.contrasenia = tk.StringVar()

    def _menu(self):
        tk.Label(self.raiz,text="Usuario").pack()
        tk.Entry(self.raiz,textvariable=self.usuario).pack()
        tk.Label(self.raiz,text="Contraseña").pack()
        tk.Entry(self.raiz,show="*", textvariable=self.contrasenia).pack()
        tk.Button(self.raiz,text="Iniciar", command=lambda:iniciarSesion(self.usuario.get(),self.contrasenia.get(),self.sesion)).pack()

class interfazAlumno(Programa):
    def __init__(self,p_titulo,p_tamanio):
        super().__init__(p_titulo,p_tamanio)
    
    def _menu(self):
        tk.Button(self.raiz,text="Mis Datos").pack()
        tk.Button(self.raiz,text="Info Materias").pack()
        tk.Button(self.raiz,text="Info Docentes").pack()
        tk.Button(self.raiz,text="Cerrar sesion").pack()

class interfazDocente(Programa):
    def __init__(self,p_titulo,p_tamanio,p_sesion):
        super().__init__(p_titulo,p_tamanio,p_sesion)
    
    def _menu(self):
        tk.Label(self.raiz,text="Usuario:").grid(row=1,column=0)
        tk.Label(self.raiz,text="").grid(row=2,column=0)
        tk.Label(self.raiz,text=self.sesion["nombre_usuario"]).grid(row=1,column=1)
        tk.Button(self.raiz,text="Mis Datos").grid(row=3,column=0)
        tk.Button(self.raiz,text="Info Materias").grid(row=3,column=1)
        tk.Button(self.raiz,text="Info Estudiantes").grid(row=3,column=2)
        tk.Button(self.raiz,text="Cerrar sesion").grid(row=3,column=3)

def iniciarSesion(p_user,p_pass,p_sesion):
    resultado_consulta = base.bbdd.procedimiento("obtenerCredencial",[p_user])[0]
    contrasenia = resultado_consulta[1]
    tipo_usuario = resultado_consulta[0]
    if contrasenia == "Usuario invalido":
        p_sesion["Acceso"] = contrasenia
        tk.Label(programa.raiz,text=p_sesion["Acceso"]).pack()
    else:
        if contrasenia == p_pass:
            p_sesion["Usuario"] = p_user
            p_sesion["Acceso"] = True
            p_sesion["Tipo Usuario"] = tipo_usuario
            programa._finalizar(None)
        else:
            p_sesion["Acceso"] = "Contraseña Invalida"
            tk.Label(programa.raiz,text=p_sesion["Acceso"]).pack()

def sesionUsuario(p_usuario,p_tipo):
    sesion = {}
    sesion["nombre_usuario"] = p_usuario
    sesion["tipo_usuario"] = p_tipo
    consulta = "SELECT * FROM {tabla} WHERE {condicion} = '{user}'"
    if p_tipo == 'estudiante':
        consulta = consulta.format(tabla = "ESTUDIANTE",condicion = "estudiante.usuario",user=p_usuario)
        res_cons = base.bbdd.ejecutar(consulta)[0]
        usuario = clase.Estudiante(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
    if p_tipo == "docente":
        consulta = consulta.format(tabla = "DOCENTE",condicion = "docente.usuario",user=p_usuario)
        res_cons = base.bbdd.ejecutar(consulta)[0]
        usuario = clase.Docente(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
    sesion["Datos"] = usuario
    return sesion

if __name__ == "__main__":

    datos_sesion = {}
    datos_programa = {}
    programa = interfazInicial("Inicio","200x200",datos_programa)
    programa._iniciar()
    print(datos_programa)
    if datos_programa["Acceso"] == True:
        datos_sesion = sesionUsuario(datos_programa["Usuario"],datos_programa["Tipo Usuario"])
        if datos_programa["Tipo Usuario"] == "docente":
            docente = interfazDocente("DOCENTES","400x200",datos_sesion)
            docente._iniciar()