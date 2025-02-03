import random
from datetime import datetime, timedelta

FECHA_INICIO = input("Ingrese fecha inicial (YYYY-MM-DD): ")
FECHA_FIN = input("Ingrese fecha final (YYYY-MM-DD): ")
HORA_INICIO = 7                                 # Rango, para meter ams en el día y menos en la noche igualmente para nuestro analisis, hora militar
HORA_FIN = 19 
INFLAR_CHOFERES = [5, 12, 23, 34, 45]           # Choferes que inflan precios, esto para el anlisis que vamos a hacer
NUM_SERVICIOS = 100                             # Cantidad de servicios a generar

def generar_fecha():
    start_date = datetime.strptime(FECHA_INICIO, "%Y-%m-%d")
    end_date = datetime.strptime(FECHA_FIN, "%Y-%m-%d")
    
    delta = end_date - start_date
    random_day = random.randint(0, delta.days)
    fecha = start_date + timedelta(days=random_day)
    
    hora = random.randint(HORA_INICIO, HORA_FIN)
    minuto = random.randint(0, 59)
    return fecha.replace(hour=hora, minute=minuto, second=0)

def calcular_costo(kilometros, id_chofer):
    base = 10000
    extra_km = 1200
    km_base = 10
    
    if id_chofer in INFLAR_CHOFERES or (random.random() < 0.2 and id_chofer not in INFLAR_CHOFERES):
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
    
    # Kilometraje con decimales (0.5 a 50 km)
    kilometraje = round(random.uniform(0.5, 50), 2)
    
    id_cliente = random.randint(1, 82)                  # Cantidad de clientes que tenemos en nuestra base
    id_chofer = random.choice([
        random.randint(1, 98),                          # Cantidad de choferes que tenemos en nuestra base
        *[random.randint(100, 110) for _ in range(2)] 
    ])
    
    id_coordinador = random.choice([
        random.randint(1, 60),                          # Cantidad de coordinadores que tenemos en nuestra base
        0,  
        None
    ])
    
    costo = calcular_costo(kilometraje, id_chofer)
    
    fecha_sql = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    costo_sql = f"{costo:.2f}"
    kilometraje_sql = f"{kilometraje:.2f}"
    
    inserts.append(
        f"('{fecha_sql}', '{tipo_servicio}', {costo_sql}, {kilometraje_sql}, "
        f"{id_cliente}, {id_chofer}, {id_coordinador if id_coordinador is not None else 'NULL'})"
    )

query = f"""INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
VALUES
{",\n".join(inserts)};"""

print(query)