"""Semana 10 - Mini-proyecto de datos (cierre del Corte 2).

Autora: Zara Melisa Monroy Vera (zara-mon2006)

Integra lo del corte en un solo flujo:
    EXTRAER (CSV crudo)  ->  LIMPIAR (pandas, semana 9)
    ->  CARGAR en el modelo relacional (semana 6)
    ->  ANALIZAR con 2 consultas (SQL y pandas, semana 7)

Uso:
    python pipeline.py

Necesita las carpetas 06-week y 09-week al lado de esta (reutiliza su código).
Escribe todo en salidas/. Los análisis son descriptivos: no son recomendaciones de inversión.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "09-week"))
sys.path.insert(0, str(AQUI.parent / "06-week"))
from limpieza import leer_crudo, limpiar, perfilar_antes, perfilar_despues  # noqa: E402  (semana 9)
from build_db import conteos, construir_db, leer_limpio  # noqa: E402  (semana 6)

SALIDAS = AQUI / "salidas"
TEAL = "#0b6e75"
NARANJA = "#c4650a"

# --- Análisis 1: SQL = filtro (WHERE) + agregación (GROUP BY) ---------------
# Solo acciones con cotización: exigir sector33 deja fuera ETF y fondos.
SQL_ANALISIS_1 = """
SELECT g.nombre                               AS segmento,
       COUNT(*)                               AS valores_con_cotizacion,
       ROUND(SUM(c.capitalizacion) / 1e12, 2) AS capitalizacion_total_billones_yen,
       ROUND(AVG(c.capitalizacion) / 1e9, 1)  AS capitalizacion_promedio_miles_millones_yen
FROM valor AS v
JOIN cotizacion       AS c ON c.codigo_valor = v.codigo_valor
JOIN valor_segmento   AS vs ON vs.codigo_valor = v.codigo_valor
JOIN segmento_mercado AS g ON g.segmento_id = vs.segmento_id
WHERE v.sector33_codigo IS NOT NULL
GROUP BY g.segmento_id, g.nombre
ORDER BY capitalizacion_total_billones_yen DESC, g.nombre;
"""


def extraer(ruta: Path) -> pd.DataFrame:
    """E: lee el CSV tal cual (todo como texto, sin interpretar nada)."""
    df = leer_crudo(ruta)
    print(f"[extraer] {len(df)} filas x {df.shape[1]} columnas desde {ruta.name}")
    return df


def limpiar_datos(raw: pd.DataFrame, ruta: Path):
    """T: aplica la limpieza de la semana 9 y mide antes/después."""
    antes = perfilar_antes(raw, ruta)
    limpio = limpiar(raw)
    despues = perfilar_despues(limpio)
    print(f"[limpiar] filas {antes['filas']} -> {despues['filas']} | "
          f"faltantes {antes['celdas_faltantes_total']} -> {despues['celdas_faltantes_total']} "
          "(sin imputar) | "
          f"espacios sobrantes {antes['celdas_con_espacios_sobrantes']} -> "
          f"{despues['celdas_con_espacios_sobrantes']}")
    return limpio, antes, despues


def cargar(limpio: pd.DataFrame):
    """L: guarda el CSV limpio y lo carga en el modelo relacional normalizado."""
    SALIDAS.mkdir(exist_ok=True)
    csv = SALIDAS / "stock_list_clean.csv"
    limpio.to_csv(csv, index=False, date_format="%Y-%m-%d")
    con = construir_db(csv, SALIDAS / "stock.db")
    assert con.execute("PRAGMA foreign_key_check").fetchall() == [], "llaves foráneas rotas"
    print(f"[cargar] {conteos(con)}")
    return con, csv


def analizar(con, csv: Path):
    plano = leer_limpio(csv)
    acciones = plano[plano["sector33_code"].notna() & plano["close"].notna()]

    # ---- Análisis 1 (SQL): capitalización por segmento de mercado
    a1 = pd.read_sql_query(SQL_ANALISIS_1, con)
    # Mediana en pandas (SQLite no trae MEDIAN): la media sola engaña con datos tan sesgados
    med = (acciones.dropna(subset=["new_market_segment"]).groupby("new_market_segment")["market_cap"]
           .median().div(1e9).round(1).rename("capitalizacion_mediana_miles_millones_yen"))
    a1 = a1.merge(med, left_on="segmento", right_index=True, how="left")

    # Verificación cruzada SQL == pandas (conteo y suma)
    chk = (acciones.dropna(subset=["new_market_segment"]).groupby("new_market_segment")["market_cap"]
           .agg(["count", "sum"]))
    chk["sum"] = (chk["sum"] / 1e12).round(2)
    s = a1.set_index("segmento")
    assert (chk["count"].sort_index().values == s["valores_con_cotizacion"].sort_index().values).all()
    assert (chk["sum"].sort_index().values ==
            s["capitalizacion_total_billones_yen"].sort_index().values).all()

    # ---- Análisis 2 (pandas): concentración de la capitalización por serie de tamaño TOPIX
    total = acciones["market_cap"].sum()
    por_tamano = (acciones.assign(serie=acciones["size_name"].fillna("Sin serie de tamaño"))
                  .groupby("serie")
                  .agg(valores=("securities_code", "count"), capitalizacion=("market_cap", "sum"))
                  .reset_index())
    por_tamano["pct_capitalizacion"] = (100 * por_tamano["capitalizacion"] / total).round(1)
    por_tamano["capitalizacion_billones_yen"] = (por_tamano.pop("capitalizacion") / 1e12).round(2)
    a2 = por_tamano.sort_values("capitalizacion_billones_yen", ascending=False).reset_index(drop=True)
    top10 = 100 * acciones["market_cap"].nlargest(10).sum() / total
    print(f"[analizar] {len(acciones)} acciones con cotización; top 10 = {top10:.1f} % de la capitalización")

    a1.to_csv(SALIDAS / "analisis1_capitalizacion_por_segmento.csv", index=False)
    a2.to_csv(SALIDAS / "analisis2_concentracion_por_serie_tamano.csv", index=False)
    print("[analizar] análisis 1 (SQL) y 2 (pandas) listos; verificación cruzada OK")
    return a1, a2, round(top10, 1), len(acciones)


def graficar(a1: pd.DataFrame, a2: pd.DataFrame) -> None:
    fig, ejes = plt.subplots(1, 2, figsize=(15, 5.4))
    d1 = a1.sort_values("capitalizacion_total_billones_yen")
    ejes[0].barh(d1["segmento"], d1["capitalizacion_total_billones_yen"], color=TEAL)
    ejes[0].set_xlabel("Capitalización total (billones de yenes)")
    ejes[0].set_title("Análisis 1 · Capitalización por segmento\n(solo acciones con cotización)", fontsize=11)
    for i, (v, n) in enumerate(zip(d1["capitalizacion_total_billones_yen"], d1["valores_con_cotizacion"])):
        ejes[0].text(v + d1["capitalizacion_total_billones_yen"].max() * 0.01, i,
                     f"{v:,.1f}  (n={n})", va="center", fontsize=8)
    ejes[0].set_xlim(0, d1["capitalizacion_total_billones_yen"].max() * 1.25)

    d2 = a2.sort_values("pct_capitalizacion")
    ejes[1].barh(d2["serie"], d2["pct_capitalizacion"], color=NARANJA)
    ejes[1].set_xlabel("% de la capitalización total de las acciones")
    ejes[1].set_title("Análisis 2 · Concentración por serie de tamaño TOPIX", fontsize=11)
    for i, (p, n) in enumerate(zip(d2["pct_capitalizacion"], d2["valores"])):
        ejes[1].text(p + 0.6, i, f"{p:.1f} %  (n={n})", va="center", fontsize=8)
    ejes[1].set_xlim(0, d2["pct_capitalizacion"].max() * 1.3)
    for ax in ejes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Mini-proyecto · Listado de la Bolsa de Tokio (cierres de 2021) · Zara Melisa Monroy Vera",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SALIDAS / "analisis.png", dpi=140, facecolor="white")


def main() -> None:
    ruta = AQUI / "data" / "stock_list.csv"
    raw = extraer(ruta)
    limpio, antes, despues = limpiar_datos(raw, ruta)
    con, csv = cargar(limpio)
    a1, a2, top10, n_acc = analizar(con, csv)
    graficar(a1, a2)
    print("\nAnálisis 1 (SQL):\n" + a1.to_string(index=False))
    print("\nAnálisis 2 (pandas):\n" + a2.to_string(index=False))


if __name__ == "__main__":
    main()
