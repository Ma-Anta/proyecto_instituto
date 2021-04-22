# pylint: disable=import-error
import interfaz.funciones as fc
import interfaz.interfaz as app

menuIngreso = {"1":"Usuario","2":"Invitado","3":"Salir"}

if __name__ == "__main__":
    sesion = {}
    fc.limpiarPantalla()
    print("\n---Bienvenido---")
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuIngreso)
        if opcion == "1":
            fc.limpiarPantalla()
            usuario = input("Ingrese su usuario: ")
            inicio,tipo_credencial = fc.iniciarSesion(usuario)
            fc.limpiarPantalla()
            if inicio == True:
                sesion = fc.sesionUsuario(usuario,tipo_credencial)
                if sesion["tipo_usuario"] == "docente":
                    app.interfazDocente(sesion)
                if sesion["tipo_usuario"] == "estudiante":
                    app.interfazEstudiante(sesion)
            else:
                print(inicio," \nInicio de sesion fallido\n")
        elif opcion == "2":
            fc.limpiarPantalla()
            app.interfazInvitado()
        elif opcion == "3":
            exit = True
            print("\nHasta las vista, Baby")