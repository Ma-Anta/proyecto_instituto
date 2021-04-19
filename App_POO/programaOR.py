# pylint: disable=import-error
import bbdd.bbdd as base
import tkinter as tk

class Programa():
    conect = base.bbdd
    def __init__(self,p_sesion,p_exit):
        self._exit = p_exit
        self._sesion = p_sesion
    
    def manejoMenu(self):
        print("\n")
        for item in self._menu:
            print(item," - ",self._menu[item])
        opcion = input("\nIngrese una opcion: ")
        return opcion
    
    def _ejecucion(self):
        while self._exit != True:
            opcion = self.manejoMenu()
            if opcion in ["Salir","Cerrar sesion","Volver"]:
                self._exit = True
    
    def _infoCarrera(self):
        menuCarreras = {"1":"Listar todas","2":"Buscar y listar","3":"Volver"}
        dictCarreras = {}
        exit = False
        while exit != True:
            print("\nMENU INFO CARRRERAS\n")
            opcion = fc.manejoMenu(menuCarreras)
            if opcion == "1":
                dictCarreras = fc.busquedaCarrera()
                fc.limpiarPantalla()
                for item in dictCarreras:
                    dictCarreras[item].imprimeObjeto(False)
            if opcion == "2":
                idCarrera = int(input("\nInserte el id de la carrera buscada: "))
                if idCarrera in dictCarreras.keys():
                    fc.limpiarPantalla()
                    dictCarreras[idCarrera].imprimeObjeto(True)
                else:
                    fc.limpiarPantalla()
                    dictCarreras = fc.busquedaCarrera(idCarrera)
                    dictCarreras[idCarrera].imprimeObjeto(True)
            if opcion == "3":
                exit = True

    def _infoMateria(self):
    menuMaterias = {"1":"Listar todas","2":"Buscar y listar","3":"Volver"}
    dictMaterias = {}
    exit = False
    while exit != True:
        print("\nMENU INFO MATERIAS\n")
        opcion = fc.manejoMenu(menuMaterias)
        if opcion == "1":
            dictMaterias = fc.busquedaMateria()
            fc.limpiarPantalla()
            for item in dictMaterias:
                dictMaterias[item].imprimeObjeto(False)
        if opcion == "2":
            idMateria = int(input("\nInserte el id de la carrera buscada: "))
            if idMateria in dictMaterias.keys():
                fc.limpiarPantalla()
                dictMaterias[idMateria].imprimeObjeto(True)
            else:
                fc.limpiarPantalla()
                dictMaterias = fc.busquedaMateria(idMateria)
                dictMaterias[idMateria].imprimeObjeto(True)
        if opcion == "3":
            exit = True

class interfazDocente(Programa):
    _menu = {"2":"Información Carreras","3":"Información Materias","4":"Información Estudiantes","5":"Información Docentes","6":"Cerrar sesión"}
    def __init__(self,p_sesion,p_exit):
        super().__init__(p_sesion,p_exit)




interfaz = interfazDocente(None,False)
interfaz._ejecucion()