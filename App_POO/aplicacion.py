# pylint: disable=import-error
import interfaz.interfaz as app

#INICIO DEL PROGRAMA. INSTANCIA UN OBJETO DEL TIPO INTERFAZINICIO

if __name__ == "__main__":
    sesion = {}
    print("\n---Bienvenido---")
    interfazInicial = app.InterfazInicio(sesion)
    interfazInicial._ejecucion()

#OBSERVACIONES:
    # 1 - Se hubiera optado por una interfaz grafica si hubieramos tenido el tiempo para aprenderlo.
    # 2 - Se necesita ampliar el funcionamiento del usuario Preceptor asi como los métodos de la clase para dar
        #una funcionalidad mas completa.
    # 3 - Se podria optar por tener una separacion completa entre las clases de las interfaces y las funciones del programa
    #ya que algunas funciones estan implementada dentro de la misma interfaz, cuando en realidad, deberia tener una funcion propia.
    # 4 - En algunos casos se crearon funciones complejas (por ejemplo: busquedaAsistencias) dado que se pensaba abstraerla para un manejo
    #por tipo de usuario, la idea se logro pero teniendo una funcion poco reutilizable. Se podria pensar como reducirla a funciones
    #mas pequeñas para optimizarla.
    # 5 - En algunos casos, las funcionalidades no estan completas por falta de tiempo para desarrollarlas.
