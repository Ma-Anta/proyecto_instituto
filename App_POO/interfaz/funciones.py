# pylint: disable=import-error
import os
import platform
import bbdd.bbdd as base
import clases.clases as clase
import getpass as gp

def manejoMenu(p_menu):
    print("\n")
    for item in p_menu:
        print(item," - ",p_menu[item])
    opcion = input("\nIngrese una opcion: ")
    return opcion

def busquedaCarrera(p_id_carrera = None):
    dictCarreras = {}
    if p_id_carrera == None:
        consulta = "SELECT * FROM CARRERA"
    else:
        consulta = "SELECT * FROM CARRERA WHERE carrera.id = {}".format(p_id_carrera)
    carreras = base.bbdd.ejecutar(consulta)
    for carrera in carreras:
        carrera_a_agregar = clase.Carrera(carrera[0],carrera[1],carrera[2],carrera[3])
        dictCarreras[carrera_a_agregar.id] = carrera_a_agregar
    return dictCarreras

def busquedaMateria(p_id_materia = None):
    dictMaterias = {}
    if p_id_materia == None:
        consulta = "SELECT * FROM MATERIA"
    else:
        consulta = "SELECT * FROM MATERIA WHERE materia.id = {}".format(p_id_materia)
    materias = base.bbdd.ejecutar(consulta)
    for materia in materias:
        materia_a_agregar = clase.Materia(materia[0],materia[1],materia[2])
        dictMaterias[materia_a_agregar.id] = materia_a_agregar
    return dictMaterias

def busquedaDocente(p_legajo_docente = None,p_id_materia = None):
    dictDocentes = {}
    if p_legajo_docente == None:
        consulta = "SELECT * FROM DOCENTE"
    else:
        consulta = "SELECT * FROM DOCENTE WHERE docente.legajo = {}".format(p_legajo_docente)
    docentes = base.bbdd.ejecutar(consulta)
    for docente in docentes:
        docentes_a_ingresar = clase.Docente(docente[1],docente[2],docente[3],docente[0],docente[4],docente[5],docente[6])
        dictDocentes[docentes_a_ingresar.legajo] = docentes_a_ingresar
    return dictDocentes

def printNotasEstudiantes(p_lista_notas):
    for materia in p_lista_notas:
        print("Notas para la materia: {}".format(materia))
        for nota in p_lista_notas[materia]:
            print("\nFecha: {} Nota: {} Tipo de examen: {}".format(nota[0],nota[1],nota[2]))

def sesionUsuario(p_usuario,p_tipo):
    sesion = {}
    sesion["nombre_usuario"] = p_usuario
    sesion["tipo_usuario"] = p_tipo
    consulta = "SELECT * FROM {tabla} WHERE {condicion} = '{user}'"
    if p_tipo == 'estudiante':
        consulta = consulta.format(tabla = "ESTUDIANTE",condicion = "estudiante.usuario",user=p_usuario)
        res_cons = base.bbdd.ejecutar(consulta)[0]
        usuario = clase.Estudiante(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
    if p_tipo == "docente":
        consulta = consulta.format(tabla = "DOCENTE",condicion = "docente.usuario",user=p_usuario)
        res_cons = base.bbdd.ejecutar(consulta)[0]
        usuario = clase.Docente(res_cons[0],res_cons[1],res_cons[2],res_cons[3],res_cons[4],res_cons[5],res_cons[6])
    sesion["Datos"] = usuario
    return sesion

def iniciarSesion(p_usuario):
    limpiarPantalla()
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
            return 'Contraseña invalida',tipo_usuario

def limpiarPantalla():
    if platform.system() == "Windows":
        os.system('cls')
    elif platform.system() == "Linux":
        os.system('clear')