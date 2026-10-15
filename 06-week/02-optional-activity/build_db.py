"""Semana 6 - Carga el CSV limpio en el modelo relacional normalizado (SQLite).

Autora: Zara Melisa Monroy Vera (zara-mon2006)

Uso:
    python build_db.py                 # crea stock.db junto a este archivo

Otras semanas importan `construir_db` para reutilizar el mismo modelo.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
TABLAS = ["sector17", "sector33", "tamano_indice", "seccion_producto",
          "segmento_mercado", "valor", "cotizacion", "valor_segmento"]


def leer_limpio(csv: Path) -> pd.DataFrame:
    # El código se lee como texto (un código con ceros a la izquierda se rompería como número)
    return pd.read_csv(csv, dtype={"securities_code": str})


def construir_db(csv_limpio: Path, db_path: Path | None = None) -> sqlite3.Connection:
    """Crea la base (en archivo, o en memoria si db_path es None) y la llena."""
    df = leer_limpio(csv_limpio)

    # Comprobaciones de normalización: cada código determina un solo nombre
    s17 = df[["sector17_code", "sector17_name"]].dropna().drop_duplicates()
    s33 = df[["sector33_code", "sector33_name", "sector17_code"]].dropna().drop_duplicates()
    tam = df[["size_code", "size_name"]].dropna().drop_duplicates()
    assert s17["sector17_code"].is_unique and s33["sector33_code"].is_unique
    assert tam["size_code"].is_unique

    if db_path is not None and Path(db_path).exists():
        Path(db_path).unlink()
    con = sqlite3.connect(":memory:" if db_path is None else str(db_path))
    con.executescript((AQUI / "schema.sql").read_text(encoding="utf-8"))

    def enteros(filas):
        return [tuple(int(v) if isinstance(v, float) and v == int(v) else v for v in f)
                for f in filas]

    con.executemany("INSERT INTO sector17 VALUES (?,?)", enteros(s17.itertuples(index=False, name=None)))
    con.executemany("INSERT INTO sector33 VALUES (?,?,?)", enteros(s33.itertuples(index=False, name=None)))
    con.executemany("INSERT INTO tamano_indice VALUES (?,?)", enteros(tam.itertuples(index=False, name=None)))
    con.executemany("INSERT INTO seccion_producto(nombre) VALUES (?)",
                    [(n,) for n in sorted(df["section_products"].unique())])
    con.executemany("INSERT INTO segmento_mercado(nombre) VALUES (?)",
                    [(n,) for n in sorted(df["new_market_segment"].dropna().unique())])

    sec = dict(con.execute("SELECT nombre, seccion_id FROM seccion_producto"))
    seg = dict(con.execute("SELECT nombre, segmento_id FROM segmento_mercado"))

    def nulo(x):
        return None if pd.isna(x) else x

    con.executemany(
        "INSERT INTO valor VALUES (?,?,?,?,?,?,?)",
        [(r.securities_code, r.name, int(r.universe0), r.effective_date,
          sec[r.section_products],
          None if pd.isna(r.sector33_code) else int(r.sector33_code),
          None if pd.isna(r.size_code) else int(r.size_code))
         for r in df.itertuples()])
    con.executemany(
        "INSERT INTO cotizacion VALUES (?,?,?,?,?)",
        [(r.securities_code, r.trade_date, float(r.close), float(r.issued_shares),
          float(r.market_cap)) for r in df.dropna(subset=["close"]).itertuples()])
    con.executemany(
        "INSERT INTO valor_segmento VALUES (?,?)",
        [(r.securities_code, seg[r.new_market_segment])
         for r in df.dropna(subset=["new_market_segment"]).itertuples()])
    con.commit()
    return con


def conteos(con: sqlite3.Connection) -> dict:
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in TABLAS}


if __name__ == "__main__":
    csv = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "stock_list_clean.csv"
    con = construir_db(csv, AQUI / "stock.db")
    print("Filas por tabla:", conteos(con))
    print("Violaciones de llave foránea:", len(con.execute("PRAGMA foreign_key_check").fetchall()))
