# Resultados de la semana 7

Generado por `queries.py`. Q1 y Q3 se verificaron contra su equivalente en pandas con `assert_frame_equal`. Capitalización en billones (10^12) de yenes; la moneda no viene declarada en el archivo.

## Q1

Filtra con `WHERE` las cotizaciones de gran capitalización. Solo mira la tabla `cotizacion`, por eso no distingue acciones de ETF.

```sql
-- Pregunta: ¿qué cotizaciones tienen una capitalización de al menos 5 billones
-- de yenes (5 x 10^12)? Incluye ETF si los hubiera: aquí solo se filtra.
SELECT codigo_valor, fecha_operacion, cierre, capitalizacion
FROM cotizacion
WHERE capitalizacion >= 5e12
ORDER BY capitalizacion DESC, codigo_valor;
```

Filas devueltas: 34

| codigo_valor | fecha_operacion | cierre | capitalizacion |
|---|---|---|---|
| 1557 | 2021-12-30 | 54920.0 | 52192239810720.0 |
| 7203 | 2021-12-30 | 2105.5 | 34351206097030.0 |
| 6758 | 2021-12-30 | 14475.0 | 18254158779975.0 |
| 6861 | 2021-12-30 | 72280.0 | 17579051399520.0 |
| 1306 | 2021-12-30 | 2073.5 | 16417389210222.0 |
| 6098 | 2021-12-30 | 6972.0 | 11824233329160.0 |
| 9432 | 2021-12-30 | 3150.0 | 11409339866400.0 |
| 8035 | 2021-12-30 | 66280.0 | 10419939181080.0 |
| 9984 | 2021-12-30 | 5434.0 | 9362530568820.0 |
| 4063 | 2021-12-30 | 19920.0 | 8299922836560.0 |
| 8306 | 2021-12-30 | 624.9 | 8299918750488.0 |
| 6594 | 2021-12-30 | 13520.0 | 8061766007360.0 |
| 1321 | 2021-12-30 | 29770.0 | 7965662053050.0 |
| 9433 | 2021-12-30 | 3362.0 | 7746651647100.0 |
| 1308 | 2021-12-30 | 2053.0 | 7671944976758.0 |
| 6367 | 2021-12-30 | 26090.0 | 7647343555570.0 |
| 1305 | 2021-12-30 | 2097.0 | 7621830905625.0 |
| 6902 | 2021-12-30 | 9529.0 | 7508327438079.0 |
| 4661 | 2021-12-30 | 19395.0 | 7053770653200.0 |
| 7974 | 2021-12-30 | 53650.0 | 6967471850000.0 |
| 9434 | 2021-12-30 | 1454.5 | 6962902649765.0 |
| 9983 | 2021-12-30 | 65310.0 | 6927670473360.0 |
| 1326 | 2021-12-30 | 19330.0 | 6489081000000.0 |
| 7741 | 2021-12-30 | 17110.0 | 6325601562200.0 |
| 4519 | 2021-12-30 | 3735.0 | 6271280386245.0 |
| 6981 | 2021-12-30 | 9157.0 | 6188431371117.0 |
| 6501 | 2021-12-30 | 6230.0 | 6032103283710.0 |
| 7267 | 2021-12-30 | 3230.0 | 5850913828900.0 |
| 4568 | 2021-12-30 | 2925.0 | 5695074534825.0 |
| 8001 | 2021-12-30 | 3518.0 | 5575641275072.0 |
| 8058 | 2021-12-30 | 3652.0 | 5425861677852.0 |
| 8316 | 2021-12-30 | 3943.0 | 5419109768186.0 |
| 6273 | 2021-12-30 | 77590.0 | 5227188564810.0 |
| 4689 | 2021-12-30 | 667.4 | 5109835906723.0 |

## Q2

Une 6 tablas con `JOIN` para mostrar nombre, sector, serie de tamaño y segmento en lugar de códigos. Al exigir sector (JOIN interno) se excluyen ETF y fondos; `LEFT JOIN` con `tamano_indice` conserva los valores sin serie de tamaño.

```sql
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
```

Filas devueltas: 10

| codigo_valor | nombre | sector33 | tamano_indice | segmento | capitalizacion_billones_yen |
|---|---|---|---|---|---|
| 7203 | TOYOTA MOTOR CORPORATION | Transportation Equipment | TOPIX Core30 | Prime Market | 34.35 |
| 6758 | SONY GROUP CORPORATION | Electric Appliances | TOPIX Core30 | Prime Market | 18.25 |
| 6861 | KEYENCE CORPORATION | Electric Appliances | TOPIX Core30 | Prime Market | 17.58 |
| 6098 | Recruit Holdings Co.,Ltd. | Services | TOPIX Core30 | Prime Market | 11.82 |
| 9432 | NIPPON TELEGRAPH AND TELEPHONE CORPORATION | Information & Communication | TOPIX Core30 | Prime Market | 11.41 |
| 8035 | Tokyo Electron Limited | Electric Appliances | TOPIX Core30 | Prime Market | 10.42 |
| 9984 | SoftBank Group Corp. | Information & Communication | TOPIX Core30 | Prime Market | 9.36 |
| 4063 | Shin-Etsu Chemical Co.,Ltd. | Chemicals | TOPIX Core30 | Prime Market | 8.3 |
| 8306 | Mitsubishi UFJ Financial Group,Inc. | Banks | TOPIX Core30 | Prime Market | 8.3 |
| 6594 | NIDEC CORPORATION | Electric Appliances | TOPIX Core30 | Prime Market | 8.06 |

## Q3

Agrupa con `GROUP BY` por sector de 17 grupos para ver cuántos valores hay, cuántos tienen cotización y cuánta capitalización suman. Es una descripción del archivo, no una recomendación de inversión.

```sql
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
```

Filas devueltas: 17

| sector17 | valores | con_cotizacion | capitalizacion_total_billones_yen |
|---|---|---|---|
| ELECTRIC APPLIANCES & PRECISION INSTRUMENTS | 305 | 293 | 152.92 |
| IT & SERVICES, OTHERS | 1188 | 1155 | 151.75 |
| AUTOMOBILES & TRANSPORTATION EQUIPMENT | 114 | 108 | 72.97 |
| RAW MATERIALS & CHEMICALS | 294 | 288 | 56.04 |
| RETAIL TRADE | 359 | 339 | 40.0 |
| MACHINERY | 230 | 228 | 38.28 |
| PHARMACEUTICAL | 77 | 73 | 36.51 |
| COMMERCIAL & WHOLESALE TRADE | 320 | 311 | 35.72 |
| BANKS | 93 | 81 | 31.6 |
| CONSTRUCTION & MATERIALS | 316 | 303 | 27.24 |
| TRANSPORTATION & LOGISTICS | 119 | 117 | 26.94 |
| FINANCIALS (EX BANKS) | 97 | 88 | 26.63 |
| FOODS | 137 | 136 | 26.43 |
| REAL ESTATE | 143 | 137 | 14.43 |
| STEEL & NONFERROUS METALS | 80 | 77 | 9.98 |
| ELECTRIC POWER & GAS | 25 | 25 | 7.07 |
| ENERGY RESOURCES | 20 | 17 | 4.4 |
