-- Semana 7 - Consultas SQL sobre el modelo del listado de valores de la Bolsa de Tokio
-- Autora: Zara Melisa Monroy Vera (zara-mon2006)
-- Base: SQLite, creada con 06-week/build_db.py a partir de stock_list_clean.csv
-- Las cifras de dinero están en yenes (la moneda no viene declarada en el archivo).

-- [Q1] WHERE ---------------------------------------------------------------
-- Pregunta: ¿qué cotizaciones tienen una capitalización de al menos 5 billones
-- de yenes (5 x 10^12)? Incluye ETF si los hubiera: aquí solo se filtra.
SELECT codigo_valor, fecha_operacion, cierre, capitalizacion
FROM cotizacion
WHERE capitalizacion >= 5e12
ORDER BY capitalizacion DESC, codigo_valor;

-- [Q2] JOIN ----------------------------------------------------------------
-- Pregunta: ¿cuáles son las 10 acciones de mayor capitalización, con su nombre,
-- sector, serie de tamaño y segmento? (se excluyen ETF y fondos al exigir sector;
-- desempate por código)
SELECT v.codigo_valor,
       v.nombre,
       s33.nombre  AS sector33,
       t.nombre    AS tamano_indice,
       g.nombre    AS segmento,
       ROUND(c.capitalizacion / 1e12, 2) AS capitalizacion_billones_yen
FROM valor AS v
JOIN cotizacion      AS c   ON c.codigo_valor    = v.codigo_valor
JOIN sector33        AS s33 ON s33.sector33_codigo = v.sector33_codigo
JOIN valor_segmento  AS vs  ON vs.codigo_valor   = v.codigo_valor
JOIN segmento_mercado AS g  ON g.segmento_id     = vs.segmento_id
LEFT JOIN tamano_indice AS t ON t.tamano_codigo  = v.tamano_codigo
ORDER BY c.capitalizacion DESC, v.codigo_valor
LIMIT 10;

-- [Q3] GROUP BY ------------------------------------------------------------
-- Pregunta: por sector de 17 grupos, ¿cuántos valores hay, cuántos tienen
-- cotización y cuánta capitalización suman?
SELECT s17.nombre                                   AS sector17,
       COUNT(*)                                     AS valores,
       COUNT(c.codigo_valor)                        AS con_cotizacion,
       ROUND(SUM(c.capitalizacion) / 1e12, 2)       AS capitalizacion_total_billones_yen
FROM valor AS v
JOIN sector33 AS s33 ON s33.sector33_codigo = v.sector33_codigo
JOIN sector17 AS s17 ON s17.sector17_codigo = s33.sector17_codigo
LEFT JOIN cotizacion AS c ON c.codigo_valor = v.codigo_valor
GROUP BY s17.sector17_codigo, s17.nombre
ORDER BY capitalizacion_total_billones_yen DESC, s17.nombre;
