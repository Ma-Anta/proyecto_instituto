# pylint: disable=import-error
import bbdd.bbdd as base
import tkinter as tk

class Programa():
    
    conect = base.bbdd

    menuIngreso = {"1": "Usuarios","2":"Invitados","3":"Salir"}
    menuUsuario = {"1": "Docentes","2": "Estudiantes", "4":"Menu Inicial"}
    menuInvitado = {"1": "Carreras","2": "Materias","3": "Menu Inicial"}
    menuDocente = {"1":"Carreras","2":"Materias","3":"Estudiantes","4":"Menu Inicial"}
    menuEstudiante = {"1":"Carreras","2":"Materias","3":"Docentes","4":"Menu Inicial"}
    
    def __init__(self,p_menu = None,p_sesion=None):
        self._menu = p_menu
        self._sesion = None

    def getAcceso(self,p_usuario):
        credencial = self.conect.procedimiento("obtenerCredencial",[p_usuario])[0][0]
        if credencial == "Usuario invalido":
            return credencial
        else:
            contrasena = input("Ingrese contraseña: ")
            if contrasena == credencial:
                return True
            else:
                return False

    def setSesion(self,p_usuario,p_perfil):
        consulta = "SELECT legajo,apellido_nombre from docente where docente.usuario like '"+p_usuario+"'"
        datos = self.conect.ejecutar(consulta)[0]
        sesion = {"legajo":datos[0],"apellido_nombre":datos[1],"permiso":p_perfil}
        return sesion
    
    def manejoMenu(self,p_menu):
        for opcion in p_menu:
            print(opcion," - ",p_menu[opcion])
        opcion = input("\nElija una opción: ")
        return opcion






"""
if __name__ == "__main__":
    opcion = 0
    programa = Programa()
    opcion = programa.manejoMenu()
    if opcion == "1":
        usuario = input("\nIngrese su usuario: ")
        ingreso = programa.getAcceso(usuario)
        if ingreso == "Usuario invalido":
            print(ingreso)
        elif ingreso == True:
            programa.sesion = programa.getSesion(usuario,opcion)
            print("\nBienvenido",programa.sesion["apellido_nombre"],"\n")
            if opcion == "1":
                programa.menu = programa.menuDocente()
                opcion = programa.manejoMenu()
            if opcion == "2":
                programa.menu = programa.menuEstudiantes()
                opcion = programa.manejoMenu()
        else:
            print("Contraseña invalida")
"""