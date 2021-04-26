# coding: utf-8
# Para instalar
# pylint: disable=import-error
# $ pip install --user -U nltk

import nltk
from nltk import word_tokenize, Text, FreqDist
from nltk.chat.util import Chat, reflections
import re
import random
import App_POO.bbdd.bbdd as base
from datetime import datetime
from datetime import timedelta


#from BD.pgdatabase import DB

# Se aplican expresiones regulares para determinar lo que ingresa el/la usuario/a
# (.*) representa cualquier cadena luego o antes de una palabra o frase.
# Por ejemplo mi nombre es (.*) hace match con "mi nombre es Sam", "mi nombe es Mariano Moreno",
# "mi nombre es Lucia pero me dice Lu"
# Luego en la respuesta, la referencia a %1 indica la expresión que tenga (.*),
# por ejemplo la respuesta a "mi nombre es Sam" sería "Hola Sam, como estas ?"


class MyChat(Chat):

    conect = base.bbdd

    etiquetas = {}

    def __init__(self, pairs, reflections={}):

        # add `z` because now items in pairs have three elements
        self._pairs = [(re.compile(x), y, z) for (x, y, z) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()



    def respond(self, str):

        """
        Redefinimos el método que genera la respuesta.
        El objetivo es poder hacer el análisis de palabras.

        :type str: str
        :param str: Cadena a ser mapeada para dar respuesta
        :rtype: str
        """

        flag_match = True
        if(flag_match):
            # desarma una cadena en tokens (palabras o  etiquetas) y uso un diccionario para
            # contar ocurrencias.
            tokens = word_tokenize(str)
            for tok in tokens:
                if tok not in self.etiquetas:
                    self.etiquetas[tok] = 1
                else:
                    self.etiquetas[tok] += 1

            flag_match = False

        # Bucle que verifica si el parámetro hace match con alguna de las reglas.
        # En base a esto elabora la respuesta y llama a una función si aplica.

        for (pattern, response, callback) in self._pairs:
            match = pattern.match(str)

            if match:

                resp = random.choice(response)
                #resp = self._wildcards(resp, match)
                
                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'

                # run `callback` if exists
                if callback: # eventually: if callable(callback):
                    var = str.split()[1]
                    menu = "\n\n****************************************************\nSI DESEA                                   INGRESE\nIr al menú principal docente               MENU_DOC\nIr al menú principal estudiante            MENU_EST\nIr al menú principal invitado              MENU_INV\nVolver al inicio                           INICIO\nSalir                                      SALIR\n****************************************************"
                    function = callback(match,var)
                    resp = resp.format(function)+menu
                return resp

def get_nomape_docente(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_nomape_docente",[p_legajo])[0][0]
    return consulta

def get_nomape_estudiante(match,p_dni):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_nomape_estudiante",[p_dni])[0][0]
    return consulta

def get_datos_materias(match,p_materia):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_datos_materia",[p_materia])[0][0]
    return consulta

def get_titulo_carrera(match,p_carrera):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_titulo_carrera",[p_carrera])[0][0]
    return consulta

def get_nivel_carrera(match,p_carrera):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_nivel_carrera",[p_carrera])[0][0]
    return consulta

def get_materias_carreras(match,p_carrera):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_materias_carreras",[p_carrera])
    retorno = ''
    for materia in consulta:
        retorno = retorno +"Año: " +str(materia[0]) +' - Materia: '+ materia[1]+"\n"
    return retorno

def get_datos_docentes_por_nombre(match,p_nombre):
    p_legajo = None
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_datos_docentes",[p_legajo,p_nombre])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Apellido y nombre: " +dato[0] +' - Email: '+ dato[1]+"\n"
    return retorno

def get_datos_docentes_por_legajo(match,p_legajo):
    p_nombre = None
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_datos_docentes",[p_legajo,p_nombre])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Apellido y nombre: " +dato[0] +' - Email: '+ dato[1]+"\n"
    return retorno

def get_datos_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_datos_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Apellido y nombre: " +dato[0] +' - Email: '+ dato[1]+"\n"
    return retorno

def get_legajo_estudiante(match,p_dni):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_legajo_estudiantes",[p_dni])[0][0]
    return consulta

def get_legajo_docente(match,p_dni):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_legajo_docentes",[p_dni])[0][0]
    return consulta

def get_matriculas_estudiantes(matc,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_matriculaciones_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Carrera: " +dato[0] +' - Materia: '+ dato[1]+' - Anio: '+ str(dato[2])+"\n"
    return retorno

def get_notas_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_notas_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "Materia: "+dato[0] + '- Tipo de examen: '+dato[1] +'- Fecha: '+ str(dato[2]) +'- Nota: '+str(dato[3])+"\n"
    return retorno

def get_notas_aprobadas_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_notas_aprobadas_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "Materia: "+dato[0] + '- Tipo de examen: '+dato[1] +'- Fecha: '+ str(dato[2]) +'- Nota: '+str(dato[3])+"\n"
    return retorno

def get_notas_desaprobadas_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_notas_desaprobadas_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "Materia: "+dato[0] + '- Tipo de examen: '+dato[1] +'- Fecha: '+ str(dato[2]) +'- Nota: '+str(dato[3])+"\n"
    return retorno

def get_ausencia_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_ausencia_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "- Materia: "+dato[0]+ "- Fecha: "+str(dato[1])+"\n"
        
    return retorno

def get_presencia_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_presencia_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "- Materia: "+dato[0]+ "- Fecha: "+str(dato[1])+"\n"
    return retorno


def get_asistencia_estudiantes(match,p_legajo):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_asistencia_estudiantes",[p_legajo])
    retorno = ''
    for dato in consulta:
        retorno = retorno + "- Materia: "+dato[0]+ "- Fecha: "+str(dato[1])+"- Asistencia: "+dato[2]+"\n"
    return retorno


def get_datos_institucionales_contacto(match,p_dato):
    consulta = base.bbdd.procedimiento("proy_inst_f_datos_institucionales_contacto",[p_dato])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Domicilio: "+dato[0]+"- Localidad: "+dato[1]+"- Teléfonos: "+dato[2]+"- Email: "+dato[3]+"- Facebook: "+dato[4]+"\n"
    return retorno

def get_datos_institucionales(match,p_dato):
    consulta = base.bbdd.procedimiento("proy_inst_f_datos_institucionales",[p_dato])
    retorno = ''
    for dato in consulta:
        retorno = retorno +"Región: "+str(dato[0])+"- Distrito: "+str(dato[1])+"- Nombre: "+dato[2]+"- Establecimiento: "+dato[3]+"\n"
    return retorno


pares = [
    [   r"INICIO",
        ["Hola soy un bot, eres estudiante, docente o invitado?"],None
    ],

    [   r"(.*)docente|docente(.*)|(.*)docente(.*)|docente",
        ["\nIngrese la letra 'L'+ espacio, seguido de su número de legajo"],None
    ],
    [
        r"(L [0-9]{1,2})",
        ["\nHola {}. Si desea saber\nACERCA DE                  INGRESE\nInformación general	     INFO\nmaterias                   MATERIA\ncarreras                   CARRERA\ndatos de docentes          DDOC\ndatos de estudiantes       DEST\n"],
        get_nomape_docente
    ],
    [
        r"MENU_DOC",
        ["\nSi desea saber\nACERCA DE                  INGRESE\nInformación general	   INFO\nMaterias                   MATERIA\nCarreras                   CARRERA\nDatos de docentes          DDOC\nDatos de estudiantes       DEST\n"],None
    ],
    [   r"MATERIA",
        ["\nIngrese la letra 'M'+ espacio, seguido el nombre de la materia."],None

    ],
    [   r"M (.*)",
        ["\n{}"],
        get_datos_materias
    ],
    [   r"CARRERA",
        ["\nCARRERA: Profesorado de educacion inicial\nSi desea saber        \nACERCA DE       INGRESE        \nMaterias        CM+espacio+I        \nTitulo          CT+espacio+I        \nNivel           CN+espacio+I        \n\nCARRERA: Profesorado de educacion especial\nSi desea saber        \nACERCA DE       INGRESE        \nMaterias        CM+espacio+E        \nTitulo          CT+espacio+E        \nNivel           CN+espacio+E        \n\nCARRERA: Tecnicatura superior en analisis desarrollo y programacion de aplicaciones\nSi desea saber        \nACERCA DE       INGRESE        \nMaterias        CM+espacio+A        \nTitulo          CT+espacio+A        \nNivel           CN+espacio+A\n"],None
    ],
    [   r"CT (.*)",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese CARRERA"],
        get_titulo_carrera
    ],
    [   r"CN (.*)",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese CARRERA"],
        get_nivel_carrera
    ],
    [   r"CM (.*)",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese CARRERA"],
        get_materias_carreras
    ],
    [   r"DDOC",
        ["\nIngrese el DD + espacio seguido del número de legajo del docente\n"],None
    ],
    [   r"(DD [0-9]{1,2})",
        ["\n{}"],
        get_datos_docentes_por_legajo
    ],
    [   r"NDOC (.*)",
        ["\n{}"],
        get_datos_docentes_por_nombre
    ],
    [   r"DEST",
        ["\nIngrese el DE + espacio seguido del número de legajo del estudiante\n"],None
    ],
    [   r"(DE [0-9]{1,2})",
        ["\n{}"],
        get_datos_estudiantes
    ],
    
    [   r"(.*)estudiante|estudiante(.*)|(.*)estudiante(.*)|estudiante",
        ["\nIngrese 'DNI'+ espacio, seguido de su número de dni"],None
    ],
    [   r"(DNI [0-9]{8})",
        ["\nHola {}.\nSi desea saber\nACERCA DE                  INGRESE\nInformación general	   INFO\nmatriculación		   MATRICULACION\nnotas			   NOTAS\nasistencia		   ASISTENCIAS"],
        get_nomape_estudiante
    ],
    [   r"MENU_EST",
        ["\nSi desea saber\nACERCA DE                  INGRESE\nInformación general	   INFO\nMatriculación		   MATRICULACION\nNotas			   NOTAS\nAsistencia		   ASISTENCIAS"],None
    ],
    [   r"legajo|(.*)legajo|legajo(.*)|(.*)legajo(.*)",
        ["\nSI ES          INGRESE        \nEstudiante     LEG_EST + espacio + Nro de DNI        \nDocente        LEG_DOC + espacio + Nro de DNI"],None
    ],
    [   r"(LEG_EST [0-9]{8})",
        ["\nTu número de legajo es {}."],
        get_legajo_estudiante
    ],
    [   r"(LEG_DOC [0-9]{8})",
        ["\nTu número de legajo es {}."],
        get_legajo_docente
    ],
    [   r"MATRICULACION",
        ["\nIngrese MMAT + espacio + Nro de legajo"],None
    ],
    [   r"(MMAT [0-9]{1,2})",
        ["\n{}"],
        get_matriculas_estudiantes
    ],
    [   r"NOTAS",
        ["\nSi desea saber\nACERCA DE                INGRESE\nNotas aprobadas	         VMNOT + espacio + Nro de legajo\nNotas desaprobadas	 FMNOT + espacio + Nro de legajo\nTodas las notas	         MNOT + espacio + Nro de legajo"],None
    ],
    [   r"(MNOT [0-9]{1,2})",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese NOTAS"],
        get_notas_estudiantes
    ],
        [r"(VMNOT [0-9]{1,2})",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese NOTAS"],
        get_notas_aprobadas_estudiantes
    ],
        [r"(FMNOT [0-9]{1,2})",
          ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese NOTAS"],
        get_notas_desaprobadas_estudiantes
    ],
    [   r"ASISTENCIAS",
        ["\nSi desea saber        \nACERCA DE                INGRESE\nPresencias     	         VMASIS + espacio + Nro de legajo\nAusencias                FMASIS + espacio + Nro de legajo\nTodas las asistencias    MASIS + espacio + Nro de legajo"],None
    ],
    [   r"(FMASIS [0-9]{1,2})",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese ASISTENCIAS"],
        get_ausencia_estudiantes
    ],
    [   r"(VMASIS [0-9]{1,2})",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese ASISTENCIAS"],
        get_presencia_estudiantes
    ],
    [   r"(MASIS [0-9]{1,2})",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese ASISTENCIAS"],
        get_asistencia_estudiantes
    ],
    [   r"(.*)invitado|invitado(.*)|(.*)invitado(.*)|invitado|MENU_INV",
        ["\nHola. Si desea saber\nACERCA DE                  INGRESE\nInformación general	   INFO\nMaterias                   MATERIA\nCarreras                   CARRERA\nDatos de docentes          NDOC + espacio + nombre del docente"],None
    ],
    [   r"INFO",
        ["\nSi desea información\nACERCA DE                  INGRESE\nDatos de contacto          DATOS + espacio + INFO\nDatos institucionales      INST + espacio + INFO"],None
    ],
    [   r"DATOS (.*)",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese INFO"],
        get_datos_institucionales_contacto
    ],
    [   r"INST (.*)",
        ["\n{}\n\n****************************************************\nSi desea volver al menú anterior ingrese INFO"],
        get_datos_institucionales
    ],


]
mis_reflexions = {
    "ir": "fui",
    "hola": "hey",
    "docente":"profesor",
    "estudiante":"alumno",
    "particular":"interesado",
    "nombre y apellido":"apellido y nombre",
    "nombre":"apellido",
    "dni":"documento",
    "asistencia":"asistencias",
    "carrera":"carreras",
    "materia":"materias",
    "datos de docente":"datos de docentes",
    "datos de docente":"datos docente",
    "datos de docente":"datos docentes"
}

def chatear():
    print("Hola soy un bot, eres estudiante, docente o invitado?")
    chat = MyChat(pares, mis_reflexions)
    chat.converse()

# Indica que el incio del programa llama a la función chatear
if __name__ == "__main__":
    chatear()
