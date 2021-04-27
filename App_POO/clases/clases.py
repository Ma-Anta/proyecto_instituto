# pylint: disable=import-error
import re
import bbdd.bbdd as base
from abc import ABC,abstractmethod

#CLASES.

class Persona():
    #SE ESPERABA PODER MANEJAR INSERCIONES Y MODIFICACIONES DE DATOS CON EXPRESIONES REGULARES PARA VALIDARLOS.
    _conect = base.bbdd
    _validaMail = re.compile(r"""\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b""")
    _validaFecha = re.compile(r"""[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}""")
    _ValidaDNI = re.compile(r"""[0-9]{8}""")
    #CONSTRUCTOR
    def __init__ (self,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        self._dni = p_dni
        self._nombre = p_nombre
        self._email = p_email
        self._domicilio = p_domicilio
        self._telefono = p_telefono
        self._fechaNac = p_fechaNac
    #SE CREA METODO MATERIAS EN LA CLASE PADRE PORQUE ES EL MISMO METODO PARA ESTUDIANTES Y ALUMNOS
    #SOLO SE PASA POR PARAMETRO EL PROCEDIMIENTO DE LA BASE DE DATOS CORRESPONDIENTE.
    def materias(self,p_legajo,p_procedimiento,p_anio_cursada = None):
        lista_materias = {}
        consulta = self._conect.procedimiento(p_procedimiento,[p_legajo,p_anio_cursada])
        for materia in consulta:
            materia_a_insertar = Materia(materia[0],materia[1],materia[2])
            lista_materias[materia_a_insertar.id] = materia_a_insertar
        return lista_materias
    #METODO PARA MOSTRAR LA INFORMACION DE LA PERSONA.
    #SE USA UN VALOR BOOLEANO PARA DETERMINAR SI SE MUESTRAN TODOS LOS DATOS, O ALGUNOS.
    def _muestraDatos(self,p_todos):
        if p_todos:
            print("\nMis datos: ")
            print("\nDNI: {}\nNombre: {}\nEmail: {}\nDomicilio: {}\nTelefono: {}\nFecha de nacimiento: {}".format(self._dni,self._nombre,self._email,self._domicilio,self._telefono,self._fechaNac))
        else:
            print("\nDATOS: ")
            print("\nNombre: {}\nEmail: {}\nTelefono: {}".format(self._nombre,self._email,self._telefono))
    #FUNCION QUE SE ESPERABA QUE MODIFIQUE DATOS PERSONALES. NO ESTA TERMINADA.
    def _modificaDatos(self,p_tipo):
        dato = (input("\n¿Que dato desea modificar? ")).lower()
        exit = False
        while exit != True:
            if dato == "dni":
                dni = input("\nIngrese DNI sin puntos ni comas: ")
                if self._ValidaDNI.match(dni):
                    dni = int(dni)
                    self._dni = dni
                else:
                    print("\nDNI incorrecto, ingrese solo numeros.")
            elif "nombre" in dato:
                name = input("\nIngrese nuevo apellido y nombre: ")
                self._nombre = name
            elif dato == "email":
                email = input("\nIngrese email nuevo: ")
                if self._validaMail.match(email):
                    self._email = email
                else:
                    print("\nEmail invalido.")
            elif dato == "domicilio":
                domicilio = input("\nIngrese nuevo domicilio: ")
                self._domicilio = domicilio
            elif dato == "telefono":
                telefono = input("\nIngrese nuevo numero de telefono (solo numeros): ")
                try:
                    telefono = int(telefono)
                    self._telefono = telefono
                except:
                    print("\nNumero de telefono no valido.")
            elif "nacimiento" in dato:
                fecha = input("Ingrese nueva fecha de nacimiento (formato: yyyy-MM-dd): ")
                if self._validaFecha.macth(fecha):
                    self._fechaNac = fecha
                else:
                    print("\nFecha invalida.")
            seguir = input("\n¿Desea modificar otro dato? (s/n)")
            if seguir == "n":
                exit = True
    #FUNCION QUE SE ESPERABA SIRVA PARA MODIFICAR LA CONTRASEÑA DEL USUARIO.
    def _cambiaContraseña(self,p_tipo):
        pass

class Preceptor(Persona):
    def __init__ (self,p_legajo,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        super().__init__(p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac)
        self._legajo=p_legajo

    def _insertaAsistencia(self,p_datos):
        insercion = self._conect.procedimiento("proy_inst_f_alta_asistencias",p_datos)
        return insercion
    
    def _insertaNotas(self,p_datos):
        insercion = self._conect.procedimiento("proy_inst_f_alta_notas",p_datos)
        return insercion

    def _crearUsuario(self,p_datos):
        pass

    def _insertaDocenteEstudiante(self,p_tipo,p_datos):
        pass

    def _insertaCarrera_Materia(self,p_tipo,p_datos):
        pass

class Docente(Persona):
    def __init__ (self,p_legajo,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        super().__init__(p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac)
        self._legajo=p_legajo
        self._materias = self._getMaterias()
    #EL DOCENTE OBTIENE LAS MATERIAS A SU CARGO.
    def _getMaterias(self,p_anio = None):
        materias = super().materias(self._legajo,"materias_por_docente",p_anio)
        return materias
    #METODO QUE MUESTRA LAS MATERIAS A CARGO DEL DOCENTE.
    def _muestraMaterias(self,p_verDoc):
        for materia in self._materias:
            self._materias[materia]._imprimeObjeto(p_verDoc)

class Estudiante(Persona):

    def __init__(self,p_legajo,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        super().__init__(p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac)
        self._legajo=p_legajo
        self._materias = self._getMaterias()
        self._carreras = {}
    #CALCULO DEL PROMEDIO DE NOTAS.
    def _promedio (self,p_anio_cursada):
        consulta = super()._conect.procedimiento("promedio",[self._legajo,p_anio_cursada])
        promedio = consulta[0][0]
        return promedio
    #OBTENCION DE LAS MATERIAS A LAS CUALES ESTA MATRICULADO EL ALUMNO
    def _getMaterias(self):
        materias = super().materias(self._legajo,"materias_por_estudiante",None)
        return materias
    #OBTENCION DE NOTAS DEL ESTUDIANTE
    def _getNotaMateria(self,p_materia_id = None,p_anio = None):
        listado_notas = {}
        lista_notas = self._conect.procedimiento("proy_inst_f_notas_estudiantes",[p_materia_id,self._legajo,p_anio])
        for materia in lista_notas:
            listado_notas[materia[0]] = []
        for materia in lista_notas:
            listado_notas[materia[0]].append(materia[1::])
        return listado_notas
    #OBTENCION DE ASISTENCIAS DEL ESTUDIANTE
    def _getAsistencia(self,p_materia_id = None,p_anio = None):
        consulta = "select ae.materia_id,ae.fecha,ae.asistencia from asistencia_estudiantes ae where ae.estudiante_legajo = {}".format(self._legajo)
        if p_materia_id != None:
            consulta = consulta + " and materia_id = {}".format(p_materia_id)
        elif p_anio != None:
            consulta = consulta + " and EXTRACT(YEAR from ae.fecha) = {}".format(p_anio)
        lista_asistencia = self._conect.ejecutar(consulta)
        return lista_asistencia
    #MUESTRA ASISTENCIAS
    def _verAsistencias(self,p_materia_id = None,p_anio = None):
        listaAsistencias = self._getAsistencia(p_materia_id,p_anio)
        print(listaAsistencias)
        for asistencia in listaAsistencias:
            if asistencia[2] == True:
                presencia = "Presente"
            else:
                presencia = "Ausente"
            print("\nFecha: {}\nAsistencia: {}".format(asistencia[1],presencia))
    #CALCULO DE PORCENTAJES DE ASISTENCIA
    def _porcentajeAsistencia(self,p_materia_id = None,p_anio = None):
        lista_asistencias = self._getAsistencia(p_materia_id,p_anio)
        if lista_asistencias == []:
            return None
        else:
            total = 0
            presencias = 0
            for asistencia in lista_asistencias:
                total +=1
                if asistencia[2] == True:
                    presencias += 1        
            return round(((presencias*100)/total))
    #MOSTRAR LAS MATERIAS A LAS QUE EL ALUMNO ESTA MATRICULADO
    def _muestraMaterias(self,p_verDoc):
        for materia in self._materias:
            self._materias[materia]._imprimeObjeto(p_verDoc)

class Materia():

    conect = base.bbdd

    def __init__(self,p_id,p_nombre,p_horas_totales,p_ciclo = None,):
        self.id = p_id
        self.nombre = p_nombre
        self.ciclo_lectivo = p_ciclo
        self.horas_totales = p_horas_totales
        self.docentes_asignados = self._docentesAsignados()
    #IMPRIME LOS ATRIBUTOS DEL OBJETO
    def _imprimeObjeto(self,p_verDocentes):
        print("\nInformación de materia: "+self.nombre)
        print("\nID: {}\nNombre: {}\nCiclo lectivo: {}\nHoras totales: {}".format(self.id,self.nombre,self.ciclo_lectivo,self.horas_totales))
        if p_verDocentes:
            print("\nDocentes\n")
            for docente in self.docentes_asignados:
                print("\nNombre: {}\nEmail: {}".format(docente,self.docentes_asignados[docente]))
    #OBTIENE LOS ALUMNOS INSCRIPTOS EN LA MATERIA
    def _alumnosInscriptos(self,p_anio = None):
        asistentes = {}
        consulta = self.conect.procedimiento("proy_inst_f_matriculacion_materia",[self.id,p_anio])
        for alumno in consulta:
            asistentes[alumno[1]] = alumno[2]
        return asistentes
    #OBTIENE LOS DOCENTES ASIGNADOS A LA MATERIA
    def _docentesAsignados(self):
        docentes = {}
        consulta = self.conect.ejecutar("select d.apellido_nombre,d.email from materias_docentes md join docente d on md.docente_legajo = d.legajo where md.materia_id = {}".format(self.id))
        for docente in consulta:
            docentes[docente[0]] = docente[1]
        return docentes
    #MUESTRA LOS ALUMNOS
    def _muestraAlumnos(self,p_anio = None):
        alumnos = self._alumnosInscriptos(p_anio)
        if alumnos == {}:
            print("\nSin alumnos para el año seleccionado.")
        else:
            for alumno in alumnos:
                print("\nLegajo: {}\nNombre: {}".format(alumno,alumnos[alumno]))

class Carrera():
    
    conect = base.bbdd

    def __init__(self,p_id,p_nombre,p_titulo,p_nivel):
        self.id = p_id
        self.nombre = p_nombre
        self.titulo = p_titulo
        self.nivel = p_nivel
        self.materias = self._getMaterias()
    #OBTIENE LAS MATERIAS PERTENECIENTES A LA CARRERA
    def _getMaterias(self):
        lista_materias = {}
        consulta = self.conect.procedimiento("materias_por_carrera",[self.id])
        for materia in consulta:
            materia_a_insertar = Materia(materia[4],materia[5],materia[7],materia[6])
            lista_materias[materia_a_insertar.id] = materia_a_insertar
        return lista_materias
    #CALCULA LAS HORAS TOTALES DE LA CARRERA (PARA ESTO, SUMA LAS HORAS DE CADA MATERIA)
    def _getHorasTotales(self):
        horas_totales = 0
        for materia in self.materias:
            horas_totales = horas_totales + self.materias[materia].horas_totales
        return horas_totales
    #OBTIENE LOS ALUMNOS INSCRIPTOS (NO ESTA TERMINADA)
    def _getAlumnosinscriptos(self):
        alumnos = {}
        pass
    #IMPRIME LOS ATRIBUTOS DEL OBJETO.
    def _imprimeObjeto(self,p_imprimeMateria):
        print("\nInformacion de Carrera: "+self.nombre)
        print("\nID: {}\nTitulo: {}\nNivel: {}\nHoras totales: {}".format(self.id,self.titulo,self.nivel,self._getHorasTotales()))
        if p_imprimeMateria:
            print("\nMaterias\n")
            for materia in self.materias:
                self.materias[materia]._imprimeObjeto(False)
