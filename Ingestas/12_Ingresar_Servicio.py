## Con este código puede emular un sistema que ingresa registros como si fuese un coordinador

import pyodbc
from datetime import datetime

server = r'Servidor_Aquí'           ## Para que funcione coloque el servidor de su base de datos aquí
database = 'Towing_Company'         ## Y aquí la base de datos
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

def solicitar_datos():
    tipo_servicio = input("Tipo de servicio: ")
    costo = float(input("Costo del servicio: "))
    kilometraje = float(input("Kilometraje: "))
    id_cliente = int(input("ID del cliente: "))
    id_chofer = int(input("ID del chofer: "))
    id_coordinador = int(input("ID del coordinador: "))

    return tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador

def insertar_servicio(tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador):
    try:
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, fecha_hora_actual, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
        conn.commit()
        print("Servicio insertado correctamente.")
    except:
        print("Verifique la pólzia antes de continuar")

def main():
    while True:
        print("1. Insertar un nuevo servicio")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador = solicitar_datos()

            insertar_servicio(tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()

cursor.close()
conn.close()