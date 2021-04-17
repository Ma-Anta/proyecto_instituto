import os
#import urllib.parse as up
import psycopg2

#up.uses_netloc.append("postgres")
class Database():
    
    def __init__(self,p_database,p_user,p_password,p_host,p_port):
        self.cursor=self.connection(p_database,p_user,p_password,p_host,p_port)
    
    def connection(self,p_database,p_user,p_password,p_host,p_port):
        conn = psycopg2.connect(database=p_database,
            user=p_user,
            password=p_password,
            host=p_host,
            port=p_port
            )
        self.connect = conn
        cursor = conn.cursor()
        return cursor
    
    def ejecutar(self,consulta):
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        return resultado

    def close_connection(self):
        self.cursor.close()

    def procedimiento(self,procedimiento,parametros):
        self.cursor.callproc(procedimiento,parametros)
        resultado = self.cursor.fetchall()
        return resultado


bbdd = Database("kezqosou","kezqosou","ufCrLcrXhiS2xBPfQGEsw-czRYilMDM9","queenie.db.elephantsql.com",5432)