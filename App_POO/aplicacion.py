# pylint: disable=import-error
import interfaz.interfaz as app

if __name__ == "__main__":
    sesion = {}
    print("\n---Bienvenido---")
    interfazInicial = app.InterfazInicio(sesion)
    interfazInicial._ejecucion()
