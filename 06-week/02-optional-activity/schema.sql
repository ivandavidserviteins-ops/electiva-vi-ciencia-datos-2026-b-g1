-- Semana 6 - Modelo relacional del listado de valores de la Bolsa de Tokio
-- Autora: Zara Melisa Monroy Vera (zara-mon2006)
-- Motor: SQLite 3 (las llaves foráneas se activan con PRAGMA foreign_keys = ON)

PRAGMA foreign_keys = ON;

-- Catálogos (cada nombre se guarda una sola vez) --------------------------------

-- Clasificación sectorial de 17 grupos
CREATE TABLE sector17 (
    sector17_codigo  INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL UNIQUE
);

-- Clasificación sectorial de 33 grupos; cada una pertenece a un único sector de 17
CREATE TABLE sector33 (
    sector33_codigo  INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL UNIQUE,
    sector17_codigo  INTEGER NOT NULL REFERENCES sector17(sector17_codigo)
);

-- Serie de tamaño del índice TOPIX (Core30, Large70, Mid400, Small 1, Small 2)
CREATE TABLE tamano_indice (
    tamano_codigo    INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL UNIQUE
);

-- Clasificación antigua del mercado ("Section/Products"): First Section, ETFs, etc.
CREATE TABLE seccion_producto (
    seccion_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT NOT NULL UNIQUE
);

-- Segmentos nuevos del mercado: Prime, Standard, Growth (y variantes de acciones extranjeras)
CREATE TABLE segmento_mercado (
    segmento_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT NOT NULL UNIQUE
);

-- Entidad principal: un valor listado (acción, ETF, REIT...). La llave es el CÓDIGO,
-- no el nombre: hay 5 nombres repetidos que son empresas distintas.
CREATE TABLE valor (
    codigo_valor     TEXT PRIMARY KEY CHECK (length(codigo_valor) BETWEEN 4 AND 5),
    nombre           TEXT NOT NULL,
    universe0        INTEGER NOT NULL CHECK (universe0 IN (0, 1)),
    fecha_efectiva   TEXT NOT NULL,                       -- ISO aaaa-mm-dd
    seccion_id       INTEGER NOT NULL REFERENCES seccion_producto(seccion_id),
    sector33_codigo  INTEGER REFERENCES sector33(sector33_codigo),     -- NULL: ETF, fondos...
    tamano_codigo    INTEGER REFERENCES tamano_indice(tamano_codigo)   -- NULL: fuera de la serie TOPIX
);

-- Un valor tiene muchas cotizaciones (una por fecha de operación)
CREATE TABLE cotizacion (
    codigo_valor      TEXT NOT NULL REFERENCES valor(codigo_valor),
    fecha_operacion   TEXT NOT NULL,
    cierre            REAL NOT NULL CHECK (cierre > 0),
    acciones_emitidas REAL NOT NULL CHECK (acciones_emitidas > 0),
    capitalizacion    REAL NOT NULL CHECK (capitalizacion > 0),
    PRIMARY KEY (codigo_valor, fecha_operacion)
);

-- N:M valor <-> segmento de mercado. Un segmento agrupa muchos valores y, con las
-- reclasificaciones, un valor puede pasar por más de un segmento a lo largo del tiempo.
CREATE TABLE valor_segmento (
    codigo_valor  TEXT    NOT NULL REFERENCES valor(codigo_valor),
    segmento_id   INTEGER NOT NULL REFERENCES segmento_mercado(segmento_id),
    PRIMARY KEY (codigo_valor, segmento_id)
);

CREATE INDEX idx_valor_sector33 ON valor(sector33_codigo);
CREATE INDEX idx_cotizacion_cap ON cotizacion(capitalizacion);
