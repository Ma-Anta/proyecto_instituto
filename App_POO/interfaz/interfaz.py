# pylint: disable=import-error
import os
import interfaz.funciones as fc

menuCarreras = {"1":"Listar todas","2":"Buscar y listar","3":"Salir"}

def interfazEstudiante(p_sesion):
    menuEstudiante = {"1":"Carrera","2":"Materias","3":"Docentes","4":"Salir"}
    exit = False
    while exit != True:
        print("\nMENU ESTUDIANTES\n")
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
        print("\nMENU DOCENTES\n")
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
        print("\nMENU CARRRERAS\n")
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
    menuMateriaD = {"1":"Docentes asignados","2":"Alumnos inscriptos","3":"Info materia","4":"Salir"}
    menuMateriaE = {"1":"Docentes asignados","2":"Mis notas","3":"Mis asistencias","4":"Salir"}
    existe = False
    while existe != True:
        print("\nMENU MATERIA")
        if p_sesion["tipo_usuario"] == "docente":
            opcion = fc.manejoMenu(menuMateriaD)
            if opcion == "1":
                pass
            elif opcion == "2":
                pass
        if p_sesion["tipo_usuario"] == "estudiante":
            opcion = fc.manejoMenu(menuMateriaE)
            estudiante = p_sesion["Datos"]
            estudiante._materias = estudiante._getMaterias()
            if opcion == "1":
                pass
            elif opcion == "2":
                anio = int(input("Ingrese el año de cursada: "))
                for materia in estudiante._materias:
                    print("\nNotas para la materia: {}".format(estudiante._materias[materia].nombre))
                    lista_notas = estudiante._conect.procedimiento("proy_inst_f_notas_estudiantes",[estudiante._materias[materia].id,estudiante.legajo,anio])
                    if lista_notas == []:
                        print("\nNo se encuentran notas para la materia en el año: {}".format(anio))
                    else:
                        for nota in lista_notas:
                            print("\nFecha: {}\nNota: {}\nTipo de examen: {}".format(nota[0],nota[1],nota[2]))
                        

def interfazVerDocentes(p_sesion):
    menuVerDocente = {"1":"Todos los docentes","2":"Docentes por materia","3":"Docente por ID","4":"Salir"}
    dictDocentes = {}
    exit = False
    while exit != True:
        print("\nMENU BUSQUEDA DOCENTES\n")
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