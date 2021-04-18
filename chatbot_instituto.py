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
                    function = callback(match,var)
                    resp = resp.format(function)
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

"""def get_materias_carrera(match,p_carrera):
    consulta = base.bbdd.procedimiento("proy_inst_f_obtener_materias_carrera",[p_carrera])[0][0]
    return consulta
"""
"""     def get_asistencia_x_fechas(self,p_fecha_desde,p_fecha_hasta):
        consulta = self.conect.procedimiento("",[p_fecha_desde,p_fecha_hasta])[0][0]
        return consulta
"""
pares_docentes = [
    [   r"(.*)docente|docente(.*)|docente",
        ["Ingrese la letra 'L'+ espacio, seguido de su número de legajo"],None
    ],
    [
        r"(L [0-9]{1,2})",
        ["Hola {}. Desea saber acerca de materias, carreras, datos de docentes o datos de estudiantes?"],
        get_nomape_docente
    ],
    [   r"(.*)materia|materia(.*)|(.*)materia",
        ["Ingrese la letra 'M'+ espacio, seguido el nombre de la materia."],None

    ],
    [   r"M (.*)",
        ["{}"],
        get_datos_materias
    ],
    [   r"(.*)carrera|carrera(.*)|(.*)carrera",
        ["CARRERA: Profesorado de educacion inicial\nSi desea saber        \nACERCA DE     INGRESE        \nMaterias        CM+espacio+I        \nTitulo          CT+espacio+I        \nNivel           CN+espacio+I        \n\nCARRERA: Profesorado de educacion especial\nSi desea saber        \nACERCA DE     INGRESE        \nMaterias        CM+espacio+E        \nTitulo          CT+espacio+E        \nNivel           CN+espacio+E        \n\nCARRERA: Tecnicatura superior en analisis desarrollo y programacion de aplicaciones\nSi desea saber        \nACERCA DE     INGRESE        \nMaterias        CM+espacio+A        \nTitulo          CT+espacio+A        \nNivel           CN+espacio+A        \n"],None
    ],
    [   r"CT (.*)",
        ["{}"],
        get_titulo_carrera
    ],
    [   r"CN (.*)",
        ["{}"],
        get_nivel_carrera
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
    "materia":"materias"
    
}

def chatear():
    print("Hola soy un bot, eres estudiante, docente o particular?")
    chat = MyChat(pares_docentes, mis_reflexions)
    chat.converse()

# Indica que el incio del programa llama a la función chatear
if __name__ == "__main__":
    chatear()
