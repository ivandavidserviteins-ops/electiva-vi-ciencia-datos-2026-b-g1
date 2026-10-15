# Semana 7 · Consultas SQL y pandas

## ESTUDIANTES: ZARA MELISA MONROY VERA E IVÁN DAVID CARDOZO CHARRY

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 7 · Herramientas y lenguajes (SQL, NoSQL, Python)* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`queries.sql`](queries.sql) | 3 consultas SQL: `WHERE`, `JOIN` y `GROUP BY`, cada una con su pregunta |
| [`queries.py`](queries.py) | Ejecuta las consultas sobre SQLite y reproduce en pandas el `GROUP BY` (y también el `WHERE`) |
| [`resultados.md`](resultados.md) | Salida completa de las tres consultas |

Las consultas se ejecutan sobre el modelo de la [semana 6](../06-week/README.md), con los 4 417 valores del CSV limpio.

```bash
python queries.py    # necesita la carpeta 06-week al lado de esta
```

El script **falla si SQL y pandas no coinciden** (`assert_frame_equal`); con los datos entregados pasa sin diferencias.

## Qué responde cada consulta

> Todo es descriptivo del archivo (una foto con cierres de diciembre de 2021). No son recomendaciones de inversión. Las cifras están en billones (10^12) de yenes; el archivo no declara la moneda.

### Q1 · `WHERE`: cotizaciones de gran capitalización

```sql
SELECT codigo_valor, fecha_operacion, cierre, capitalizacion
FROM cotizacion
WHERE capitalizacion >= 5e12
ORDER BY capitalizacion DESC, codigo_valor;
```

Devuelve **34 cotizaciones** con capitalización de al menos 5 billones de yenes. Como solo mira `cotizacion`, **incluye ETF** (por ejemplo los códigos 1557 y 1306, cuya "capitalización" es el patrimonio del fondo y no el de una empresa). Es la razón de que Q2 y Q3 pasen por `sector33`.

### Q2 · `JOIN`: las 10 acciones de mayor capitalización

```sql
SELECT v.codigo_valor, v.nombre, s33.nombre AS sector33,
       t.nombre AS tamano_indice, g.nombre AS segmento,
       ROUND(c.capitalizacion / 1e12, 2) AS capitalizacion_billones_yen
FROM valor AS v
JOIN cotizacion       AS c   ON c.codigo_valor      = v.codigo_valor
JOIN sector33         AS s33 ON s33.sector33_codigo = v.sector33_codigo
JOIN valor_segmento   AS vs  ON vs.codigo_valor     = v.codigo_valor
JOIN segmento_mercado AS g   ON g.segmento_id       = vs.segmento_id
LEFT JOIN tamano_indice AS t ON t.tamano_codigo     = v.tamano_codigo
ORDER BY c.capitalizacion DESC, v.codigo_valor
LIMIT 10;
```

Une seis tablas para mostrar nombre, sector, serie de tamaño y segmento en lugar de códigos. Encabeza Toyota (código 7203, 34,35 billones), seguida de Sony (6758, 18,25) y Keyence (6861, 17,58). El `JOIN` interno con `sector33` deja fuera ETF y fondos; el `LEFT JOIN` con `tamano_indice` evita perder valores sin serie de tamaño (en el top 10 todos la tienen).

### Q3 · `GROUP BY`: valores y capitalización por sector de 17 grupos

```sql
SELECT s17.nombre AS sector17,
       COUNT(*) AS valores,
       COUNT(c.codigo_valor) AS con_cotizacion,
       ROUND(SUM(c.capitalizacion) / 1e12, 2) AS capitalizacion_total_billones_yen
FROM valor AS v
JOIN sector33 AS s33 ON s33.sector33_codigo = v.sector33_codigo
JOIN sector17 AS s17 ON s17.sector17_codigo = s33.sector17_codigo
LEFT JOIN cotizacion AS c ON c.codigo_valor = v.codigo_valor
GROUP BY s17.sector17_codigo, s17.nombre
ORDER BY capitalizacion_total_billones_yen DESC, s17.nombre;
```

Los dos sectores con más capitalización son *Electric Appliances & Precision Instruments* (152,92) e *IT & Services, Others* (151,75), con 305 y 1 188 valores. Que el segundo sector tenga casi cuatro veces más valores para una capitalización casi igual muestra que **contar valores y sumar capitalización responden preguntas distintas**. `COUNT(*)` cuenta todos los valores del sector y `COUNT(c.codigo_valor)` solo los que tienen cotización; por eso las dos columnas difieren. `SUM` ignora los NULL, es decir, no inventa precios.

## Equivalente en pandas

```python
g = plano.dropna(subset=["sector17_name"]).groupby("sector17_name")
p3 = pd.DataFrame({
    "valores": g.size(),
    "con_cotizacion": g["close"].count(),
    "capitalizacion_total_billones_yen": (g["market_cap"].sum(min_count=1) / 1e12).round(2),
})
```

Es la misma agrupación sobre la tabla plana. `size()` equivale a `COUNT(*)`, `count()` a `COUNT(columna)` (ignora NA) y `sum(min_count=1)` replica que `SUM` de puros NULL da NULL.

## Limitaciones

- La capitalización viene del archivo (cierre × acciones emitidas, comprobado con error relativo < 10^-6); no la recalculé con otra fuente.
- Una sola fecha de cierre por valor: no se pueden hacer comparaciones en el tiempo.
- Q2 y Q3 excluyen ETF y fondos porque ninguno tiene sector en el archivo (verificado: 0 ETF con sector).

## Referencias

CORHUILA. (2026). *Ciencia de Datos · Semana 7 · Herramientas y lenguajes (SQL, NoSQL, Python)* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/07-week/01-session/

Elmasri, R., y Navathe, S. B. (2016). *Fundamentals of database systems* (7.ª ed.). Pearson.

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Comparison with SQL*. https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html

pandas. (s. f.). *Group by: split-apply-combine*. https://pandas.pydata.org/docs/user_guide/groupby.html

Python Software Foundation. (s. f.). *sqlite3 — DB-API 2.0 interface for SQLite databases*. https://docs.python.org/3/library/sqlite3.html

SQLite. (s. f.). *SQL as understood by SQLite*. https://www.sqlite.org/lang.html
