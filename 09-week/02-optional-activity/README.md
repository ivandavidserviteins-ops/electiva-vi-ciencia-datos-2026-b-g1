# Semana 9 · Limpieza del listado de valores de la Bolsa de Tokio

## ESTUDIANTES: ZARA MELISA MONROY VERA E IVÁN DAVID CARDOZO CHARRY

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 9 · Transformación y calidad de datos* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`limpieza.py`](limpieza.py) | Script de limpieza en pandas (función `limpiar`) y generador del reporte antes/después |
| [`data/stock_list.csv`](data/stock_list.csv) | Dataset **original** (4 417 filas × 16 columnas) |
| [`data/stock_list_clean.csv`](data/stock_list_clean.csv) | Dataset **limpio** que produce el script (4 417 filas × 16 columnas, nombres en `snake_case`) |
| [`reportes/antes_despues.md`](reportes/antes_despues.md) y [`.json`](reportes/antes_despues.json) | Evidencia antes/después |

```bash
python limpieza.py     # lee data/stock_list.csv y regenera data/ y reportes/
```

**Decisión de diseño:** no imputo ningún precio ni cantidad de acciones. Un precio inventado es peor que un precio ausente, así que los faltantes se dejan como `NA` y se documentan.

## 1. Evidencia antes/después

| Métrica | Antes | Después |
|---|---:|---:|
| Filas | 4 417 | 4 417 |
| Filas duplicadas exactas | 0 | 0 |
| Códigos de valor repetidos | 0 | 0 |
| Celdas faltantes (vacías o con «-») | 8 209 | 8 209 |
| Marcadores distintos para «faltante» | 2 (`""` y `"-"`) | 1 (`NA`) |
| Celdas con espacios sobrantes | 3 776 | 0 |
| Valores distintos en `17SectorName` (antes incluye «-») | 34 | 17 |
| Celdas de sector con caracteres de ancho completo | 97 | 0 |
| Fechas guardadas como decimal (`20211230.0`) | 4 121 | 0 |

Faltantes por columna (iguales antes y después): `new_market_segment` 645 · `sector33_*` y `sector17_*` 500 · `size_*` 2 190 · `trade_date`, `close`, `issued_shares`, `market_cap` 296.

## 2. Problemas encontrados y cómo los traté

| # | Problema | Cómo lo detecté | Tratamiento |
|---|---|---|---|
| 1 | **Dos marcadores de faltante**: celda vacía y «-» | Lectura con `dtype=str, keep_default_na=False` y conteo de cada marcador | Ambos pasan a `NA` real |
| 2 | **Espacios sobrantes** al final de `17SectorName` (3 776 celdas) | Comparar cada celda con su `strip()` | `strip()` y colapso de espacios dobles |
| 3 | **Caracteres de ancho completo** en sectores (`FINANCIALS （EX BANKS）`) | Buscar caracteres no ASCII (97 celdas) | Normalización Unicode NFKC en las columnas de clasificación; **no** en `Name`, que son nombres legales |
| 4 | **Fechas guardadas como decimal** (`20211230.0`) | Inspección de `TradeDate` | Quito el `.0` y convierto a fecha |
| 5 | **Tipos incorrectos**: códigos de sector como decimal por los `NA`, `Universe0` como texto | `dtypes` de la lectura ingenua | Enteros anulables (`Int64`), `float64` para precios, `bool` para `Universe0`; el código de valor se mantiene como **texto** |
| 6 | **Faltantes de precio**: 296 valores sin `Close`, acciones ni capitalización | Conteo de nulos | **No se imputan**; se verifica que los cuatro campos de precio falten juntos |

## 3. Dos dimensiones de calidad que mejoré

Dimensiones de la sesión de clase: completitud, exactitud, consistencia, unicidad y vigencia (Wang y Strong, 1996; ISO/IEC, 2008).

### a) Consistencia: de 34 a 17 etiquetas de sector

Un mismo sector aparecía escrito de varias formas (con y sin espacio final, con paréntesis normales o de ancho completo), por lo que un `groupby('17SectorName')` habría partido un sector en dos grupos. Tras la limpieza hay una sola etiqueta por sector, un solo marcador de faltante y fechas y números con su tipo real.

### b) Completitud: hecha explícita, no mejorada

Las 8 209 celdas faltantes **siguen siendo las mismas**; la limpieza no las rellena. Lo que mejoró es que ahora son `NA` reales y no una mezcla de `""` y `"-"`, de modo que `isna()`, `count()` o un `COUNT(columna)` en SQL las tratan bien. Eso es consistencia sobre el faltante, no completitud: los datos no están más completos.

### Bonus: unicidad y exactitud (verificadas, no corregidas)

El script comprueba con `assert` que el código de valor es único y de 4 o 5 dígitos, que capitalización = cierre × acciones (error relativo < 10^-6), que cada sector de 33 grupos pertenece a un solo sector de 17 y que cada código de clasificación tiene un solo nombre. Pasó todo sin cambios: esas dimensiones ya eran correctas en el archivo.

## 4. Limitaciones

- **Fecha `2000-01-01`:** 286 valores la tienen como fecha efectiva, todos sin precio. Parece un valor por defecto; no la corregí porque no hay fuente para saber la real.
- **`Universe0`:** su significado no está documentado (2 000 valores lo tienen en verdadero). Lo guardé tal cual.
- **Moneda:** no viene declarada; se asume yenes.
- **ETF y fondos** viven en el mismo archivo que las acciones (no tienen sector); hay que filtrarlos en análisis de capitalización de empresas.
- Los 296 valores sin precio no tienen cotización en el modelo de la semana 6.

## 5. Referencias

CORHUILA. (2026). *Ciencia de Datos · Semana 9 · Transformación y calidad de datos* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/09-week/01-session/

International Organization for Standardization & International Electrotechnical Commission. (2008). *ISO/IEC 25012:2008 Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*.

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Working with missing data*. https://pandas.pydata.org/docs/user_guide/missing_data.html

Python Software Foundation. (s. f.). *unicodedata — Unicode Database*. https://docs.python.org/3/library/unicodedata.html

Rahm, E., y Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.

Unicode Consortium. (s. f.). *UAX #15: Unicode normalization forms*. https://unicode.org/reports/tr15/

Wang, R. Y., y Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33.

Wickham, H. (2014). Tidy data. *Journal of Statistical Software, 59*(10), 1–23.
