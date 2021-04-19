# pylint: disable=import-error

import bbdd.bbdd as base

class Persona():
    
    _conect = base.bbdd
    
    def __init__ (self,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        self.dni = p_dni
        self.nombre = p_nombre
        self.email = p_email
        self.fechaNac = p_fechaNac

    def materias(self,p_legajo,p_procedimiento,p_anio_cursada = None):
        lista_materias = {}
        consulta = self._conect.procedimiento(p_procedimiento,[p_legajo,p_anio_cursada])
        for materia in consulta:
            materia_a_insertar = Materia(materia[0],materia[1],materia[2])
            lista_materias[materia_a_insertar.id] = materia_a_insertar
        return lista_materias

class Docente(Persona):
    def __init__ (self,p_dni,p_nombre,p_email,p_legajo,p_domicilio,p_telefono,p_fechaNac):
        super().__init__(p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac)
        self.legajo=p_legajo
        self.materias = []

    def getMaterias(self,p_anio = None):
        self.lista_materias = super().materias("materias_por_docente",self.legajo,p_anio)

class Estudiante(Persona):

    def __init__(self,p_legajo,p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac):
        super().__init__(p_dni,p_nombre,p_email,p_domicilio,p_telefono,p_fechaNac)
        self.legajo=p_legajo
        self._materias = {}
        self.carreras = []
    

    def _promedio (self,p_anio_cursada):
        consulta = super()._conect.procedimiento("promedio",[self.legajo,p_anio_cursada])
        promedio = consulta[0][0]
        return promedio
    
    def _getMaterias(self,p_anio = None):
        materias = super().materias(self.legajo,"materias_por_estudiante",p_anio)
        return materias

class Materia():

    conect = base.bbdd

    def __init__(self,p_id,p_nombre,p_horas_totales,p_ciclo = None,):
        self.id = p_id
        self.nombre = p_nombre
        self.ciclo_lectivo = p_ciclo
        self.horas_totales = p_horas_totales
    
    def imprimeObjeto(self):
        print("\nID: {}\nNombre: {}\nCiclo lectivo: {}\nHoras totales: {}".format(self.id,self.nombre,self.ciclo_lectivo,self.horas_totales))
    
    def _alumnosInscriptos(self,p_anio = None):
        asistentes = {}
        consulta = self.conect.procedimiento("proy_inst_f_asistenciasMateria",[self.id,p_anio])
        for alumno in consulta:
            asistentes[alumno[0]] = alumno[1]
        return asistentes

class Carrera():
    
    conect = base.bbdd

    def __init__(self,p_id,p_nombre,p_titulo,p_nivel):
        self.id = p_id
        self.nombre = p_nombre
        self.titulo = p_titulo
        self.nivel = p_nivel
        self.materias = self.getMaterias()

    def getMaterias(self):
        lista_materias = {}
        consulta = self.conect.procedimiento("materias_por_carrera",[self.id])
        for materia in consulta:
            materia_a_insertar = Materia(materia[4],materia[5],materia[7],materia[6])
            lista_materias[materia_a_insertar.id] = materia_a_insertar
        return lista_materias
    
    def getHorasTotales(self):
        horas_totales = 0
        for materia in self.materias:
            horas_totales = horas_totales + self.materias[materia].horas_totales
        return horas_totales
    
    def imprimeObjeto(self,p_imprimeMateria):
        print("\nInformacion de Carrera: "+self.nombre)
        print("\nID: {}\nTitulo: {}\nNivel: {}\nHoras totales: {}".format(self.id,self.titulo,self.nivel,self.getHorasTotales()))
        if p_imprimeMateria:
            print("\nMaterias\n")
            for materia in self.materias:
                self.materias[materia].imprimeObjeto()