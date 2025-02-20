import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="base"

    )
    if mydb:
        print("Conexion Exitosa")
        print(connectionBD)
    else:
        print("Error en la conexion.")
        
    return mydb
connectionBD()