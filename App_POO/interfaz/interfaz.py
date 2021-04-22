# pylint: disable=import-error
import interfaz.funciones as fc

def interfazEstudiante(p_sesion):
    menuEstudiante = {"1":"Mis Datos","2":"Información Materias","3":"Información Docentes","4":"Cerrar sesión"}
    exit = False
    while exit != True:
        print("\nMENU ESTUDIANTES\n")
        opcion = fc.manejoMenu(menuEstudiante)
        if opcion == "1":
            fc.limpiarPantalla()
            MisDatos(p_sesion)
        if opcion == "2":
            fc.limpiarPantalla()
            infoMateria()
        if opcion == "3":
            fc.limpiarPantalla()
            infoDocentes()
        elif opcion == "4":
            exit = True

def interfazDocente(p_sesion):
    menuDocentes = {"1":"Mis datos","2":"Información Carreras","3":"Información Materias","4":"Información Estudiantes","5":"Información Docentes","6":"Cerrar sesión"}
    exit = False
    while exit != True:
        print("\nMENU DOCENTES\n")
        opcion = fc.manejoMenu(menuDocentes)
        if opcion == "1":
            fc.limpiarPantalla()
            MisDatos(p_sesion)
        if opcion == "2":
            fc.limpiarPantalla()
            infoCarrera()
        elif opcion == "3":
            fc.limpiarPantalla()
            infoMateria()
        elif opcion == "4":
            pass
        elif opcion == "5":
            fc.limpiarPantalla()
            infoDocentes()
        elif opcion == "6":
            exit = True

def infoCarrera():
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

def infoMateria():
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

def infoDocentes():
    menuVerDocente = {"1":"Todos los docentes","2":"Docentes por materia","3":"Docente por ID","4":"Volver"}
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

def MisDatos(p_sesion):
    usuario = p_sesion["Datos"]
    encabezado = "Legajo: {}\nNombre: {}".format(usuario.legajo,usuario.nombre)
    fc.limpiarPantalla()    
    print("-----------\n"+encabezado+"\n-----------\n")
    if p_sesion["tipo_usuario"] == "estudiante":
        misDatosEst(usuario)
    if p_sesion["tipo_usuario"] == "docente":
        misDatosDoc(usuario)

def misDatosEst(p_usuario):
    menu = {"1":"Notas","2":"Asistencias","3":"Volver"}
    exit = False
    p_usuario._materias = p_usuario._getMaterias()
    while exit != True:
        print("\nMIS DATOS\n")
        opcion = fc.manejoMenu(menu)
        if opcion == "1":
            fc.limpiarPantalla()
            interfazMisNotas(p_usuario)
        elif opcion == "2":
            fc.limpiarPantalla()
            print("\nASISTENCIAS\n")
            menuAsistencia = {"1":"Porcentaje por materia","2": "Porcentaje por año","3":"Fecha"}
            opcion = fc.manejoMenu(menuAsistencia)
            if opcion == "1":
                print("\nMaterias disponibles:\n")
                for materia in p_usuario._materias:
                    print("\nID: {}\nMateria: {}".format(p_usuario._materias[materia].id,p_usuario._materias[materia].nombre))
                materia = int(input("\nInserte el id de la materia: "))
                porc_asistencia = p_usuario._porcentajeAsistencia(p_materia_id = materia)
                print("Porcentaje de asistencia = {}%".format(porc_asistencia))
            elif opcion == "2":
                anio = int(input("\nInserte el año: "))
                porc_asistencia = p_usuario._porcentajeAsistencia(p_anio = anio)
                print("Porcentaje de asistencia = {}%".format(porc_asistencia))
            elif opcion == "3":
                fecha = input("\nInserte fecha: (Formato requerido: YYYY-MM-DD) ")
                consulta = "select ae.fecha, ae.asistencia from asistencia_estudiantes ae where estudiante_legajo = {} and fecha = '{}';".format(p_usuario.legajo,fecha)
                asistencia = p_usuario._conect.ejecutar(consulta)[0][1]
                if asistencia == True:
                    print("Presente")
                else:
                    print("Ausente")
        elif opcion == "3":
            exit = True

def misDatosDoc(p_usuario):
    menu = {"1":"Materias","2":"Alumnos","3":"Volver"}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menu)
        if opcion == "1":
            print("\nMENU MATERIAS")
            p_usuario.materias = p_usuario.getMaterias()
            menu = {"1":"Alumnos inscriptos"}
            if opcion == "1":
                print("\nMaterias disponibles: \n")
                for materia in p_usuario.materias:
                    print("\nID: {}\nMateria: {}".format(materia,p_usuario.materias[materia].nombre))
                materia = int(input("\nIngrese ID materia: "))
                anio = int(input("\nIngrese el año a consultar: "))
                asistentes = p_usuario.materias[materia]._alumnosInscriptos(anio)
                for alumno in asistentes:
                    print("\nLegajo: {}\nNombre: {}".format(alumno,asistentes[alumno]))

def interfazMisNotas(p_usuario):
    exit = False
    while exit != True:
        print("\nNOTAS")
        menuNotas = {"1":"Por materia","2":"Por año","3":"Volver"}
        opcion = fc.manejoMenu(menuNotas)
        if opcion == "1":
            print("\nMaterias disponibles:\n")
            for materia in p_usuario._materias:
                print("\nID: {}\nMateria: {}".format(p_usuario._materias[materia].id,p_usuario._materias[materia].nombre))
            materia = int(input("\nInserte el id de la materia: "))
            lista_notas = p_usuario._getNotaMateria(p_materia_id = materia)
            fc.printNotasEstudiantes(lista_notas)
        if opcion == "2":
            anio = int(input("\nIngrese el año: "))
            lista_notas = p_usuario._getNotaMateria(p_anio = anio)
            fc.printNotasEstudiantes(lista_notas)
        if opcion == "3":
            exit = True