/*
	Estas consultas son una serie de ideas que pueden ser aplicadas 
	al caso de estudio, pero sientase en la confiranza de realzar
	los análisis que desee y modificar las ingestas de servicios a gusto.
	
	Se recomienda si se desea usar consultas ejecutar hasta que ya el proyecto esté 
	completamente creado
*/

-- Analicemos cuanto nos cueta el kilometro por fecha

-- Interrogante ¿Cuáles son los costos operativos reales?
-- ¿Existe alguna inconsistencia o son planos?
-- ¿Se están respetando los contratos que el cliente nos indicó?
-- Interrogante ¿Cuáles son los costos operativos reales?
-- ¿Existe alguna inconsistencia o son planos?
-- ¿Se están respetando los contratos que el cliente nos indicó?

-- Detectamos una incosistencia en el último mes
SELECT 
    CONVERT(DATE, fecha_hora) AS Fecha,
    SUM(Costo -10000) / SUM(kilometraje - 10) AS Costo_Kilometro,
    COUNT(id_servicio) AS Cantidad_Servicios
FROM Servicios
WHERE kilometraje > 10
AND Costo > 10000
GROUP BY CONVERT(DATE, fecha_hora)
ORDER BY Fecha;


-- Averiguar el origen de la inconsistencia
-- La inconsitencia no es general, es focalizada
SELECT
	Choferes.id_chofer,
    CONCAT(Choferes.nombre_chofer,' ',Choferes.apellidos_chofer) AS Chofer,
    SUM(Servicios.Costo - 10000) / SUM(Servicios.kilometraje - 10) AS Costo_Kilometro
FROM Servicios
INNER JOIN Choferes ON Servicios.id_chofer = Choferes.id_chofer
WHERE (Servicios.kilometraje > 10 AND Servicios.Costo > 10000) OR (Servicios.kilometraje < 10 AND Servicios.Costo > 10000)
GROUP BY
	Choferes.id_chofer,
	CONCAT(Choferes.nombre_chofer,' ',Choferes.apellidos_chofer)
HAVING SUM(Servicios.Costo - 10000) / SUM(Servicios.kilometraje - 10) > 1200
ORDER BY Choferes.id_chofer DESC;



-- Id coon sobreprecio 45, 34, 23, 12 5
-- Sabemos que este sobreprecio inicio desde el 2025-02-01

-- Surge la siguiente interrogante, ¿Cuánto hemos pagado de sobreprecio?
WITH 
	basicos AS (
		SELECT
			DATEPART(MONTH, fecha_hora) AS mes,
			SUM(costo) AS total_facturado,
			COUNT(id_servicio) AS cantidad,
			SUM(costo) - (COUNT(id_servicio) * 10000) AS perdida_cortos
		FROM Servicios
		WHERE id_chofer IN (45, 34, 23, 12, 5)
		AND CAST(fecha_hora AS DATE) >= '2025-02-01'
		AND kilometraje < 10
		GROUP BY DATEPART(MONTH, fecha_hora)
	),  
	largos AS (
		SELECT
			DATEPART(MONTH, fecha_hora) AS mes,
			SUM(costo) AS total_facturado,
			COUNT(id_servicio) AS cantidad,
			(SUM(costo - 10000) - SUM((kilometraje - 10) * 1200)) AS perdida_largos,
			SUM(kilometraje - 10) AS total_km_adicionales_recorridos
		FROM Servicios
		WHERE id_chofer IN (45, 34, 23, 12, 5)
		AND CAST(fecha_hora AS DATE) >= '2025-02-01'
		AND kilometraje > 10
		GROUP BY DATEPART(MONTH, fecha_hora)
	),
	total AS(
		SELECT
			DATEPART(MONTH, fecha_hora) AS mes,
			SUM(costo) AS total_facturado
		FROM Servicios
		WHERE CAST(fecha_hora AS DATE) >= '2025-02-01'
		GROUP BY DATEPART(MONTH, fecha_hora)
	)
SELECT 
	basicos.mes,
	(basicos.perdida_cortos + largos.perdida_largos) AS total_perdida,
	total.total_facturado,
	((basicos.perdida_cortos + largos.perdida_largos) / total.total_facturado) * 100 AS porcentaje_variacion_negativa
FROM basicos
INNER JOIN largos ON basicos.mes = largos.mes
INNER JOIN total ON total.mes = largos.mes
ORDER BY basicos.mes;


-- Verificar seguimiento de procesos
-- ¿Se han brindado servicios no amparados?
SELECT * 
FROM Servicios 
WHERE NOT EXISTS (
    SELECT * 
    FROM Polizas 
    INNER JOIN Autos_Asegurados ON Autos_Asegurados.id_poliza = Polizas.id_poliza
    INNER JOIN Clientes ON Clientes.id_cliente = Autos_Asegurados.id_cliente
    WHERE Polizas.cobertura_grua = 1 
    AND Clientes.id_cliente = Servicios.id_cliente
);

-- Total de servicio				81,920
-- Total de servicio no amparados	58,621


-- Trigger que devuelve un error para pólizas invalidas
/*
	Ojo, cuando ejecute este trigger no se garantiza el funcionamiento
	de la ingesta servicio_v#.py, ya que aquí limitamos
	que solo autos asegurados con servicio de grua activo puedan recibir el servicio
*/
INSTEAD OF INSERT
AS
BEGIN
    IF NOT EXISTS (
        SELECT *
        FROM inserted
        INNER JOIN Polizas ON Polizas.id_poliza = (
            SELECT TOP 1 Autos_Asegurados.id_poliza
            FROM Autos_Asegurados
            WHERE Autos_Asegurados.id_cliente = inserted.id_cliente
        )
        WHERE Polizas.cobertura_grua = 1	-- Valida si la poliza no tiene cobertua
    )
	-- Si es verdadfero rechase la inserción
    BEGIN
        PRINT ('La póliza no cuenta con servicio de grua');
        ROLLBACK TRANSACTION;
    END
	-- Si es falso entonces adelante con la inserción
    ELSE
    BEGIN
		INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
        SELECT fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador
        FROM inserted;
    END
END;

-- Para averiguar clientes con pólizas amparadas
SELECT * FROM Clientes
INNER JOIN Autos_Asegurados ON Autos_Asegurados.id_cliente = Clientes.id_cliente
INNER JOIN Polizas ON Autos_Asegurados.id_poliza = Polizas.id_poliza
WHERE Polizas.cobertura_grua = 1
ORDER BY Clientes.id_cliente

-- Realizar una inserción fallida
INSERT INTO Servicios (fecha_hora, tipo_servicio, costo, kilometraje, id_cliente, id_chofer, id_coordinador)
VALUES ('2025-01-01 13:43:00.000', 'Plataforma', 16384.00, 15.32, 1, 3, 59);


-- Esta vista clasifica los horarios por turnos, nos puede ser útil para detectar si existe sobre Staff
CREATE VIEW segmentacion_horario AS (
	SELECT 
		Servicios.id_servicio,
		CONCAT(Coordinadores.nombre_coordinador,' ', Coordinadores.apellidos_coordinador) AS nombre_coordinador,
		Servicios.kilometraje,
		Servicios.costo,
		Servicios.fecha_hora,
		CASE 
			WHEN CAST(Servicios.fecha_hora AS TIME) BETWEEN '06:00:00' AND '14:59:59' THEN 'Mañana'
			WHEN CAST(Servicios.fecha_hora AS TIME) BETWEEN '13:00:00' AND '21:59:59' THEN 'Tarde'
			ELSE 'Noche'
		END AS horario,
		CONVERT(DATE, fecha_hora) AS fecha
	FROM Servicios
	INNER JOIN Coordinadores ON Servicios.id_coordinador = Coordinadores.id_coordinador);

-- A partir de un día con cantidad de servicios altos sacamos cuanto es la cantidad 
-- De servicios promedio que debe coordinar un agente
SELECT 
	COUNT(id_servicio) / 60 AS promedio_por_coordinador -- 20 Coordinadores por turno (3 turnos)
FROM segmentacion_horario
WHERE CONVERT(DATE, fecha_hora) = '2025-02-10'
-- Pero, veamos el comportamiento entre distintos turnos
AND horario = 'Mañana'
AND horario = 'Tarde'
AND horario = 'Noche'


-- Calculos para ver el rendimiento operativo y verificar si existe o no sobre staff
SELECT
	horario,
	COUNT(id_servicio) / 20 AS promedio_por_coordinador -- 20 Coordinadores por turno (3 turnos)
FROM segmentacion_horario
WHERE CONVERT(DATE, fecha_hora) = '2025-02-10'
GROUP BY horario;


-- 32 Servicios en un día de alto volumen por coordinador

-- 54 Servicios promedio en el turno de mañana en 8 horas ingresa 
-- 36 Servicios promedio en el turno de la tarde
-- 07 Servicios promedio en el turno de nocturno

SELECT
	horario,
	CASE 
	 WHEN horario = 'Mañana' THEN COUNT(id_servicio)/8
	 WHEN horario = 'Tarde' THEN COUNT(id_servicio)/7
	 ELSE COUNT(id_servicio)/8
	END AS promedio_hora
FROM segmentacion_horario
WHERE CONVERT(DATE, fecha_hora) = '2025-02-10'
GROUP BY horario;

SELECT
	COUNT(id_servicio) AS promedio_hora
FROM segmentacion_horario
WHERE CONVERT(DATE, fecha_hora) = '2025-02-10'
AND horario = 'Noche';
