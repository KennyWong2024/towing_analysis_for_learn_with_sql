## Esta es la versión 3
## Realiza la ingesta directamente a la base de datos

import random
from datetime import datetime, timedelta
import pyodbc

# Ejecutar pip install pyodbc
server = r'Colocar_Servidor_Aquí'                   # Servidor
database = 'Colocar_Database_Aquí'                  # Base de datos
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Conectar a la base de datos
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

FECHA_INICIO = input("Ingrese fecha inicial (YYYY-MM-DD): ")
FECHA_FIN = input("Ingrese fecha final (YYYY-MM-DD): ")
NUM_SERVICIOS = int(input("Ingrese la cantidad de servicios a generar: "))

HORA_INICIO = 0                         # 0 nocturno, 6 inicio diurno
HORA_FIN = 5                           # 5 nocturno, 23 fin diuno
INFLAR_CHOFERES = [5, 12, 23, 34, 45]   # Choferes que inflan precios 5, 12, 23, 34, 45

# Horarios con mayor incidencia
HORAS_PICO = [2] ## Diurnas 8, 9, 11, 12, 13, 17, 18, 19 | Nocturnas 22, 2, 5, 6

def generar_fecha():
    start_date = datetime.strptime(FECHA_INICIO, "%Y-%m-%d")
    end_date = datetime.strptime(FECHA_FIN, "%Y-%m-%d")

    delta = end_date - start_date
    random_day = random.randint(0, delta.days)
    fecha = start_date + timedelta(days=random_day)

    if random.random() < 0.6: 
        hora = random.choice(HORAS_PICO)
    else:
        hora = random.randint(HORA_INICIO, HORA_FIN)

    minuto = random.randint(0, 59)
    return fecha.replace(hour=hora, minute=minuto, second=0)

def calcular_costo(kilometros, id_chofer):
    base = 10000
    extra_km = 1200
    km_base = 10

    if id_chofer in INFLAR_CHOFERES:
        base = 20000
        extra_km = 2000

    return base if kilometros <= km_base else base + (kilometros - km_base) * extra_km

# Generar datos y realizar la ingesta directa
for _ in range(NUM_SERVICIOS):
    fecha_hora = generar_fecha()
    tipo_servicio = 'Plataforma'
    kilometraje = round(random.uniform(0.5, 50), 2)
    id_cliente = random.randint(1, 82)
    id_chofer = random.randint(1, 98)
    id_coordinador = random.randint(41, 60)

    costo = calcular_costo(kilometraje, id_chofer)
    
    fecha_sql = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    
    # Insertar directamente en la base de datos
    cursor.execute("""
        INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, fecha_sql, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print(f"{NUM_SERVICIOS} servicios insertados correctamente en la base de datos.")