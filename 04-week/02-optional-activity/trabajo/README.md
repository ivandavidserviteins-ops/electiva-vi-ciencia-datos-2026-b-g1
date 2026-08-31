# Diagnóstico de Datos de un Proceso — Predicción de Movimientos de Precio a partir del Volumen de Trading Institucional (JPX)

**Actividad Calificable · Corte 1 | Ciencia de Datos | Entrega Individual**

![Kaggle](https://img.shields.io/badge/Kaggle-JPX_Dataset-20BEFF?style=flat-square&logo=kaggle)
![Big Data](https://img.shields.io/badge/Big_Data-5_V's-blue?style=flat-square)
![ML](https://img.shields.io/badge/Machine_Learning-Supervisado-green?style=flat-square)
![Analytics](https://img.shields.io/badge/Analítica-Predictiva_%2F_Diagnóstica-red?style=flat-square)
![IEEE](https://img.shields.io/badge/Referencias-Formato_IEEE-orange?style=flat-square)

---

## 📌 Descripción

Diagnóstico de datos aplicado a un proceso real de decisión financiera: **la anticipación de movimientos de precio en el mercado bursátil japonés a partir del comportamiento del volumen de negociación institucional**. El proyecto utiliza el dataset **JPX Tokyo Stock Exchange Prediction**, publicado en Kaggle por Japan Exchange Group (JPX), con `trades.csv` como fuente protagonista, y responde a la pregunta de si los patrones de volumen semanal permiten anticipar movimientos de precio para apoyar decisiones de *timing* de entrada y salida de una posición. El trabajo cubre el inventario de datos, la clasificación del tipo de analítica, la justificación como caso de Big Data (5 V's), el ciclo de vida del proyecto y la comparación con el enfoque independiente de una compañera de curso sobre el mismo dataset.

> 📄 El desarrollo extendido de este trabajo (portada, abstract, marco teórico completo) está en **`TRABAJO_I_CORTE.pdf`**, incluido en esta misma carpeta.

---

## 📌 Nota importante: mismo dataset, enfoques distintos

Las actividades formativas de las semanas 1 a 4 (opcionales, sin nota) se desarrollaron **en pareja** con Zara Melisa Monroy Vera, por lo que ambos exploramos desde el inicio del corte el mismo dataset. La actividad calificable de este Corte 1 es de **entrega individual**: se mantiene el mismo dataset ya explorado (evitando partir de cero), pero cada integrante desarrolló su propia pregunta de negocio y enfoque analítico independiente.

| | Mi enfoque | Enfoque de mi compañera |
|---|---|---|
| **Pregunta de negocio** | ¿El volumen de negociación semanal anticipa movimientos de precio, para apoyar el timing de entrada/salida? | Predicción del retorno futuro de cada acción para construir un portafolio de inversión |
| **Archivo(s) protagonista(s)** | `trades.csv` (cruzado con `stock_prices.csv`) | `stock_prices.csv`, `financials.csv` |
| **Tipo de ML** | Supervisado — clasificación/regresión sobre variación de precio | Supervisado — regresión/ranking sobre retorno |
| **Granularidad temporal** | Semanal | Diaria |

---

## 🏗️ Arquitectura del análisis

| Etapa | Función | Fuentes / herramientas involucradas |
|---|---|---|
| **1. Pregunta** | Formular la pregunta de negocio y de datos | Definición del problema |
| **2. Obtener** | Descargar y consolidar las fuentes de datos | Kaggle, J-Quants API/Pro, TDnet, noticias Nikkei/NQN |
| **3. Limpiar** | Alinear granularidad temporal (semanal vs. diario) y tratar outliers de volumen | Python (Pandas), reglas de validación temporal |
| **4. Analizar** | Entrenar el modelo predictivo supervisado | ML (Random Forest / XGBoost) usando volumen como *feature* principal |
| **5. Visualizar** | Generar señales de entrada/salida y dashboards comparativos | Python/Matplotlib, Power BI |
| **6. Decidir** | Determinar el momento óptimo de entrada/salida | Decisión de negocio del inversionista |

---

## 🎯 Objetivo general

Diagnosticar la viabilidad y estructura de los datos disponibles en el conjunto **JPX Tokyo Stock Exchange Prediction**, con el fin de determinar su pertinencia para modelar y anticipar movimientos de precio de acciones del mercado bursátil japonés a partir de patrones de volumen de negociación institucional, como insumo para decisiones de timing de entrada y salida en una posición de inversión.

## 🎯 Objetivos específicos

- **Formular** una pregunta de negocio clara y accionable sobre la anticipación de movimientos de precio a partir del volumen de trading.
- **Elaborar** un inventario de al menos seis fuentes/campos de datos, clasificando cada una por su nivel de estructura.
- **Determinar** el tipo de analítica de datos aplicable y evaluar si el caso constituye un escenario de Big Data mediante las cinco V's.
- **Diseñar** el ciclo de vida del proyecto de datos aplicado al caso JPX, representado en diagramas de flujo.
- **Diferenciar** el enfoque analítico individual de este documento del enfoque de la compañera de trabajo en pareja.

---

## ❓ Problema y pregunta de datos

**Problema real:** los inversionistas institucionales en el mercado japonés, una vez decidido qué acción negociar, deben determinar **cuándo** es el momento óptimo para entrar o salir de la posición, con el fin de maximizar el retorno de la operación y minimizar el riesgo de un timing desfavorable.

**Pregunta de datos:**
> ¿Los patrones de volumen de negociación semanal permiten anticipar movimientos de precio antes de que ocurran, con el fin de apoyar decisiones de timing de entrada y salida de una posición de inversión?

Esta pregunta complementa el reto de evaluación definido por la competencia original organizada por Japan Exchange Group (JPX) en colaboración con AlpacaJapan Co., Ltd. [1], enfocándose en la dimensión temporal y de volumen del comportamiento del mercado.

---

## 🌐 Problem & Data *(English section)*

Institutional investors operating in the Japanese equity market face a recurring operational challenge distinct from stock selection: once a security has been chosen, they must determine the optimal moment to enter or exit a position, in order to maximize the return of the operation and minimize the risk of unfavorable timing [1]. Addressing this challenge systematically requires historical weekly trading volumes, daily stock prices, and corporate disclosure records, all of which are provided through the JPX Tokyo Stock Exchange Prediction dataset hosted on Kaggle and originally sourced from Japan Exchange Group's official data infrastructure [1], [2], [3]. Beyond the six structured files included in the original dataset, this project also incorporates semi-structured corporate disclosure records published through TDnet and unstructured financial news covering the listed companies, so the data inventory reflects the full range of structures found in a real business problem [4], [5]. The analytics type required is primarily **predictive analytics**, with a relevant **diagnostic** component, since the objective is to forecast short-term price movement using a supervised machine learning model trained on weekly trading-volume patterns cross-validated against daily price data [2]. Given the combination of structured, semi-structured, and unstructured sources, together with the need to reconcile data of different temporal granularities, this problem also raises meaningful **data veracity** challenges characteristic of Big Data scenarios [2].

---

## 🗂️ Inventario de datos (8 fuentes)

| # | Fuente / Campo | Tipo de dato | Descripción breve | Ref. |
|---|---|---|---|---|
| 1 | `trades.csv` **(protagonista)** | Estructurado | Resumen agregado de volúmenes de negociación semanal | [2] |
| 2 | `stock_prices.csv` | Estructurado | Precio de cierre diario (OHLC), usado para validación cruzada | [2] |
| 3 | `financials.csv` | Estructurado | Resultados de reportes de ganancias trimestrales | [2] |
| 4 | `options.csv` | Estructurado | Estado de opciones sobre el mercado japonés | [2] |
| 5 | `stock_list.csv` | Estructurado | Código de acción ↔ nombre de empresa ↔ industria | [2] |
| 6 | `secondary_stock_prices.csv` | Estructurado | Precios de valores menos líquidos | [2] |
| 7 | Noticias financieras Nikkei/NQN | **No estructurado** | Texto narrativo libre que puede explicar picos de volumen | [5] |
| 8 | Comunicados TDnet (TSE) | **Semiestructurado** | PDF/XBRL + metadatos, útiles para explicar anomalías de volumen | [4] |

📎 Tabla completa con justificación de clasificación disponible en `Inventario_datos_JPX_companero.xlsx` (hoja **"Inventario de datos"**) y en el PDF.

![Inventario de fuentes hacia decisión](images/inventario.png)
*Figura 1. Flujo de las ocho fuentes de datos hacia el pipeline de análisis y la señal de timing. Elaboración propia, asistida con IA (Claude, Anthropic).*

---

## 🧠 Tipo de analítica aplicada

| Tipo | Pregunta que responde | ¿Aplica al proyecto? |
|---|---|---|
| Descriptiva | ¿Qué pasó? | Sí (apoyo) |
| **Diagnóstica** | ¿Por qué pasó? | **Sí — relevante** |
| **Predictiva** | ¿Qué pasará? | **Sí — núcleo del proyecto** |
| Prescriptiva | ¿Qué se debería hacer? | Parcial |

**Tipo de ML:** supervisado (clasificación/regresión), usando el volumen de `trades.csv` como predictor principal de la variación de precio [2].

📎 Detalle completo en `Inventario_datos_JPX.xlsx` (hoja **"Tipo de analitica"**) y en el PDF.

---

## 📈 ¿Es un caso de Big Data? Justificación con las 5 V's

| V | Nivel | Justificación breve |
|---|---|---|
| Volumen | Media | `trades.csv` es un agregado semanal, más compacto que precios diarios |
| Velocidad | Media | Actualización semanal; procesamiento *batch* suficiente |
| **Variedad** | **Alta** | Estructurado + semiestructurado (TDnet) + no estructurado (noticias) |
| **Veracidad** | **Alta (reto principal)** | Desalineación temporal crítica entre volumen semanal y precio diario |
| Valor | Alta | Una señal de timing precisa mejora el retorno neto de las operaciones |

**Conclusión:** el caso se justifica como Big Data principalmente por **veracidad** (agregación temporal) y **variedad**, más que por el volumen bruto de los archivos [9].

📎 Análisis completo, reto de veracidad y mitigación en `Inventario_datos_JPX.xlsx` (hoja **"Big Data - 5 V"**) y en el PDF.

---

## 🔄 Ciclo de vida del proyecto

![Ciclo de vida del proyecto de datos](images/ciclo_vida.png)
*Figura 2. Ciclo de vida del proyecto de datos aplicado al caso de volumen de trading JPX. Elaboración propia, asistida con IA (Claude, Anthropic).*

```mermaid
flowchart LR
    A["1. Pregunta
    ¿volumen anticipa
    movimiento de precio?"] --> B["2. Obtener
    JPX / Kaggle / J-Quants / TDnet"]
    B --> C["3. Limpiar
    alinear semanal con diario"]
    C --> D["4. Analizar
    modelo ML supervisado"]
    D --> E["5. Visualizar
    señales de entrada/salida"]
    E --> F["6. Decidir
    timing de compra / venta"]
```

📎 Tabla de las 6 etapas con aplicación al caso y herramientas en `Inventario_datos_JPX.xlsx` (hoja **"Ciclo de vida"**) y en el PDF.

---

## 🆚 Comparación de enfoques con el trabajo de la compañera

| Criterio | Mi enfoque | Enfoque de mi compañera |
|---|---|---|
| Pregunta de negocio | ¿El volumen anticipa movimientos de precio para timing de entrada/salida? | Predicción de retorno para portafolio (top/bottom 200) |
| Archivo protagonista | `trades.csv` | `stock_prices.csv`, `financials.csv` |
| Tipo de analítica dominante | Predictiva con foco diagnóstico | Predictiva con salida prescriptiva |
| Tipo de ML | Supervisado — clasificación/regresión | Supervisado — regresión/ranking |
| Granularidad temporal | Semanal | Diaria |
| V crítica del Big Data | Veracidad (agregación temporal) | Variedad y Veracidad |
| Decisión de negocio habilitada | Momento óptimo de entrada/salida | Composición de un portafolio |

**Conclusión:** mi trabajo responde a **cuándo** actuar sobre una posición ya definida, mientras que el de mi compañera responde a **qué** acciones incluir en un portafolio — dos preguntas complementarias dentro de un flujo real de inversión. Ambos trabajos parten del mismo dataset por continuidad del trabajo en pareja, pero constituyen **análisis individuales, independientes y complementarios**.

📎 Tabla completa en `Inventario_datos_JPX.xlsx` (hoja **"Comparacion enfoques"**) y en el PDF.

---

## ✅ Conclusiones

El dataset **JPX Tokyo Stock Exchange Prediction** demostró ser una fuente de datos robusta, verificable y bien documentada institucionalmente por Japan Exchange Group (JPX) [1], [2], apta tanto para las actividades formativas en pareja como para el desarrollo de análisis individuales diferenciados. El problema se clasificó como **analítica predictiva** con componente **diagnóstico**, resuelto mediante **aprendizaje automático supervisado** [2], [10], y se justificó como caso de **Big Data** principalmente por veracidad y variedad, más que por volumen bruto [9]. El ciclo de vida completo se trazó de forma coherente, identificando la desalineación temporal entre `trades.csv` y `stock_prices.csv` como el principal reto de limpieza. Finalmente, se demostró que este trabajo y el de la compañera, aunque comparten el dataset de origen, constituyen entregas individuales, independientes y complementarias dentro de un flujo real de inversión.

*(Conclusiones completas en el PDF adjunto).*

---

## 📁 Archivos de este repositorio

```
04-week/02-optional-activity/trabajo
├── README.md                                  ← este archivo (resumen técnico)
├── TRABAJO_I_CORTE.pdf               ← documento completo
├── Inventario_datos_JPX.xlsx         ← anexo con tablas de inventario, analítica, Big Data y comparación
└── images/
    ├── ciclo_vida.png
    └── inventario.png
```

---

## 📚 Referencias (formato IEEE)

[1] Kaggle, "JPX Tokyo Stock Exchange Prediction," *Kaggle Competitions*, 2022. [Online]. Available: https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/overview. [Accessed: Aug. 30, 2026].

[2] Kaggle, "JPX Tokyo Stock Exchange Prediction — Data," *Kaggle Competitions*, 2022. [Online]. Available: https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/data. [Accessed: Aug. 30, 2026].

[3] Japan Exchange Group, "J-Quants API," *JPX Official Website*, 2026. [Online]. Available: https://www.jpx.co.jp/english/markets/other-data-services/j-quants-api/. [Accessed: Aug. 30, 2026].

[4] Japan Exchange Group, "Overview of TDnet," *JPX Official Website*, 2022. [Online]. Available: https://www.jpx.co.jp/english/equities/listing/disclosure/tdnet/index.html. [Accessed: Aug. 30, 2026].

[5] QUICK Corp., "QUICK APIs — Data Coverage (Nikkei/NQN News)," *QUICK Corporate Website*, 2022. [Online]. Available: https://corporate.quick.co.jp/en/apis/. [Accessed: Aug. 30, 2026].

[6] Japan Exchange Group, "Availability of English Disclosure Information by Listed Companies," *JPX English Disclosure GATE*, 2026. [Online]. Available: https://www.jpx.co.jp/english/equities/listed-co/disclosure-gate/availability/. [Accessed: Aug. 30, 2026].

[7] Japan Exchange Group, "J-Quants Pro," *JPX Official Website*, 2025. [Online]. Available: https://www.jpx.co.jp/english/markets/other-data-services/j-quants-pro/index.html. [Accessed: Aug. 30, 2026].

[8] Japan Exchange Group, "JPxData Portal," *JPX Official Website*, 2026. [Online]. Available: https://www.jpx.co.jp/english/markets/data-catalog/index.html. [Accessed: Aug. 30, 2026].

[9] IBM, "What is Big Data?," *IBM Think*, 2026. [Online]. Available: https://www.ibm.com/think/topics/big-data. [Accessed: Aug. 30, 2026].

[10] Qlik, "Embrace the Future — Make the Move from Descriptive to Prescriptive Analytics," *Qlik Blog*, 2022. [Online]. Available: https://www.qlik.com/blog/embrace-the-future-moving-from-descriptive-to-prescriptive-analytics. [Accessed: Aug. 30, 2026].

---

## 👤 Autor

| Nombre | Rol |
|---|---|
| **Iván David Cardozo Charry** | Autor (entrega individual) |

**Trabajo formativo en pareja (semanas 1-4, base del dataset):** Zara Melisa Monroy Vera

---

## 🎓 Información Académica

**Programa:** Ingeniería Industrial
**Asignatura:** Electiva VI Ciencia de Datos (Cód. 69109) [Pénsum 40D, Grupo 1]
**Institución:** Corporación Universitaria del Huila — CORHUILA
**Docente:** Jesús Ariel González Bonilla
**Fecha:** Agosto 30 de 2026

---



> Proyecto académico desarrollado para la Electiva VI Ciencia de Datos — Ingeniería Industrial, Corte 1, 2026-B.
