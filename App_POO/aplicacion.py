# pylint: disable=import-error
import os
import bbdd.bbdd as base
import interfaz.funciones as fc
import interfaz.interfaz as app

menuIngreso = {"1":"Usuario","2":"Invitado","3":"Salir"}
menuMaterias = {"1":"Buscar materia","2":"Ver estudiantes por materia","3":"Salir"}

if __name__ == "__main__":
    sesion = {}
    os.system("cls")
    print("\n---Bienvenido---")
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuIngreso)
        if opcion == "1":
            os.system("cls")
            usuario = input("Ingrese su usuario: ")
            inicio,tipo_credencial = fc.iniciarSesion(usuario)
            os.system("cls")
            if inicio == True:
                sesion = fc.sesionUsuario(usuario,tipo_credencial)
                if sesion["tipo_usuario"] == "docente":
                    app.interfazDocente(sesion)
                if sesion["tipo_usuario"] == "estudiante":
                    app.interfazEstudiante(sesion)
            else:
                print(inicio," \nInicio de sesion fallido\n")
        elif opcion == "3":
            exit = True
            print("\nHasta las vista, Baby")