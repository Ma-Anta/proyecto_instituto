# pylint: disable=import-error
import bbdd.bbdd as base
import clases.clases as clase

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

def busquedaDocente(p_legajo_docente = None):
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