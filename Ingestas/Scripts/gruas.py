import random

marcas = ["Isuzu", "Hino", "Nissan", "Volvo"]
modelos = {  # Estas marcas se eligieron con base a los modelos observados en distintas páginas de Facebook de grúas
    "Isuzu": ["NQR"],
    "Hino": ["300"],
    "Nissan": ["UD"],
    "Volvo": ["FMX", "FH16"]
}
proveedores = [  # Integramente ligado a nuestra base de datos, decimos cuántas grúas queremos para cada proveedor
    (1, 3), (2, 4), (3, 5), (4, 7), (5, 9), (6, 9), (7, 1), (8, 8), (9, 2), (10, 5),
    (11, 3), (12, 3), (13, 4), (14, 2), (15, 2), (16, 5), (17, 3), (18, 1), (19, 5),
    (20, 2), (21, 4), (22, 5), (23, 2), (24, 3), (25, 1)
]

def generar_placa():
    return f"CL13{random.randint(1000, 9999)}"  # Esto limita a que respete la estructura de placas de Costa Rica que inicien con CL

def generar_grua(id_proveedor):
    marca = random.choices(marcas, weights=[35, 35, 25, 10], k=1)[0]
    modelo = random.choice(modelos[marca])
    annio = random.randint(2010, 2019) if marca != "Volvo" else random.randint(1980, 1997)
    return {
        "placa": generar_placa(),
        "marca": marca,
        "modelo": modelo,
        "annio": annio,
        "tipo": "Plataforma",
        "id_proveedor": id_proveedor
    }

inserts = []
for id_proveedor, cantidad in proveedores:
    for _ in range(cantidad):
        grua = generar_grua(id_proveedor)
        inserts.append(
            f"('{grua['placa']}', '{grua['marca']}', '{grua['modelo']}', {grua['annio']}, "
            f"'{grua['tipo']}', {grua['id_proveedor']})"
        )

# Aquí es el generador del Query, esto nos devuelve la salida en la consola con la estructura pensada para SQL Server
query = "INSERT INTO Gruas (placa_grua, marca_grua, modelo_grua, annio_grua, tipo_grua, id_proveedor) VALUES\n"
query += ",\n".join(inserts) + ";"

print(query)