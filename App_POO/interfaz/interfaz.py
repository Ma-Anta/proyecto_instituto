# pylint: disable=import-error
from interfaz import funciones as fc
from abc import ABC,abstractmethod
import os
import platform

class Interfaz():
    _menu = {}

    def __init__(self,p_sesion):
        self._sesion = p_sesion
   
    def _manejoMenu(self):
        print("\n")
        for item in self._menu:
            print(item," - ",self._menu[item])
        opcion = input("\nIngrese una opcion: ")
        return opcion   
    
    def _limpiar(self):
        if platform.system() == "Windows":
            os.system('cls')
        elif platform.system() == "Linux":
            os.system('clear')
    
    @abstractmethod
    def _ejecucion(self):
        exit = False
        try:
            while exit != True:
                exit = self._opciones()
        except ValueError:
            print("\nError en la ejecución del programa.\n",ValueError)
    
    @abstractmethod
    def _opciones(self):
        pass
    
    def _misDatos(self):
        menu = {"1":"Ver datos personales","2":"Modificar datos personales","3":"Cambiar contraseña","4":"Volver"}
        self._menu = menu
        exit = False
        while exit != True:
            opcion = self._manejoMenu()
            if opcion == "1":
                self._limpiar()
                self._sesion["Datos"]._muestraDatos(True)
            if opcion == "2":
                self._limpiar()
                self._sesion["Datos"]._modificaDatos()
            if opcion == "3":
                pass
            if opcion == "4":
                exit = True

class InterfazInformacion(Interfaz):
    _menuInfo = {"1":"Carreras","2":"Materias","3":"Docentes","4":"Estudiantes","5":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)

    def _opciones(self):
        if self._sesion["tipo_usuario"] == "invitado":
            self._menu = self._menuInfo.pop("4")
        else:
            self._menu = self._menuInfo
        opcion = self._manejoMenu()
        if opcion == "1":
            self._info(1)
        if opcion == "2":
            self._info(2)
        if opcion == "3":
            self._limpiar()
            buscarPersonas = interfazBusquedaPersonas(self._sesion,"docente")
            buscarPersonas._ejecucion()
        if opcion == "4":
            if self._sesion["tipo_usuario"] == "invitado":
                print("Opción no valida")
            self._limpiar()
            buscarPersonas = interfazBusquedaPersonas(self._sesion,"estudiante")
            buscarPersonas._ejecucion()      
        if opcion == "5":
            return True

    def _info(self,p_busqueda):
        menuInfo = {"1":"Listar todas","2":"Buscar y listar","3":"Volver"}
        diccionario = {}
        self._menu = menuInfo
        if p_busqueda == 1:
            diccionario = fc.busquedaCarrera()
        if p_busqueda == 2:
            diccionario = fc.busquedaMateria()
        exit = False
        while exit != True:
            if p_busqueda == 1:
                print("\nMENU INFO CARRRERAS\n")
            else:
                print("\nMENU INFO MATERIAS\n")
            opcion = self._manejoMenu()
            if opcion == "1":
                for item in diccionario:
                    diccionario[item]._imprimeObjeto(False)
            if opcion == "2":
                numeroID = int(input("\nInserte el ID buscado: "))
                if numeroID in diccionario.keys():
                    self._limpiar()
                    diccionario[numeroID]._imprimeObjeto(True)
                else:
                    self._limpiar()
                    print("\nCarrera no encontrada.\n")
            if opcion == "3":
                exit = True

class interfazBusquedaPersonas(Interfaz):
    _menuBusquedaPersonas = {"1":"Todos","2":"Por nombre","3":"Por legajo","4":"Volver"}
    _dictPersonas = {}
    
    def __init__(self,p_sesion,p_tipo):
        super().__init__(p_sesion)
        self._tipo = p_tipo
    
    def _opciones(self):
        if self._sesion["tipo_usuario"] == "invitado":
            try:
                self._menuBusquedaPersonas.pop("3")
            except:
                pass
        self._menu = self._menuBusquedaPersonas
        opcion = self._manejoMenu()
        if opcion == "1":
            self._dictPersonas = fc.busquedaPersona(self._tipo)
            fc.imprimirPersona(self._dictPersonas)
        if opcion == "2":
            nombre = input("Ingrese nombre a buscar: ")
            self._dictPersonas = fc.busquedaPersona(p_tipo = self._tipo,p_nombre = nombre)
            fc.imprimirPersona(self._dictPersonas)
        if opcion == "3":
            if self._sesion["tipo_usuario"] == "invitado":
                print("\nOpción inexistente\n")
            else:
                legajo = int(input("Ingrese el numero de legajo: "))
                if legajo in self._dictPersonas.keys():
                    self._dictPersonas[legajo]._muestraDatos(False)
                else:
                    self._dictPersonas = fc.busquedaPersona(p_tipo = self._tipo,p_legajo = legajo)
                    fc.imprimirPersona(self._dictPersonas)
        if opcion == "4":
            return True
        
class InterfazInicio(Interfaz):
    _menuIngreso = {"1":"Usuario","2":"Invitado","3":"Salir"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuIngreso
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            usuario = input("\nIngrese usuario: ")
            inicio,tipo_usuario = fc.iniciarSesion(usuario)
            if inicio == True:
                self._sesion = fc.sesionUsuario(usuario,tipo_usuario)
                usuario = interfazUsuario(self._sesion)
                usuario._ejecucion()
            else:
                print("\n"+inicio+"\n")
        if opcion == "2":
            self._sesion["tipo_usuario"] = "invitado"
            invitado = interfazInvitado(self._sesion)
            invitado._ejecucion()
        if opcion == "3":
            print("\nGracias! \nVuelvas prontos! (leer como Apu)\n")
            return True
      
class interfazUsuario(Interfaz):
    
    _menuEst = {"1":"Datos personales","2":"Datos academicos","3":"Información","4":"Cerrar sesion"}
    
    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        print("\nMENU USUARIOS\nLegajo: {}\nNombre: {}\nTipo de usuario: {}".format(self._sesion["Datos"]._legajo,self._sesion["Datos"]._nombre,self._sesion["tipo_usuario"]))
        self._menu = self._menuEst
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            self._misDatos()
        elif opcion == "2":
            self._limpiar()
            datosAcad = DatosAcademicos(self._sesion)
            datosAcad._ejecucion()
        elif opcion == "3":
            self._limpiar()
            busqueda = InterfazInformacion(self._sesion)
            busqueda._ejecucion()
        elif opcion == "4":
            return True

class interfazInvitado(Interfaz):
    _menuInvitado = {"1":"Informacion de carreras/materias","2":"Informacion de docentes","3":"Salir"}
    
    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuInvitado
        print("\nMENU INVITADOS")
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            busqueda = InterfazInformacion(self._sesion)
            busqueda._ejecucion()
        if opcion == "2":
            self._limpiar()
            buscarPersonas = interfazBusquedaPersonas(self._sesion,"docente")
            buscarPersonas._ejecucion()
        if opcion == "3":
            return True

class DatosAcademicos(Interfaz):
    _menuAcademico = {"1":"Carrera","2":"Materias","3":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuAcademico
        opcion = self._manejoMenu()

        if opcion == "2":
            if self._sesion["tipo_usuario"] == "docente":
                misMaterias = MisMateriasDoc(self._sesion)
                misMaterias._ejecucion()
            if self._sesion["tipo_usuario"] == "estudiante":
                misMaterias = MisMateriasEst(self._sesion)
                misMaterias._ejecucion()
        if opcion == "3":
            return True

class MisMateriasEst(Interfaz):
    _menuDatos = {"1":"Mis materias","2":"Mis notas","3":"Mis asistencias","4":"Salir"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        print("\nMIS DATOS\n")
        usuario = self._sesion["Datos"]
        self._menu = self._menuDatos
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            usuario._muestraMaterias(True)
        if opcion == "2":
            self._limpiar()
            id = fc.materiasDisponibles(usuario)
            notas = usuario._getNotaMateria(p_materia_id = id)
            for nota in notas:
                print("\nMateria: {}".format(nota))
                for informacion in notas[nota]:
                    print("\nFecha: {}\nNota: {}\nTipo nota: {}".format(informacion[0],informacion[1],informacion[2]))
        if opcion == "3":
            self._limpiar()
            print("\nASISTENCIAS\n")
            opcion = int(input("\n1 - Por materia\n2 - Por año\n3 - Ambos\n"))
            if opcion == 1:
                id = fc.materiasDisponibles(usuario)
                asistencia = usuario._getAsistencia(p_materia_id = id)
            elif opcion == 2:
                anio = int(input("\nIngrese año: "))
                asistencia = usuario._getAsistencia(p_anio = anio)
            elif opcion == 3:
                id = fc.materiasDisponibles(usuario)
                anio = int(input("\nIngrese año: "))
                asistencia = usuario._getAsistencia(p_materia_id = id,p_anio = anio)
            for dato in asistencia:
                if dato[2] == True:
                    presencia = "Presente"
                else:
                    presencia = "Ausente"
                print("\nFecha: {}\nAsistencia: {}".format(dato[1],presencia))
        if opcion == "4":
            return True

class MisMateriasDoc(Interfaz):
    _menuMaterias = {"1":"Alumnos inscriptos","2":"Asistencias","3":"Notas","4":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuMaterias
        print("\nMIS MATERIAS")
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            print("\nMATERIAS DISPONIBLES")
            id = fc.materiasDisponibles(self._sesion["Datos"])
            anio = int(input("\nIngrese año de consulta: "))
            asistentes = self._sesion["Datos"]._materias[id]._alumnosInscriptos(anio)
            for asistente in asistentes:
                print(asistente,asistentes[asistente])
        elif opcion == "2":
            self._limpiar()
            menuAsist = Asistencias(self._sesion)
            menuAsist._ejecucion()
        elif opcion == "3":
            self._limpiar()
            notas = fc.busquedaNotas(self._sesion["Datos"])
            for nota in notas:
                print("\nMateria: {}\nFecha: {}\nNota: {}\nTipo nota: {}".format(nota,notas[nota][1],notas[nota][2],notas[nota][3]))
        elif opcion == "4":
            return True

class Asistencias(Interfaz):
    _menuAsist = {"1":"Por materia y año","2":"Asistencias porcentuales","3":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)

    def _opciones(self):
        print("\nASISTENCIAS")
        self._menu = self._menuAsist
        opcion = self._manejoMenu()
        if opcion == "1":
            fc.busquedaAsistencias(self._sesion["Datos"],1)
        elif opcion == "2":
            fc.busquedaAsistencias(self._sesion["Datos"],2)
        elif opcion == "3":
            return True