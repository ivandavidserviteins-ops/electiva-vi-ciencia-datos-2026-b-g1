"""Semana 6 - Dibuja el ERD del listado de valores de la Bolsa de Tokio (genera erd.png).

Autora: Zara Melisa Monroy Vera (zara-mon2006)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

AQUI = Path(__file__).resolve().parent
H = 0.36
ENC, PK, FK = "#0b6e75", "#fff4c2", "#e2f1f3"

# nombre: (x, y_superior, ancho, [(clave, columna, tipo)])
TABLAS = {
    "seccion_producto": (0.4, 9.7, 3.5, [("PK", "seccion_id", "INTEGER"), ("", "nombre", "TEXT UNIQUE")]),
    "tamano_indice": (12.1, 6.4, 3.5, [("PK", "tamano_codigo", "INTEGER"), ("", "nombre", "TEXT UNIQUE")]),
    "valor": (5.9, 9.7, 4.1, [
        ("PK", "codigo_valor", "TEXT"), ("", "nombre", "TEXT"), ("", "universe0", "INTEGER"),
        ("", "fecha_efectiva", "TEXT (ISO)"), ("FK", "seccion_id", "-> seccion_producto"),
        ("FK", "sector33_codigo", "-> sector33 (NULL)"), ("FK", "tamano_codigo", "-> tamano_indice (NULL)")]),
    "sector33": (0.4, 6.4, 3.5, [
        ("PK", "sector33_codigo", "INTEGER"), ("", "nombre", "TEXT UNIQUE"),
        ("FK", "sector17_codigo", "-> sector17")]),
    "sector17": (0.4, 3.9, 3.5, [("PK", "sector17_codigo", "INTEGER"), ("", "nombre", "TEXT UNIQUE")]),
    "cotizacion": (12.1, 9.7, 3.7, [
        ("PK,FK", "codigo_valor", "-> valor"), ("PK", "fecha_operacion", "TEXT"),
        ("", "cierre", "REAL"), ("", "acciones_emitidas", "REAL"), ("", "capitalizacion", "REAL")]),
    "valor_segmento": (6.1, 5.0, 3.7, [
        ("PK,FK", "codigo_valor", "-> valor"), ("PK,FK", "segmento_id", "-> segmento_mercado")]),
    "segmento_mercado": (12.1, 4.0, 3.5, [("PK", "segmento_id", "INTEGER"), ("", "nombre", "TEXT UNIQUE")]),
}


def dibujar_tabla(ax, nombre, x, y, w, cols):
    alto = H * (len(cols) + 1)
    ax.add_patch(Rectangle((x, y - alto), w, alto, fc="white", ec="#333", lw=1.2, zorder=2))
    ax.add_patch(Rectangle((x, y - H), w, H, fc=ENC, ec="#333", lw=1.2, zorder=3))
    ax.text(x + w / 2, y - H / 2, nombre, color="white", ha="center", va="center",
            fontsize=10, fontweight="bold", zorder=4)
    for i, (clave, col, tipo) in enumerate(cols):
        yf = y - H * (i + 2)
        if clave:
            ax.add_patch(Rectangle((x, yf), w, H, fc=PK if "PK" in clave else FK, ec="none", zorder=3))
        ax.text(x + 0.08, yf + H / 2, clave, fontsize=7.5, va="center", color="#8a5a00",
                fontweight="bold", zorder=4)
        ax.text(x + 0.85, yf + H / 2, col, fontsize=8.5, va="center", zorder=4)
        ax.text(x + w - 0.08, yf + H / 2, tipo, fontsize=7, va="center", ha="right",
                color="#555", zorder=4)
    return {"x": x, "y": y, "w": w, "h": alto}


def main():
    fig, ax = plt.subplots(figsize=(16, 9.4))
    ax.set_xlim(0, 16)
    ax.set_ylim(2.0, 10.7)
    ax.axis("off")
    c = {n: dibujar_tabla(ax, n, *t) for n, t in TABLAS.items()}

    def pt(n, lado, f=0.5):
        b = c[n]
        return {"izq": (b["x"], b["y"] - b["h"] * f), "der": (b["x"] + b["w"], b["y"] - b["h"] * f),
                "arr": (b["x"] + b["w"] * f, b["y"]), "aba": (b["x"] + b["w"] * f, b["y"] - b["h"])}[lado]

    def unir(puntos, uno, muchos):
        """Línea por `puntos`; '1' junto al primer punto y 'N' junto al último."""
        ax.plot([p[0] for p in puntos], [p[1] for p in puntos], color="#333", lw=1.4, zorder=1)
        for (p, q, txt) in ((puntos[0], puntos[1], uno), (puntos[-1], puntos[-2], muchos)):
            dx, dy = q[0] - p[0], q[1] - p[1]
            n = max((dx ** 2 + dy ** 2) ** 0.5, 1e-9)
            ax.text(p[0] + dx / n * 0.28 - dy / n * 0.18, p[1] + dy / n * 0.28 + dx / n * 0.18, txt,
                    fontsize=10, fontweight="bold", color=ENC, ha="center", va="center")

    unir([pt("seccion_producto", "der", 0.5), (4.9, pt("seccion_producto", "der", 0.5)[1]),
          (4.9, 9.2), (5.9, 9.2)], "1", "N")
    unir([pt("tamano_indice", "izq", 0.5), pt("valor", "der", 0.88)], "1", "N")
    unir([pt("sector33", "der", 0.5), (4.9, pt("sector33", "der", 0.5)[1]),
          (4.9, 7.55), (5.9, 7.55)], "1", "N")
    unir([pt("sector17", "arr", 0.5), pt("sector33", "aba", 0.5)], "1", "N")
    unir([pt("valor", "der", 0.18), pt("cotizacion", "izq", 0.3)], "1", "N")
    unir([pt("valor", "aba", 0.5), pt("valor_segmento", "arr", 0.5)], "1", "N")
    unir([pt("segmento_mercado", "izq", 0.5), pt("valor_segmento", "der", 0.5)], "1", "N")

    ax.text(8, 10.55, "ERD · Listado de valores de la Bolsa de Tokio (N:M valor ↔ segmento de mercado, "
            "resuelta con valor_segmento)", ha="center", fontsize=12, fontweight="bold")
    ax.text(8, 2.2, "PK = llave primaria   FK = llave foránea   1 → N = uno a muchos   (NULL) = el valor puede no "
            "tenerlo   Autora: Zara Melisa Monroy Vera", ha="center", fontsize=8.5, color="#444")
    fig.savefig(AQUI / "erd.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("erd.png generado")


if __name__ == "__main__":
    main()
