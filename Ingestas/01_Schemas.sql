CREATE TABLE Supervisores (
    id_supervisor INT PRIMARY KEY IDENTITY(1,1),
    nombre_supervisor VARCHAR(30),
    apellidos_supervisor VARCHAR(30),
    extension_supervisor INT,
    mail_supervisor VARCHAR(30)
);

CREATE TABLE Coordinadores (
    id_coordinador INT PRIMARY KEY IDENTITY(1,1),
    nombre_coordinador VARCHAR(30),
    apellidos_coordinador VARCHAR(30),
    extension_coordinador INT,
    mail_coordinador VARCHAR(30),
    horario VARCHAR(30),
    id_supervisor INT,
    FOREIGN KEY (id_supervisor) REFERENCES Supervisores(id_supervisor)
);

CREATE TABLE Proveedores (
    id_proveedor INT PRIMARY KEY IDENTITY(1,1),
    nombre_proveedor VARCHAR(50),
    mail_proveedor VARCHAR(50),
    telefono_proveedor INT
);

CREATE TABLE Gruas (
    id_unidad INT PRIMARY KEY IDENTITY(1,1),
    placa_grua VARCHAR(25),
    marca_grua VARCHAR(25),
    modelo_grua VARCHAR(25),
    annio_grua FLOAT,
    tipo_grua VARCHAR(25),
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)  
);

CREATE TABLE Choferes (
    id_chofer INT PRIMARY KEY IDENTITY(1,1),
    nombre_chofer VARCHAR(30),
    apellidos_chofer VARCHAR(30),
    mail_chofer VARCHAR(50),
    telefono_chofer FLOAT,
    id_unidad INT,
    FOREIGN KEY (id_unidad) REFERENCES Gruas(id_unidad)
);

CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY IDENTITY(1,1),
    nombre_cliente VARCHAR(30),
    apellidos_cliente VARCHAR(30),
    mail_cliente VARCHAR(50),
    telefono_cliente INT
);

CREATE TABLE Aseguradoras (
    id_aseguradora INT PRIMARY KEY IDENTITY(1,1),
    nombre_aseguradora VARCHAR(50),
    mail_aseguradora VARCHAR(50),
    telefono_aseguradora INT
);

CREATE TABLE Polizas (
    id_poliza INT PRIMARY KEY IDENTITY(1,1),
    numero_poliza VARCHAR(50) UNIQUE,
    tipo_poliza VARCHAR(25),
    cobertura_danos_tercero BIT,
    cobertura_danos_asegurado BIT,
    cobertura_grua BIT,
    id_aseguradora INT,
    FOREIGN KEY (id_aseguradora) REFERENCES Aseguradoras(id_aseguradora)
);

CREATE TABLE Autos_Asegurados (
    id_auto INT PRIMARY KEY IDENTITY(1,1),
    placa_auto VARCHAR(25) UNIQUE,
    marca_auto VARCHAR(25),
    modelo_auto VARCHAR(25),
    annio_auto INT,
    tipo_auto VARCHAR(25),
    id_cliente INT,
    id_poliza INT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_poliza) REFERENCES Polizas(id_poliza)
);

CREATE TABLE Servicios (
    id_servicio INT PRIMARY KEY IDENTITY(1,1),
    fecha_hora DATETIME,
    tipo_servicio VARCHAR(25),
    costo MONEY,
    kilometraje DECIMAL(10,2),
    id_cliente INT,
    id_chofer INT,
    id_coordinador INT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_chofer) REFERENCES Choferes(id_chofer),
    FOREIGN KEY (id_coordinador) REFERENCES Coordinadores(id_coordinador)
);