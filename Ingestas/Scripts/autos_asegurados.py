import random

annio_min = 2010
annio_max = 2024

marcas_autos = {
    'Toyota': ['Corolla', 'Yaris', 'Rush'],
    'Hyundai': ['Elantra', 'Accent', 'i10', 'Grand i10'],
    'Honda': ['Civic', 'Accord', 'H-RV', 'CR-V'],
    'Nissan': ['Sentra', 'Versa', 'March'],
    'Suzuki': ['Alto', 'Vitara', 'Baleno']
}

def generar_placa():
    consonantes = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
    letra1 = random.choice(consonantes)
    letra2 = random.choice(consonantes)
    numeros = f"{random.randint(0, 999):03d}"
    return f"B{letra1}{letra2}{numeros}"

placas_generadas = set()

inserts = []
for id_cliente in range(1, 83):
    while True:
        placa = generar_placa()
        if placa not in placas_generadas:
            placas_generadas.add(placa)
            break
    
    marca = random.choice(list(marcas_autos.keys()))
    modelo = random.choice(marcas_autos[marca])
    annio = random.randint(annio_min, annio_max)
    id_poliza = random.randint(1, 25)
    
    inserts.append(
        f"('{placa}', '{marca}', '{modelo}', {annio}, 'Sedán', {id_cliente}, {id_poliza})"
    )

query = """INSERT INTO Autos_Asegurados (placa_auto, marca_auto, modelo_auto, annio_auto, tipo_auto, id_cliente, id_poliza)
VALUES
""" + ",\n".join(inserts) + ";"

print(query)