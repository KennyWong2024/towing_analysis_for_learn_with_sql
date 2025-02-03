import random
from collections import defaultdict

# Preventivo, por si usamos acentos en los nombres yu apellidos
def remove_accents(input_str):
    accents = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
    }
    for acc, no_acc in accents.items():
        input_str = input_str.replace(acc, no_acc)
    return input_str

# Definir que nombres y apellidos vamos a usar para el randomizador
nombres = ['Juan Carlos', 'Edgar', 'Allan', 'Esther', 'Judith', 'Pedro', 'José', 'Miguel', 
          'Ana María', 'Fernando', 'Sofia', 'Luisa', 'Susan', 'Kenny', 'Gabriel', 'Ricardo',
          'Andres', 'Dagoberto', 'Raul', 'Diego', 'Daniel', 'Freedy', 'Jimmy', 'Rodrigo',
          'Jorge', 'Francisco', 'Pablo', 'Alberto', 'Ramon', 'Hector', 'Misael', 'Ronald',
          'Shirley', 'Warren', 'Wagner', 'Bladimir', 'Raanvalen', 'Dilan', 'Kevin', 'Kenneth',
          'Kendall', 'Walter', 'Ángel', 'Sergio', 'Weyner', 'Frank', 'Alberto', 'Johnny',
          'Bryan', 'Erving', 'Gary', 'Gustavo', 'Johel', 'Lucas', 'Yener', 'Zahit',
          'John', 'Keylor', 'Brandon', 'Josué', 'Mateo', 'Marcos', 'Jesus', 'Leonardo',
          'Fabian', 'Emilio', 'Javier', 'Nelson', 'Cesar', 'Caleb', 'Nicolas', 'Pedro',
          'Peter', 'Rafael', 'Darío', 'Alexander', 'Giancarlo', 'Adolfo', 'Romel', 'Ronny']

apellidos = ['Gomez', 'Rodriguez', 'Gonzalez', 'Fernandez', 'Lopez', 'Ramos','Chacón',
            'Martinez', 'Pérez', 'Sanchez', 'Ramirez', 'Torres', 'Briceño', 'Salas', 
            'Diaz', 'Hernández', 'Morales', 'Rojas', 'Vargas', 'Juarez', 'Leitón',
            'Castro', 'Romero', 'Alvarado', 'Mendoza', 'Guerrero', 'Madrigal', 'Molina',
            'Castillo', 'Arias', 'Cepeda', 'Vindas', 'Chinchilla', 'Fuentes', 'Contreras',
            'Figueroa', 'Tenorio', 'Cordero', 'Cortés', 'Cruz', 'Aguilar', 'Delgado',
            'Rivera', 'Orozco', 'Nieves', 'Dominguez', 'Duarte', 'Sequeira', 'Espinoza',
            'Hidalgo', 'Esquivel', 'Fallas', 'Montoya', 'Monge', 'Peña', 'Bonilla',
            'Cedeño', 'Flores', 'León', 'Reyes', 'Bustos', 'Nájera', 'Mora']

# Esto es con base a nuestro 25 proveedores ya creados donde
# id_proveedor (Unicamente usado como llave), 
# telefono_proveedor (Extraer la estructura para generar el de sus choferes), 
# email_proveedor (Extraer el dominio para generar el de sus choferes)
proveedores = [
    (1, 88010000, 'gruastibas.cr'),
    (2, 88020000, 'gruascurridabat.cr'),
    (3, 88030000, 'gruasescazu.cr'),
    (4, 88040000, 'gruasdesamparados.cr'),
    (5, 88050000, 'gruascentral.cr'),
    (6, 88060000, 'gruasheredia.cr'),
    (7, 88070000, 'gruassarapiqqui.cr'),
    (8, 88080000, 'gruasalajuela.cr'),
    (9, 88090000, 'gruasatenas.cr'),
    (10, 88100000, 'gruasoccidente.cr'),
    (11, 88110000, 'gruasdelnorte.cr'),
    (12, 88120000, 'gruaspuntarenas.cr'),
    (13, 88130000, 'gruasgarabito.cr'),
    (14, 88140000, 'gruasquepos.cr'),
    (15, 88150000, 'gruascorredores.cr'),
    (16, 88160000, 'gruasliberia.cr'),
    (17, 88170000, 'gruassantacruz.cr'),
    (18, 88180000, 'gruascobano.cr'),
    (19, 88190000, 'gruascartago.cr'),
    (20, 88200000, 'gruasturrialba.cr'),
    (21, 88210000, 'gruasperezzeledon.cr'),
    (22, 88220000, 'gruaspococi.cr'),
    (23, 88230000, 'gruassiquirres.cr'),
    (24, 88240000, 'gruaslimon.cr'),
    (25, 88250000, 'gruastalamanca.cr')
]

contador_proveedores = defaultdict(int)

# Asiganción aleatroia de gruas
# Aquí previamente ya definimos cuantas gruas iba a tener cada proveedor
inserts_choferes = []
for id_unidad in range(1, 99):
    id_proveedor = 0
    if id_unidad <= 3: id_proveedor = 1
    elif id_unidad <= 7: id_proveedor = 2
    elif id_unidad <= 12: id_proveedor = 3
    elif id_unidad <= 19: id_proveedor = 4
    elif id_unidad <= 28: id_proveedor = 5
    elif id_unidad <= 36: id_proveedor = 6
    elif id_unidad == 37: id_proveedor = 7
    elif id_unidad <= 44: id_proveedor = 8
    elif id_unidad <= 46: id_proveedor = 9
    elif id_unidad <= 51: id_proveedor = 10
    elif id_unidad <= 53: id_proveedor = 11
    elif id_unidad <= 55: id_proveedor = 12
    elif id_unidad <= 59: id_proveedor = 13
    elif id_unidad <= 61: id_proveedor = 14
    elif id_unidad <= 63: id_proveedor = 15
    elif id_unidad <= 68: id_proveedor = 16
    elif id_unidad <= 71: id_proveedor = 17
    elif id_unidad == 72: id_proveedor = 18
    elif id_unidad <= 77: id_proveedor = 19
    elif id_unidad <= 79: id_proveedor = 20
    elif id_unidad <= 83: id_proveedor = 21
    elif id_unidad <= 88: id_proveedor = 22
    elif id_unidad <= 90: id_proveedor = 23
    elif id_unidad <= 93: id_proveedor = 24
    elif id_unidad <= 98: id_proveedor = 25

    for p in proveedores:
        if p[0] == id_proveedor:
            telefono_base = p[1]
            dominio = p[2]
            break

    # Generar número de teléfono
    # Como la estructura es 8801 (01 el proveedor) y queremos que sus respectivos choferes tengan numeros semejantes
    # Entonces simplemente sumamos 1 a la estructura general especifica al proveedor apuntado, para que sea 88010001
    contador_proveedores[id_proveedor] += 1
    telefono = telefono_base + contador_proveedores[id_proveedor]

    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    
    inicial = nombre[0].lower()
    apellido_limpio = remove_accents(apellido.replace(' ', '').lower())
    email = f"{inicial}{apellido_limpio}@{dominio}"
    
    insert = f"('{nombre}', '{apellido}', '{email}', {telefono}, {id_unidad})"
    inserts_choferes.append(insert)

# Aquí es el generador del Query, esto nos devuelve la salida en la consola con la estructura pensada para SQL Server
print("INSERT INTO Choferes (nombre_chofer, apellidos_chofer, mail_chofer, telefono_chofer, id_unidad) VALUES")
print(",\n".join(inserts_choferes) + ";")