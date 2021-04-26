# pylint: disable=import-error
import bbdd.bbdd as base
import clases.clases as clase
import os
import platform
import getpass as gp


def busquedaCarrera(p_id_carrera = None):
    dictCarreras = {}
    try:
        if p_id_carrera == None:
            consulta = "SELECT * FROM CARRERA"
        else:
            consulta = "SELECT * FROM CARRERA WHERE carrera.id = {}".format(p_id_carrera)
        carreras = base.bbdd.ejecutar(consulta)
        for carrera in carreras:
            carrera_a_agregar = clase.Carrera(carrera[0],carrera[1],carrera[2],carrera[3])
            dictCarreras[carrera_a_agregar.id] = carrera_a_agregar
        return dictCarreras
    except:
        print("\nError al buscar carreras.\n")

def busquedaMateria(p_id_materia = None):
    dictMaterias = {}
    try:
        if p_id_materia == None:
            consulta = "SELECT * FROM MATERIA"
        else:
            consulta = "SELECT * FROM MATERIA WHERE materia.id = {}".format(p_id_materia)
        materias = base.bbdd.ejecutar(consulta)
        for materia in materias:
            materia_a_agregar = clase.Materia(materia[0],materia[1],materia[2])
            dictMaterias[materia_a_agregar.id] = materia_a_agregar
        return dictMaterias
    except:
        print("\nError al buscar materias.\n")

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

def imprimirPersona(p_diccionario):
    for persona in p_diccionario:
        p_diccionario[persona]._muestraDatos(False)

def printNotasEstudiantes(p_lista_notas):
    for materia in p_lista_notas:
        print("Notas para la materia: {}".format(materia))
        for nota in p_lista_notas[materia]:
            print("\nFecha: {} Nota: {} Tipo de examen: {}".format(nota[0],nota[1],nota[2]))

def busquedaAsistencias(p_sesion,consulta):
    try:
        id = materiasDisponibles(p_sesion._sesion["Datos"])
        anio = int(input("\nIngrese año: "))
        if consulta == 1:
            consulta = "select fecha,legajo,estudiante,asistencia from proy_inst_v_asistenciasmaterias where id_materia = {} and EXTRACT(year from fecha) = {}".format(id,anio)
            asistencias = p_sesion._sesion["Datos"]._conect.ejecutar(consulta)
            for asistencia in asistencias:
                if asistencia[3] == True:
                    presencia = "Presente"
                else:
                    presencia = "Ausente"
                print("\nFecha: {}\nLegajo: {}\nNombre: {}\nAsistencia: {}".format(asistencia[0],asistencia[1],asistencia[2],presencia))            
        elif consulta == 2:
            if p_sesion["tipo_usuario"] == "estudiante":
                legajo = p_sesion._sesion["Datos"]._legajo
            else:
                legajo = int(input("\nIngrese legajo del alumno: "))
            consulta = "SELECT * FROM estudiante where legajo = {}".format(legajo)
            respuesta = p_sesion._sesion["Datos"]._conect.ejecutar(consulta)
            alumno = clase.Estudiante(respuesta[0][0],respuesta[0][1],respuesta[0][2],respuesta[0][3],respuesta[0][4],respuesta[0][5],respuesta[0][6])
            porc_asistencia = alumno._porcentajeAsistencia(id,anio)
            print("Procentaje de asistencia de {}: {}%".format(alumno._nombre,porc_asistencia))
    except:
        print("\nError al buscar asistencias.\n")

def busquedaNotas(p_usuario):
    id = materiasDisponibles(p_usuario)
    pass

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

def materiasDisponibles(usuario):
    try:
        usuario._muestraMaterias(False)
        id = int(input("\nIngrese ID de materia: "))
        if id not in usuario._materias.keys():
            print("Materia no disponible.")
        return id
    except:
        print("\nError al listar las materias disponibles.\n")
