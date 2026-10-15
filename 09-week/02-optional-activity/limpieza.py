"""Semana 9 - Limpieza del listado de valores de la Bolsa de Tokio (stock_list.csv).

Autora: Zara Melisa Monroy Vera (zara-mon2006)

Uso:
    python limpieza.py                      # lee data/stock_list.csv
    python limpieza.py ruta/raw.csv ruta/salida_dir

Genera:
    data/stock_list_clean.csv           dataset limpio
    reportes/antes_despues.json         métricas antes/después
    reportes/antes_despues.md           la misma evidencia en tabla

Principio de diseño: NO se imputa ningún precio ni cantidad de acciones. Un
precio inventado es peor que un precio ausente; los faltantes se dejan como NA
y se documentan.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent

RENOMBRAR = {
    "SecuritiesCode": "securities_code",
    "EffectiveDate": "effective_date",
    "Name": "name",
    "Section/Products": "section_products",
    "NewMarketSegment": "new_market_segment",
    "33SectorCode": "sector33_code",
    "33SectorName": "sector33_name",
    "17SectorCode": "sector17_code",
    "17SectorName": "sector17_name",
    "NewIndexSeriesSizeCode": "size_code",
    "NewIndexSeriesSize": "size_name",
    "TradeDate": "trade_date",
    "Close": "close",
    "IssuedShares": "issued_shares",
    "MarketCapitalization": "market_cap",
    "Universe0": "universe0",
}
COLS_TEXTO = ["SecuritiesCode", "Name", "Section/Products", "NewMarketSegment",
              "33SectorName", "17SectorName", "NewIndexSeriesSize"]
COLS_NUMERICAS = ["Close", "IssuedShares", "MarketCapitalization"]
COLS_PRECIO = COLS_NUMERICAS + ["TradeDate"]


def leer_crudo(ruta: Path) -> pd.DataFrame:
    """Lee todo como texto y sin convertir nada a NaN (así se ven los marcadores)."""
    return pd.read_csv(ruta, dtype=str, keep_default_na=False)


def perfilar_antes(raw: pd.DataFrame, ruta: Path) -> dict:
    natural = pd.read_csv(ruta)                     # lectura "ingenua" de pandas
    vacios = {c: int((raw[c].str.strip() == "").sum()) for c in raw.columns}
    guiones = {c: int((raw[c].str.strip() == "-").sum()) for c in raw.columns}
    sobrantes = {c: int((raw[c] != raw[c].str.strip()).sum()) for c in raw.columns}
    no_ascii = {c: int(raw[c].map(lambda s: any(ord(ch) > 127 for ch in s)).sum())
                for c in raw.columns}
    return {
        "etiqueta": "antes",
        "filas": int(len(raw)),
        "columnas": int(raw.shape[1]),
        "filas_duplicadas_exactas": int(raw.duplicated().sum()),
        "codigos_repetidos": int(raw["SecuritiesCode"].duplicated().sum()),
        "nombres_repetidos_filas": int(raw["Name"].duplicated(keep=False).sum()),
        "celdas_vacias": int(sum(vacios.values())),
        "celdas_con_guion": int(sum(guiones.values())),
        "celdas_faltantes_total": int(sum(vacios.values()) + sum(guiones.values())),
        "marcadores_de_faltante_distintos": int(sum(1 for v in (vacios, guiones) if sum(v.values()))),
        "celdas_con_espacios_sobrantes": int(sum(sobrantes.values())),
        "celdas_con_caracteres_no_ascii_en_sectores": int(
            no_ascii["17SectorName"] + no_ascii["33SectorName"]),
        "valores_distintos_17SectorName": int(raw["17SectorName"].nunique()),
        "fechas_guardadas_como_decimal": int(raw["TradeDate"].str.endswith(".0").sum()),
        "tipos_lectura_ingenua": {c: str(t) for c, t in natural.dtypes.items()},
        "detalle_vacios": {c: n for c, n in vacios.items() if n},
        "detalle_guiones": {c: n for c, n in guiones.items() if n},
    }


def limpiar(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    # 1) Espacios: quitar bordes y colapsar espacios dobles dentro del texto
    for c in df.columns:
        df[c] = df[c].str.strip().str.replace(r"\s{2,}", " ", regex=True)

    # 2) Sectores: unificar caracteres de ancho completo, p. ej. "（EX BANKS）" -> "(EX BANKS)".
    #    En Name NO se normaliza: son nombres legales y no conviene alterarlos.
    for c in ("33SectorName", "17SectorName", "Section/Products", "NewMarketSegment"):
        df[c] = df[c].map(lambda s: unicodedata.normalize("NFKC", s).strip())

    # 3) Faltantes: '' y '-' significan lo mismo (no aplica / sin dato) -> un solo NA
    df = df.replace({"": pd.NA, "-": pd.NA})

    # 4) Tipos
    df["EffectiveDate"] = pd.to_datetime(df["EffectiveDate"], format="%Y%m%d")
    df["TradeDate"] = pd.to_datetime(df["TradeDate"].str.replace(r"\.0$", "", regex=True),
                                     format="%Y%m%d")
    for c in COLS_NUMERICAS:
        df[c] = pd.to_numeric(df[c]).astype("float64")
    for c in ("33SectorCode", "17SectorCode", "NewIndexSeriesSizeCode"):
        df[c] = pd.to_numeric(df[c]).astype("Int64")
    df["Universe0"] = df["Universe0"].map({"True": True, "False": False}).astype(bool)

    # 5) Validaciones (fallan con un mensaje claro si algo no cuadra)
    assert df["SecuritiesCode"].str.fullmatch(r"\d{4,5}").all(), \
        "código con formato inesperado (el válido es de 4 o 5 dígitos, p. ej. 25935)"
    assert df["SecuritiesCode"].is_unique, "código de valor repetido"
    assert df[COLS_PRECIO].isna().sum(axis=1).isin([0, 4]).all(), \
        "fila con precio a medias (debe tener los 4 campos o ninguno)"
    con_precio = df.dropna(subset=["Close"])
    err = ((con_precio["Close"] * con_precio["IssuedShares"] - con_precio["MarketCapitalization"]).abs()
           / con_precio["MarketCapitalization"]).max()
    assert err < 1e-6, f"capitalización != cierre x acciones (error relativo {err:.2e})"
    assert df.groupby("33SectorCode")["17SectorCode"].nunique().max() == 1, \
        "un sector de 33 grupos pertenece a más de un sector de 17"
    for cod, nom in (("17SectorCode", "17SectorName"), ("33SectorCode", "33SectorName"),
                     ("NewIndexSeriesSizeCode", "NewIndexSeriesSize")):
        assert df.groupby(cod)[nom].nunique().max() == 1, f"{cod} con más de un nombre"

    return df.rename(columns=RENOMBRAR).reset_index(drop=True)


def perfilar_despues(limpio: pd.DataFrame) -> dict:
    txt = limpio.select_dtypes(include=["object", "string"])
    sobrantes = int(sum((txt[c].dropna() != txt[c].dropna().str.strip()).sum() for c in txt))
    con_precio = limpio.dropna(subset=["close"])
    err = ((con_precio["close"] * con_precio["issued_shares"] - con_precio["market_cap"]).abs()
           / con_precio["market_cap"]).max()
    return {
        "etiqueta": "después",
        "filas": int(len(limpio)),
        "columnas": int(limpio.shape[1]),
        "filas_duplicadas_exactas": int(limpio.duplicated().sum()),
        "codigos_repetidos": int(limpio["securities_code"].duplicated().sum()),
        "nombres_repetidos_filas": int(limpio["name"].duplicated(keep=False).sum()),
        "celdas_vacias": 0,
        "celdas_con_guion": 0,
        "celdas_faltantes_total": int(limpio.isna().sum().sum()),
        "marcadores_de_faltante_distintos": 1,
        "celdas_con_espacios_sobrantes": sobrantes,
        "celdas_con_caracteres_no_ascii_en_sectores": int(sum(
            limpio[c].dropna().map(lambda s: any(ord(ch) > 127 for ch in s)).sum()
            for c in ("sector17_name", "sector33_name"))),
        "valores_distintos_17SectorName": int(limpio["sector17_name"].nunique()),
        "fechas_guardadas_como_decimal": 0,
        "tipos": {c: str(t) for c, t in limpio.dtypes.items()},
        "detalle_nulos": {c: int(n) for c, n in limpio.isna().sum().items() if n},
        "error_relativo_max_capitalizacion": float(err),
    }


def tabla_md(a: dict, d: dict) -> str:
    filas = [
        ("Filas", a["filas"], d["filas"]),
        ("Filas duplicadas exactas", a["filas_duplicadas_exactas"], d["filas_duplicadas_exactas"]),
        ("Códigos de valor repetidos", a["codigos_repetidos"], d["codigos_repetidos"]),
        ("Celdas faltantes (vacías o con «-»)", a["celdas_faltantes_total"], d["celdas_faltantes_total"]),
        ("Marcadores distintos para «faltante»", a["marcadores_de_faltante_distintos"],
         d["marcadores_de_faltante_distintos"]),
        ("Celdas con espacios sobrantes", a["celdas_con_espacios_sobrantes"],
         d["celdas_con_espacios_sobrantes"]),
        ("Valores distintos en `17SectorName` (son 17 sectores + sin sector)",
         a["valores_distintos_17SectorName"], d["valores_distintos_17SectorName"]),
        ("Celdas de sector con caracteres de ancho completo",
         a["celdas_con_caracteres_no_ascii_en_sectores"],
         d["celdas_con_caracteres_no_ascii_en_sectores"]),
        ("Fechas guardadas como decimal (`20211230.0`)", a["fechas_guardadas_como_decimal"],
         d["fechas_guardadas_como_decimal"]),
    ]
    out = ["| Métrica | Antes | Después |", "|---|---:|---:|"]
    out += [f"| {m} | {x:,} | {y:,} |".replace(",", " ") for m, x, y in filas]
    out += ["", "Faltantes por columna (antes → después, mismos valores, ahora como NA real): "
            + ", ".join(f"`{c}`={n}" for c, n in d["detalle_nulos"].items())]
    return "\n".join(out)


def main(ruta: Path, salida: Path) -> pd.DataFrame:
    raw = leer_crudo(ruta)
    antes = perfilar_antes(raw, ruta)
    limpio = limpiar(raw)
    despues = perfilar_despues(limpio)

    (salida / "data").mkdir(parents=True, exist_ok=True)
    (salida / "reportes").mkdir(parents=True, exist_ok=True)
    limpio.to_csv(salida / "data" / "stock_list_clean.csv", index=False, date_format="%Y-%m-%d")
    (salida / "reportes" / "antes_despues.json").write_text(
        json.dumps({"antes": antes, "despues": despues}, indent=2, ensure_ascii=False,
                   default=str), encoding="utf-8")
    (salida / "reportes" / "antes_despues.md").write_text(tabla_md(antes, despues) + "\n",
                                                           encoding="utf-8")
    print(tabla_md(antes, despues))
    return limpio


if __name__ == "__main__":
    raw_p = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "stock_list.csv"
    out_d = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI
    main(raw_p, out_d)
