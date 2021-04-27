# pylint: disable=import-error
import bbdd.bbdd as base
import clases.clases as clase
import os
import platform
import getpass as gp

#FUNCIONES

#FUNCION PARA BUSQUEDA DE CARRERAS O MATERIAS - SE AGRUPA PORQUE EL CODIGO ES IGUAL PARA AMBAS, CON LEVES CAMBIOS.
def busquedaCarMat(p_busqueda,p_id = None):
    diccionario = {}
    try:
        consulta = "SELECT * FROM {}".format(p_busqueda)
        if p_id != None:
            consulta = consulta + "WHERE {}.id = {}".format(p_busqueda,p_id)
        datos = base.bbdd.ejecutar(consulta)
        for elemento in datos:
            if p_busqueda == 1:
                carrera_a_agregar = clase.Carrera(elemento[0],elemento[1],elemento[2],elemento[3])
                diccionario[carrera_a_agregar.id] = carrera_a_agregar
            else:
                materia_a_agregar = clase.Materia(elemento[0],elemento[1],elemento[2])
                diccionario[materia_a_agregar.id] = materia_a_agregar
        return diccionario
    except ValueError:
        print("\nError en la busqueda de carreras/materias.\n",ValueError)
#FUNCION PARA BUSCAR PERSONAS - SE AGRUPA EN UNA PORQUE EL CODIGO PARA ESTUDIANTES O DOCENTES ES EL MISMO, CON ALGUNOS CAMBIOS.
def busquedaPersona(p_tipo,p_nombre = None,p_legajo = None):
    dictPersona = {}
    consulta = "SELECT * FROM {}".format(p_tipo)
    try:
        if p_legajo != None:
            consulta = consulta+" WHERE {}.legajo = {}".format(p_tipo,p_legajo)
        if p_nombre != None:
            consulta = consulta+" WHERE apellido_nombre LIKE '%{}%'".format(p_nombre)
        personas = base.bbdd.ejecutar(consulta)
        for persona in personas:
            if p_tipo == "docente":
                persona_a_ingresar = clase.Docente(persona[0],persona[1],persona[2],persona[3],persona[4],persona[5],persona[6])
            else:
                persona_a_ingresar = clase.Estudiante(persona[0],persona[1],persona[2],persona[3],persona[4],persona[5],persona[6])
            dictPersona[persona_a_ingresar._legajo] = persona_a_ingresar
        return dictPersona
    except:
        print("\nError al buscar persona.\n")
#FUNCION PARA IMPRIMIR LA INFORMACION DE LAS PERSONAS. SOLO RECORRE EL DICCIONARIO DADO POR LA FUNCION ANTERIOR Y LLAMA AL METODO QUE MUESTRA LA INFO.
def imprimirPersona(p_diccionario):
    for persona in p_diccionario:
        p_diccionario[persona]._muestraDatos(False)
#FUNCION DE BUSQUEDA ASISTENCIAS - EN EL CASO DE UN DOCENTE BUSCA LA ASISTENCIA DE LOS ALUMNOS DE SUS MATERIAS.
#EN EL CASO DE UN ALUMNO, BUSCA SUS ASISTENCIAS PARA SUS MATERIAS.
def busquedaAsistencias(p_sesion,consulta):
    try:
        id = materiasDisponibles(p_sesion["Datos"])
        if id == None:
            print("\nError: Materia no disponible.\n")
        else:
            anio = int(input("\nIngrese año: "))
            if consulta == 1:
                if p_sesion["tipo_usuario"] == "estudiante":
                    asistencias = p_sesion["Datos"]._verAsistencias(id,anio)
                else:
                    consulta = "select fecha,legajo,estudiante,asistencia from proy_inst_v_asistenciasmaterias where id_materia = {} and EXTRACT(year from fecha) = {}".format(id,anio)
                    asistencias = p_sesion["Datos"]._conect.ejecutar(consulta)
                for asistencia in asistencias:
                    if asistencia[3] == True:
                        presencia = "Presente"
                    else:
                        presencia = "Ausente"
                    print("\nFecha: {}\nLegajo: {}\nNombre: {}\nAsistencia: {}".format(asistencia[0],asistencia[1],asistencia[2],presencia))            
            elif consulta == 2:
                if p_sesion["tipo_usuario"] == "estudiante":
                    legajo = p_sesion["Datos"]._legajo
                else:
                    legajo = alumnosAnotados(p_sesion["Datos"]._materias[id],anio)
                consulta = "SELECT * FROM estudiante where legajo = {}".format(legajo)
                respuesta = p_sesion["Datos"]._conect.ejecutar(consulta)
                alumno = clase.Estudiante(respuesta[0][0],respuesta[0][1],respuesta[0][2],respuesta[0][3],respuesta[0][4],respuesta[0][5],respuesta[0][6])
                porc_asistencia = alumno._porcentajeAsistencia(id,anio)
                if porc_asistencia == None:
                    print("\nAlumno no encontrado en la materia\n")
                else:
                    print("Procentaje de asistencia de {}: {}%".format(alumno._nombre,porc_asistencia))
    except ValueError:
        print("\nError al buscar asistencias.\n",ValueError)
#FUNCION DE BUSQUEDA DE NOTAS - LOS DOCENTES PUEDEN VER LAS NOTAS DE LOS ALUMNOS EN SUS MATERIAS.
#LOS ALUMNOS PUEDEN VER SUS NOTAS, EN SUS MATERIAS.
def busquedaNotas(p_sesion):
    id = materiasDisponibles(p_sesion["Datos"])
    if p_sesion["tipo_usuario"] == "estudiante":
        notas = p_sesion["Datos"]._getNotaMateria(p_materia_id = id)
        for nota in notas:
            print("\nMateria: {}".format(nota))
            for informacion in notas[nota]:
                print("\nFecha: {}\nNota: {}\nTipo nota: {}".format(informacion[0],informacion[1],informacion[2]))
    else:
        consulta = "select pivne.estudiante_legajo,pivne.apellido_nombre,pivne.fecha,pivne.descripcion,pivne.nota from proy_inst_v_notas_estudiantes pivne where materia_id = {}".format(id)
        notas = p_sesion["Datos"]._conect.ejecutar(consulta)
        for nota in notas:
            print("\nNOTAS")
            print("\nLegajo: {}\nNombre: {}\nFecha: {}\nTipo de nota: {}\nNota: {}".format(nota[0],nota[1],nota[2],nota[3],nota[4]))
#FUNCION QUE CREA LA SESION EN EL SISTEMA.
def sesionUsuario(p_usuario,p_tipo):
    sesion = {}
    try:
        sesion["nombre_usuario"] = p_usuario
        sesion["tipo_usuario"] = p_tipo
        consulta = "SELECT * FROM {tabla} WHERE {condicion} = '{user}'"
        if p_tipo == 'estudiante':
            consulta = consulta.format(tabla = "ESTUDIANTE",condicion = "estudiante.usuario",user=p_usuario)
            res_cons = base.bbdd.ejecutar(consulta)[0]
            usuario = clase.Estudiante(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
        elif p_tipo == "docente":
            consulta = consulta.format(tabla = "DOCENTE",condicion = "docente.usuario",user=p_usuario)
            res_cons = base.bbdd.ejecutar(consulta)[0]
            usuario = clase.Docente(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
        elif p_tipo == "preceptor":
            consulta = consulta.format(tabla = "PRECEPTOR",condicion = "preceptor.usuario",user=p_usuario)
            res_cons = base.bbdd.ejecutar(consulta)[0]
            usuario = clase.Preceptor(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
        sesion["Datos"] = usuario
        return sesion
    except:
        print("\nError al generar datos de sesion.\n")
#FUNCION QUE INICIA SESION. PARA ESTO, RECUPERA LA CONTRASEÑA DEL USUARIO TRAIDA DEL SISTEMA Y CHEQUEA LA VALIDEZ DE LA 
#CONTRASEÑA INGRESADA POR EL USUARIO. DA LOS MENSAJES DE ERROR NECESARIOS EN CADA CASO.
def iniciarSesion(p_usuario):
    try:
        resultado_consulta = base.bbdd.procedimiento("obtenerCredencial",[p_usuario])[0]
        contrasenia = resultado_consulta[1]
        tipo_usuario = resultado_consulta[0]
        if contrasenia == "Usuario invalido":
            return contrasenia,None
        else:
            passwordIngresada = gp.getpass("Ingrese contraseña: ")
            if contrasenia == passwordIngresada:
                return True,tipo_usuario
            else:
                return 'Contraseña invalida',None
    except:
        print("\nError al iniciar sesion.\n")
#FUNCION QUE IMPRIME LAS MATERIAS DISPONIBLES DEL USUARIO.
def materiasDisponibles(usuario):
    try:
        print("\nMaterias disponibles: ")
        usuario._muestraMaterias(False)
        id = int(input("\nIngrese ID de materia: "))
        if id not in usuario._materias.keys():
            return None
        else:
            return id
    except:
        print("\nError al listar las materias disponibles.\n")
#FUNCION QUE MUESTRA LOS ALUMNOS ANOTADOS PARA UNA MATERIA.
def alumnosAnotados(p_materia,p_anio):
    try:
        print("\nAlumnos inscriptos")
        p_materia._muestraAlumnos(p_anio)
        legajo = int(input("\nIngrese legajo del alumno: "))
        return legajo
    except:
        print("\nError al buscar alumnos inscriptos.")
#FUNCION USADA PARA ELEGIR EL TIPO DE NOTA EN LA INSERCION DE DATOS
def elegirTipoNota():
    tipo_notas = base.bbdd.ejecutar("SELECT * FROM tipo_nota")
    for tipo in tipo_notas:
        print("\nID: {}\nTipo: {}".format(tipo[0],tipo[1]))
    tipo = int(input("\nIngrese id de la nota a ingresar: "))
    return tipo