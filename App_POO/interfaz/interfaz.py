# pylint: disable=import-error
from interfaz import funciones as fc
from abc import ABC,abstractmethod
import os
import platform

#INTERFACES
#La idea del manejo de las interfaces es sencilla, las clases se van instanciando a medida que se necesitan.

#INTERFAZ PADRE.
class Interfaz():
    _menu = {}

    def __init__(self,p_sesion):
        self._sesion = p_sesion
    #METODO PARA MANEJAR MENU
    def _manejoMenu(self):
        print("\n")
        for item in self._menu:
            print(item," - ",self._menu[item])
        opcion = input("\nIngrese una opcion: ")
        return opcion   
    #METODO PARA LIMPIAR LA PANTALLA
    def _limpiar(self):
        if platform.system() == "Windows":
            os.system('cls')
        elif platform.system() == "Linux":
            os.system('clear')
    #METODO ABSTRACTO QUE POSEE EL BUCLE DE EJECUCION DE UNA INTERFAZ
    @abstractmethod
    def _ejecucion(self):
        exit = False
        try:
            while exit != True:
                exit = self._opciones()
        except ValueError:
            print("\nError en la ejecución del programa.\n",ValueError)
    #METODO ABSTRACTO, CADA CLASE HIJA REDEFINE EL METODO CON LAS OPCIONES DE CADA UNA
    @abstractmethod
    def _opciones(self):
        pass
#INTERFAZ DE INFORMACION DE BUSQUEDA DE CARRERAS,MATERIAS, DOCENTES O ESTUDIANTES.
#LOS DOCENTES PUEDEN VER DATOS DE DOCENTES Y ESTUDIANTES.
#LOS DOCENTES PUEDEN VER DATOS DE DOCENTES Y ESTUDIANTES.
#LOS INVITADOS PUEDEN VER SOLO DATOS DE DOCENTES.
#TODOS PUEDEN VER DATOS DE CARRERAS Y MATERIAS.
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
            self._info("carrera")
        if opcion == "2":
            self._info("materia")
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
        diccionario = fc.busquedaCarMat(p_busqueda)
        exit = False
        while exit != True:
            self._menu = menuInfo
            if p_busqueda == 1:
                print("\nMENU INFO CARRRERAS\n")
            else:
                print("\nMENU INFO MATERIAS\n")
            opcion = self._manejoMenu()
            if opcion == "1":
                self._limpiar()
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
#INTERFAZ DE BUSQUEDA DE PERSONAS.
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
            self._limpiar()
            self._dictPersonas = fc.busquedaPersona(self._tipo)
            fc.imprimirPersona(self._dictPersonas)
        if opcion == "2":
            self._limpiar()
            nombre = input("Ingrese nombre a buscar: ")
            self._dictPersonas = fc.busquedaPersona(p_tipo = self._tipo,p_nombre = nombre)
            fc.imprimirPersona(self._dictPersonas)
        if opcion == "3":
            self._limpiar()
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
#INTERFAZ DE INICIO DEL PROGRAMA.               
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
            self._limpiar()
            self._sesion["tipo_usuario"] = "invitado"
            invitado = interfazInvitado(self._sesion)
            invitado._ejecucion()
        if opcion == "3":
            print("\nGracias! \nVuelvas prontos! (leer como Apu)\n")
            return True
#INTERFAZ INICIAL PARA USUARIOS  
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
#INTERFAZ INICIAL PARA INVITADOS
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
#INTERFAZ PARA DATOS ACADEMICOS
class DatosAcademicos(Interfaz):
    _menuAcademico = {"1":"Carrera","2":"Materias","3":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuAcademico
        opcion = self._manejoMenu()
        if opcion == "1":
            pass
        if opcion == "2":
            self._limpiar()
            if self._sesion["tipo_usuario"] == "docente":
                misMaterias = MisMateriasDoc(self._sesion)
                misMaterias._ejecucion()
            if self._sesion["tipo_usuario"] == "estudiante":
                misMaterias = MisMateriasEst(self._sesion)
                misMaterias._ejecucion()
        if opcion == "3":
            return True
#INTERFAZ PARA MATERIAS DE ESTUDIANTES
class MisMateriasEst(Interfaz):
    _menuDatos = {"1":"Matriculacion","2":"Mis notas","3":"Mis asistencias","4":"Salir"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        print("\nMIS MATERIAS\n")
        usuario = self._sesion["Datos"]
        self._menu = self._menuDatos
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            usuario._muestraMaterias(True)
        if opcion == "2":
            self._limpiar()
            fc.busquedaNotas(self._sesion)
        if opcion == "3":
            self._limpiar()
            print("\nASISTENCIAS\n")
            asistencias = Asistencias(self._sesion)
            asistencias._ejecucion()
        if opcion == "4":
            return True
#INTERFAZ PARA MATERIAS DE DOCENTES
class MisMateriasDoc(Interfaz):
    _menuMaterias = {"1":"Alumnos inscriptos","2":"Asistencias","3":"Notas","4":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuMaterias
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
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
            fc.busquedaNotas(self._sesion)
        elif opcion == "4":
            return True
#INTERFAZ PARA ASISTENCIAS
class Asistencias(Interfaz):
    _menuAsist = {"1":"Por materia y año","2":"Asistencias porcentuales","3":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)

    def _opciones(self):
        print("\nASISTENCIAS")
        self._menu = self._menuAsist
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            fc.busquedaAsistencias(self._sesion,1)
        elif opcion == "2":
            self._limpiar()
            fc.busquedaAsistencias(self._sesion,2)
        elif opcion == "3":
            return True
#INTERFAZ DE PRECEPTORES
class DatosAcademicosPreceptor(Interfaz):
    _menuPrec = {"1":"Alumnos","2":"Docentes","3":"Carreras","4":"Materias","5":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuPrec
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            print("\nALUMNOS")
            manejoAlumnos = ManejoAlumnos(self._sesion)
            manejoAlumnos._ejecucion()
        if opcion == "2":
            self._limpiar()
        if opcion == "3":
            self._limpiar()
        if opcion == "4":
            self._limpiar()
        if opcion == "5":
            return True
#INTERFAZ PARA EL MANEJO DE ALUMNOS
class ManejoAlumnos(Interfaz):
    _menuManejoAlumnos = {"1":"Insertar/Modificar Notas","2":"Insertar/Modificar Asistencias","3":"Volver"}

    def __init__(self,p_sesion):
        super().__init__(p_sesion)
    
    def _opciones(self):
        self._menu = self._menuManejoAlumnos
        opcion = self._manejoMenu()
        if opcion == "1":
            self._limpiar()
            print("\nInsertar notas")
            legajo = int(input("\nIngrese legajo del alumno: "))
            materia = int(input("\nIngrese id de la materia: "))
            tipo_nota = fc.elegirTipoNota()
            fecha = input("\nIngrese la fecha de examen: ")
            nota = float(input("\nIngrese la nota: "))
            datos = [legajo,materia,tipo_nota,fecha,nota]
            print(self._sesion["Datos"]._insertaNotas(datos))
        if opcion == "2":
            self._limpiar()
            print("\nInsertar asistencia: ")
            carrera = int(input("\nIngrese el id de la carrera: "))
            materia = int(input("\nIngrese el id de la materia: "))
            legajo = int(input("\nIngrese el legajo del alumno: "))
            fecha = input("\nIngrese la fecha: ")
            asistencia = input("\nIngrese presente o ausente: ")
            if asistencia == "presente":
                asistencia = True
            elif asistencia == "ausente":
                asistencia = False
            else:
                print("\nError en la insercion de datos")
            if asistencia == True or asistencia == False:
                datos = [carrera,materia,legajo,fecha,asistencia]
                print(self._sesion["Datos"]._insertaAsistencia(datos))
        if opcion == "3":
            return True
