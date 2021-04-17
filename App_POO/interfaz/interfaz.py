# pylint: disable=import-error
import os
import interfaz.funciones as fc

menuCarreras = {"1":"Listar todas","2":"Buscar y listar","3":"Salir"}

def interfazEstudiante(p_sesion):
    menuEstudiante = {"1":"Carreras","2":"Materias","3":"Docentes","4":"Salir"}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuEstudiante)
        if opcion == "1":
            os.system("cls")
            interfazCarrera(p_sesion)
        if opcion == "2":
            os.system("cls")
            interfazMateria(p_sesion)
        if opcion == "3":
            os.system("cls")
            interfazVerDocentes(p_sesion)
        elif opcion == "4":
            exit = True

def interfazDocente(p_sesion):
    menuDocentes = {"1":"Carreras","2":"Materias","3":"Estudiantes","4":"Salir"}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuDocentes)
        if opcion == "1":
            os.system("cls")
            interfazCarrera(p_sesion)
        elif opcion == "2":
            os.system("cls")
            interfazMateria(p_sesion)
        elif opcion == "3":
            pass
        elif opcion == "4":
            exit = True

def interfazCarrera(p_sesion):
    dictCarreras = {}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuCarreras)
        if opcion == "1":
            dictCarreras = fc.busquedaCarrera()
            os.system("cls")
            for item in dictCarreras:
                dictCarreras[item].imprimeObjeto(False)
        if opcion == "2":
            idCarrera = int(input("\nInserte el id de la carrera buscada: "))
            if idCarrera in dictCarreras.keys():
                os.system("cls")
                dictCarreras[idCarrera].imprimeObjeto(True)
            else:
                os.system("cls")
                dictCarreras = fc.busquedaCarrera(idCarrera)
                dictCarreras[idCarrera].imprimeObjeto(True)
        if opcion == "3":
            exit = True

def interfazMateria(p_sesion):
    pass


def interfazVerDocentes(p_sesion):
    menuVerDocente = {"1":"Todos los docentes","2":"Docentes por materia","3":"Docente por ID","4":"Salir"}
    dictDocentes = {}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuVerDocente)
        if opcion == "1":
            dictDocentes = fc.busquedaDocente()
            for docente in dictDocentes:
                print("\nNombre: {}\nEmail: {}".format(dictDocentes[docente].nombre,dictDocentes[docente].email))
        if opcion == "2":
            pass
        if opcion == "3":
            pass
        if opcion == "4":
            exit = True