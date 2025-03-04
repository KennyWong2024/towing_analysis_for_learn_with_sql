## Se recomienda usar version 3

## Esta versión genera el INSERT por consola copiar y pegar la query
import random
from datetime import datetime, timedelta

FECHA_INICIO = input("Ingrese fecha inicial (YYYY-MM-DD): ")
FECHA_FIN = input("Ingrese fecha final (YYYY-MM-DD): ")
HORA_INICIO = 6  
HORA_FIN = 22 
INFLAR_CHOFERES = []               ## Choferes que inflan precios 5, 12, 23, 34, 45
NUM_SERVICIOS = 100                ## Cantidad de servicios a generar

# Horarios con mayor incidencia
HORAS_PICO = [8, 9, 11, 12, 13, 17, 18, 19]

def generar_fecha():
    start_date = datetime.strptime(FECHA_INICIO, "%Y-%m-%d")
    end_date = datetime.strptime(FECHA_FIN, "%Y-%m-%d")

    delta = end_date - start_date
    random_day = random.randint(0, delta.days)
    fecha = start_date + timedelta(days=random_day)

    ## Aumento de probabilidad en horas pico
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

    if kilometros <= km_base:
        return base
    else:
        return base + (kilometros - km_base) * extra_km

inserts = []
for _ in range(NUM_SERVICIOS):
    fecha_hora = generar_fecha()
    tipo_servicio = 'Plataforma'

    kilometraje = round(random.uniform(0.5, 50), 2)

    id_cliente = random.randint(1, 82)                  ## Cantidad de clientes, no tocar

    id_chofer = random.choice([
        random.randint(1, 98),
        *[random.randint(1, 98) for _ in range(2)]
    ])

    id_coordinador = random.randint(1, 40)              ## Solo coordinadores diurnos

    costo = calcular_costo(kilometraje, id_chofer)

    fecha_sql = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    costo_sql = f"{costo:.2f}"
    kilometraje_sql = f"{kilometraje:.2f}"

    inserts.append(
        f"('{fecha_sql}', '{tipo_servicio}', {costo_sql}, {kilometraje_sql}, "
        f"{id_cliente}, {id_chofer}, {id_coordinador})"
    )

## Generador de ingesta por consola
query = f"""INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
VALUES
{",\n".join(inserts)};"""

print(query)