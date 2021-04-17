# pylint: disable=import-error
import os
import bbdd.bbdd as base
import clases.clases as clase
import interfaz.funciones as fc
import interfaz.interfaz as app

menuIngreso = {"1":"Usuario","2":"Invitado","3":"Salir"}
menuUsuario = {"1":"Docente","2":"Estudiante","3":"Salir"}
menuMaterias = {"1":"Buscar materia","2":"Ver estudiantes por materia","3":"Salir"}

def iniciarSesion():
    os.system("cls")
    usuario = input("Ingrese su usuario: ")
    contrasenia = base.bbdd.procedimiento("obtenerCredencial",[usuario])[0][0]
    passwordIngresada = input("Ingrese contraseña: ")
    if contrasenia == passwordIngresada:
        print("\nBienvenido {}\n".format(usuario))
        return True
    else:
        return False

if __name__ == "__main__":
    os.system("cls")
    print("\n---Bienvenido---")
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuIngreso)
        if opcion == "1":
            inicio = iniciarSesion()
            if inicio == True:
                opcion = fc.manejoMenu(menuUsuario)
                if opcion == "1":
                    app.interfazDocente(None)
                if opcion == "2":
                    app.interfazEstudiante(None)
            else:
                print("\nInicio de sesion fallido\n")
        elif opcion == "3":
            exit = True
            print("Hasta pronto")