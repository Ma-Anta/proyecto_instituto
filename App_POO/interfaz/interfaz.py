# pylint: disable=import-error
import interfaz.funciones as fc
import bbdd.bbdd as base

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
            fc.limpiarPantalla()
            infoEstudiantes()
        elif opcion == "5":
            fc.limpiarPantalla()
            infoDocentes()
        elif opcion == "6":
            exit = True

def interfazInvitado():
    menuInvitado = {"1":"Informacion de carreras","2":"Informacion de materias","3":"Informacion de docentes","4":"Salir"}
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menuInvitado)
        if opcion == "1":
            fc.limpiarPantalla()
            infoCarrera()
        if opcion == "2":
            fc.limpiarPantalla()
            infoMateria()
        if opcion == "3":
            fc.limpiarPantalla()
            infoDocentes()
        if opcion == "4":
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
    exit = False
    while exit != True:
        print("\nMENU BUSQUEDA DOCENTES\n")
        opcion = fc.manejoMenu(menuVerDocente)
        dictDocentes = {}
        if opcion == "1":
            dictDocentes = fc.busquedaPersona(p_tipo = "docente")
            fc.imprimirPersona(dictDocentes)
        if opcion == "2":
            materia = int(input("Ingrese ID de materia: "))
            consulta = "select pivmpd.legajo,pivmpd.apellido_nombre,pivmpd.nombre from proy_inst_v_materias_por_docente pivmpd where id = {}".format(materia)
            resp_consulta = base.bbdd.ejecutar(consulta)
            for docente in resp_consulta:
                print("\nMateria: {}\nLegajo: {}\nNombre: {}".format(docente[2],docente[0],docente[1]))
        if opcion == "3":
            legajo = int(input("Ingrese el legajo del docente: "))
            dictDocentes = fc.busquedaPersona(p_tipo = "docente",p_legajo_docente = legajo)
            fc.imprimirPersona(dictDocentes)
        if opcion == "4":
            exit = True

def infoEstudiantes():
    menuVerEstudiante = {"1":"Todos los estudiantes","2":"Estudiantes por materia","3":"Estudiante por Legajo","4":"Volver"}
    exit = False
    while exit != True:
        dictEstudiantes = {}
        print("\nMENU BUSQUEDA DOCENTES\n")
        opcion = fc.manejoMenu(menuVerEstudiante)
        if opcion == "1":
            dictEstudiantes = fc.busquedaPersona(p_tipo = "estudiante")
            fc.imprimirPersona(dictEstudiantes)
        if opcion == "2":
            materia = int(input("Ingrese ID de materia: "))
            consulta = "select pivmpe.legajo,pivmpe.apellido_nombre from proy_inst_v_materias_por_estudiante pivmpe where pivmpe.id_materia = {}".format(materia)
            resp_consulta = base.bbdd.ejecutar(consulta)
            for alumno in resp_consulta:
                print("\nLegajo: {}\nNombre: {}".format(alumno[0],alumno[1]))
        if opcion == "3":
            legajo = int(input("Ingrese el legajo del estudiante: "))
            dictEstudiantes = fc.busquedaPersona(p_tipo = "estudiante",p_legajo_docente = legajo)
            fc.imprimirPersona(dictEstudiantes)
        if opcion == "4":
            exit = True

def MisDatos(p_sesion):
    encabezado = "Legajo: {}\nNombre: {}".format(p_sesion["Datos"]._legajo,p_sesion["Datos"]._nombre)
    fc.limpiarPantalla()    
    print("-----------\n"+encabezado+"\n-----------\n")
    if p_sesion["tipo_usuario"] == "estudiante":
        misDatosEst(p_sesion)
    if p_sesion["tipo_usuario"] == "docente":
        misDatosDoc(p_sesion)

def misDatosEst(p_sesion):
    menu = {"1":"Notas","2":"Asistencias","3":"Ver/Modifcar datos personales","4":"Salir"}
    usuario = p_sesion["Datos"]
    exit = False
    usuario._materias = usuario._getMaterias()
    while exit != True:
        print("\nMIS DATOS\n")
        opcion = fc.manejoMenu(menu)
        if opcion == "1":
            fc.limpiarPantalla()
            interfazMisNotas(usuario)
        elif opcion == "2":
            fc.limpiarPantalla()
            interfazAsistencias(usuario)
        elif opcion == "3":
            verModificarDatos(p_sesion)
        elif opcion == "4":
            exit = True

def misDatosDoc(p_sesion):
    menu = {"1":"Materias","2":"Alumnos","3":"Volver"}
    usuario = p_sesion["Datos"]
    exit = False
    while exit != True:
        opcion = fc.manejoMenu(menu)
        if opcion == "1":
            print("\nMENU MATERIAS")
            menu = {"1":"Alumnos inscriptos"}
            opcion = fc.manejoMenu(menu)
            if opcion == "1":
                print("\nMaterias disponibles: \n")
                for materia in usuario.materias:
                    print("\nID: {}\nMateria: {}".format(materia,usuario.materias[materia].nombre))
                materia = int(input("\nIngrese ID materia: "))
                anio = int(input("\nIngrese el año a consultar: "))
                asistentes = usuario.materias[materia]._alumnosInscriptos(anio)
                for alumno in asistentes:
                    print("\nLegajo: {}\nNombre: {}".format(alumno,asistentes[alumno]))
        if opcion == "2":
            print("\nMENU ALUMNOS")
            alumno = int(input("\nIngrese numero de legajo del alumno: "))
            menu = {"1":"Asistencias","2":"Notas"}
        if opcion == "3":
            exit = True

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

def interfazAsistencias(p_usuario):
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

def verModificarDatos(p_sesion):
    fc.limpiarPantalla()
    p_sesion["Datos"]._muestraDatos()
    modifica = input("\n¿Desea modificar algun dato? (s/n) ").lower()
    if modifica == "s":
        if p_sesion["tipo_usuario"] == "estudiante":
            p_sesion["Datos"]._modificaDatos(1)