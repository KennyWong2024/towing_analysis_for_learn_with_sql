import random
import csv

marcas = ["Isuzu", "Hino", "Nissan", "Volvo"]
modelos = {
    "Isuzu": ["NQR"],
    "Hino": ["300"],
    "Nissan": ["UD"],
    "Volvo": ["FMX", "FH16"]
}
proveedores = [
    (1, 3), (2, 4), (3, 5), (4, 7), (5, 9), (6, 9), (7, 1), (8, 8), (9, 2), (10, 5),
    (11, 3), (12, 3), (13, 4), (14, 2), (15, 2), (16, 5), (17, 3), (18, 1), (19, 5),
    (20, 2), (21, 4), (22, 5), (23, 2), (24, 3), (25, 1)
]

def generar_placa():
    return f"CL13{random.randint(1000, 9999)}"

def generar_grua(id_proveedor):
    marca = random.choices(marcas, weights=[35, 35, 25, 10], k=1)[0]
    modelo = random.choice(modelos[marca])
    annio = random.randint(2010, 2019) if marca != "Volvo" else random.randint(1980, 1997)
    return {
        "placa_grua": generar_placa(),
        "marca_grua": marca,
        "modelo_grua": modelo,
        "annio_grua": annio,
        "tipo_grua": "Plataforma",
        "id_proveedor": id_proveedor
    }

gruas = []

for id_proveedor, cantidad in proveedores:
    for _ in range(cantidad):
        grua = generar_grua(id_proveedor)
        gruas.append(grua)

with open('gruas.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["placa", "marca", "modelo", "annio", "tipo", "id_proveedor"])
    
    writer.writeheader()
    
    for grua in gruas:
        writer.writerow(grua)

print("Los datos han sido escritos en el archivo 'gruas.csv'")