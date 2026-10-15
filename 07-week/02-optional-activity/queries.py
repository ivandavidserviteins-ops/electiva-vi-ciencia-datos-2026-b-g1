"""Semana 7 - Ejecuta las 3 consultas SQL y reproduce el GROUP BY (y el WHERE) en pandas.

Autora: Zara Melisa Monroy Vera (zara-mon2006)

Uso:
    python queries.py

Requiere la carpeta 06-week al lado de esta (usa su modelo y su CSV limpio).
Escribe resultados.md con las salidas.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
SEMANA6 = AQUI.parent / "06-week"
sys.path.insert(0, str(SEMANA6))
from build_db import construir_db, leer_limpio  # noqa: E402


def cargar_consultas(ruta: Path) -> dict[str, str]:
    """Separa queries.sql en {Q1: sql, Q2: sql, Q3: sql} usando los marcadores [Qn]."""
    texto = ruta.read_text(encoding="utf-8")
    partes = re.split(r"^-- \[(Q\d)\].*$", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes), 2)}


def tabla_md(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    filas = ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([cab, sep, *filas])


def main() -> None:
    csv = SEMANA6 / "data" / "stock_list_clean.csv"
    con = construir_db(csv)               # base en memoria
    consultas = cargar_consultas(AQUI / "queries.sql")
    plano = leer_limpio(csv)              # versión plana para pandas

    sql = {k: pd.read_sql_query(q, con) for k, q in consultas.items()}

    # ---- Equivalente pandas de Q1 (WHERE) --------------------------------
    p1 = (plano.loc[plano["market_cap"] >= 5e12,
                    ["securities_code", "trade_date", "close", "market_cap"]]
          .rename(columns={"securities_code": "codigo_valor", "trade_date": "fecha_operacion",
                           "close": "cierre", "market_cap": "capitalizacion"})
          .sort_values(["capitalizacion", "codigo_valor"], ascending=[False, True])
          .reset_index(drop=True))
    pd.testing.assert_frame_equal(sql["Q1"], p1, check_dtype=False)

    # ---- Equivalente pandas de Q3 (GROUP BY) -----------------------------
    con_sector = plano.dropna(subset=["sector17_name"])
    g = con_sector.groupby("sector17_name")
    p3 = pd.DataFrame({
        "valores": g.size(),
        "con_cotizacion": g["close"].count(),
        "capitalizacion_total_billones_yen": (g["market_cap"].sum(min_count=1) / 1e12).round(2),
    }).reset_index().rename(columns={"sector17_name": "sector17"})
    p3 = p3.sort_values(["capitalizacion_total_billones_yen", "sector17"],
                        ascending=[False, True], na_position="last").reset_index(drop=True)
    pd.testing.assert_frame_equal(sql["Q3"], p3, check_dtype=False)

    print(f"Q1: {len(sql['Q1'])} cotizaciones con capitalización >= 5 billones de yenes  (SQL == pandas)")
    print(sql["Q1"].to_string(index=False))
    print("Q2: top 10 por capitalización")
    print(sql["Q2"].to_string(index=False))
    print("Q3: por sector de 17 grupos  (SQL == pandas)")
    print(sql["Q3"].to_string(index=False))

    explicacion = {
        "Q1": "Filtra con `WHERE` las cotizaciones de gran capitalización. Solo mira la tabla `cotizacion`, "
              "por eso no distingue acciones de ETF.",
        "Q2": "Une 6 tablas con `JOIN` para mostrar nombre, sector, serie de tamaño y segmento en lugar de "
              "códigos. Al exigir sector (JOIN interno) se excluyen ETF y fondos; `LEFT JOIN` con "
              "`tamano_indice` conserva los valores sin serie de tamaño.",
        "Q3": "Agrupa con `GROUP BY` por sector de 17 grupos para ver cuántos valores hay, cuántos tienen "
              "cotización y cuánta capitalización suman. Es una descripción del archivo, no una "
              "recomendación de inversión.",
    }
    md = ["# Resultados de la semana 7", "",
          "Generado por `queries.py`. Q1 y Q3 se verificaron contra su equivalente en pandas con "
          "`assert_frame_equal`. Capitalización en billones (10^12) de yenes; la moneda no viene "
          "declarada en el archivo.", ""]
    for k in ("Q1", "Q2", "Q3"):
        md += [f"## {k}", "", explicacion[k], "", "```sql", consultas[k], "```", "",
               f"Filas devueltas: {len(sql[k])}", "", tabla_md(sql[k]), ""]
    (AQUI / "resultados.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
