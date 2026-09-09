# Diagnóstico de Datos de un Proceso — Detección de Fraude Financiero en Tiempo Real en Bancolombia

**Actividad · Ciencia de Datos | Caso real: Bancolombia**

![Bancolombia](https://img.shields.io/badge/Caso_real-Bancolombia-FFD100?style=flat-square&labelColor=002855)
![Analytics](https://img.shields.io/badge/Analítica-Descriptiva_%2F_Predictiva-blue?style=flat-square)
![Data](https://img.shields.io/badge/Datos-Estructurado_%2F_Semi_%2F_No_estructurado-green?style=flat-square)
![IEEE](https://img.shields.io/badge/Referencias-Formato_IEEE-orange?style=flat-square)

---

## 📌 Descripción

Diagnóstico de datos aplicado a un caso real de negocio: **Bancolombia**, una de las entidades financieras más grandes de Colombia, y su necesidad de detectar transacciones potencialmente fraudulentas en tiempo real. El trabajo identifica cuatro tipos de datos generados por el proceso de monitoreo transaccional, clasificándolos según su nivel de estructura; formula una pregunta de analítica descriptiva y una de analítica predictiva; representa mediante un diagrama simple el flujo de la información (fuente → almacenamiento → análisis → visualización); y explica en inglés la diferencia entre ambos tipos de analítica, todo sustentado en fuentes académicas, gremiales e institucionales verificables sobre la prevención de fraude en el sector bancario colombiano.

---

## 🎯 Objetivo general

Diagnosticar los tipos de datos generados por el proceso de detección de fraude de Bancolombia y el tipo de analítica aplicable a dicho proceso, con el fin de ilustrar la clasificación de datos según su nivel de estructura y la diferencia entre analítica descriptiva y predictiva en un caso real de negocio del sector financiero colombiano.

## 🎯 Objetivos específicos

- **Identificar** cuatro tipos de datos generados por el proceso de monitoreo transaccional de Bancolombia, clasificándolos como estructurados, semiestructurados o no estructurados.
- **Formular** una pregunta de analítica descriptiva y una pregunta de analítica predictiva relevantes para la detección de fraude financiero.
- **Representar** mediante un diagrama simple el flujo de los datos desde su origen hasta su visualización (fuente → almacenamiento → análisis → visualización).
- **Explicar**, en inglés, la diferencia entre analítica descriptiva y analítica predictiva aplicada al caso de estudio.

---

## ❓ Introducción

El sector financiero colombiano atraviesa un proceso acelerado de transformación digital, en el cual la detección oportuna de fraudes se ha convertido en una prioridad crítica frente al aumento de transacciones digitales y la sofisticación de los métodos empleados por los defraudadores. Según el Informe de Gestión Gremial de Asobancaria 2024 [3], reportado también por la prensa financiera colombiana, el 73% de las entidades financieras del país ya cuentan con implementaciones basadas en inteligencia artificial que permiten automatizar procesos y detectar fraudes financieros en tiempo real [2]. Un caso particularmente representativo de este fenómeno es **Bancolombia**, uno de los bancos más grandes de Colombia [4], que enfrenta el reto constante de identificar transacciones potencialmente fraudulentas entre el enorme volumen de operaciones que procesa diariamente.

Para que un sistema de detección de fraude sea efectivo, no basta con generar alertas: es necesario clasificar adecuadamente los distintos tipos de datos involucrados en el proceso —desde el registro estructurado de cada transacción hasta los comentarios en texto libre de clientes que reportan actividad sospechosa— y distinguir entre el tipo de analítica que documenta lo que ya ocurrió y aquella que anticipa el riesgo antes de que la transacción se complete. Un trabajo de grado de la Maestría en Ciencia de Datos de la Universidad Javeriana Cali, desarrollado con el aval directo de Bancolombia, documenta precisamente este reto: los sistemas actuales de monitoreo alertan sobre clientes sospechosos, pero su incapacidad para contextualizar adecuadamente a cada cliente resulta en una alta tasa de falsos positivos [1].

El presente trabajo utiliza el caso real de Bancolombia para ilustrar la clasificación de datos según su nivel de estructura y la diferencia entre analítica descriptiva y predictiva, apoyándose en fuentes académicas, gremiales e institucionales verificables sobre el estado actual de la inteligencia artificial aplicada a la prevención de fraude en el sector bancario colombiano [1], [2], [3], [4].

---

## 🧠 Marco teórico

Para el desarrollo de este diagnóstico es necesario partir de dos conceptos fundamentales de la ciencia de datos. El primero es la **clasificación de los datos según su nivel de estructura**: los datos **estructurados** se organizan en un esquema fijo de filas y columnas, con tipos de dato claramente definidos, como ocurre en el registro de una transacción bancaria; los datos **semiestructurados** combinan cierta organización con flexibilidad, careciendo de un esquema rígido pero conservando etiquetas o metadatos que facilitan su interpretación, como los patrones de comportamiento transaccional de un cliente; y los datos **no estructurados** carecen de un formato predefinido, como ocurre con reportes de fraude en texto libre o conversaciones de atención al cliente [5].

El segundo concepto es el **tipo de analítica aplicada** a un problema de negocio: la **analítica descriptiva** responde a la pregunta "¿qué pasó?" mediante la agregación y visualización de datos históricos, mientras que la **analítica predictiva** responde a "¿qué pasará?" empleando modelos de aprendizaje automático entrenados sobre datos históricos para anticipar resultados futuros [6]. En el caso del sector bancario colombiano, la inteligencia artificial ya permite ir más allá de la detección posterior de fraude, avanzando hacia modelos que evalúan el riesgo de una transacción en tiempo real y bloquean actividades sospechosas antes de que se consoliden [2].

---

## 🗂️ Los 4 tipos de datos

| # | Dato | Clasificación |
|---|---|---|
| 1 | Registro de cada transacción (monto, fecha, cuenta origen/destino, canal utilizado) en el core bancario | **Estructurado** |
| 2 | Historial de comportamiento transaccional del cliente (patrones de gasto, ubicación habitual, frecuencia de operaciones) | **Semiestructurado** |
| 3 | Reportes de clientes sobre transacciones sospechosas (línea telefónica o formularios de texto libre) | **No estructurado** |
| 4 | Conversaciones registradas con el chatbot o la línea de atención al cliente sobre posibles casos de fraude | **No estructurado** |

📎 Tabla completa con justificación en `Tipos_de_datos_Bancolombia.xlsx`.

---

## 🧩 Preguntas de analítica

**Descriptiva:** ¿Cuántas transacciones fueron marcadas como sospechosas por los sistemas de monitoreo de Bancolombia durante el último mes?

**Predictiva:** ¿Qué probabilidad tiene una transacción específica de ser fraudulenta, considerando el comportamiento histórico del cliente y el contexto de la operación (monto, canal, ubicación)? [1]

---

## 🔄 Diagrama de flujo de datos

![Flujo de datos de Bancolombia](images/diagrama_flujo_bancolombia.png)
*Figura 1. Flujo de datos aplicado al proceso de detección de fraude en tiempo real en Bancolombia. Elaboración propia, asistida con IA (Claude, Anthropic), con base en [1], [2].*

- **Fuente:** cada transacción y el comportamiento histórico del cliente se capturan al momento de la operación.
- **Almacenamiento:** la información se consolida en el core bancario y en el data warehouse de la entidad.
- **Análisis:** un modelo de aprendizaje automático calcula un puntaje de riesgo (*scoring*) para cada transacción, buscando contextualizar mejor a cada cliente y reducir los falsos positivos [1].
- **Visualización:** el resultado se traduce en una alerta para el analista de fraude o en el bloqueo automático de la transacción [2].

---

## 🌐 Two sentences in English

- *Descriptive analytics is defined as the process of examining historical data to summarize and explain what has already occurred within an organization; in Bancolombia's case, this is reflected in reporting how many transactions were flagged as suspicious by the bank's monitoring systems over a given period, a figure that can only be produced by reviewing past alerts and transactional records after they have already been generated [1].*

- *Predictive analytics, in contrast, is defined as the use of historical and real-time data, often through machine learning models, to forecast outcomes that have not yet happened; Bancolombia applies this concept when it estimates, before a transaction is even completed, the probability that it is fraudulent based on the customer's past behavior, a data-driven approach aimed at reducing the high false-positive rate of current monitoring systems, in line with the broader trend in which 73% of Colombian banks now use artificial intelligence to detect fraud in real time [1], [2].*

---

## ✅ Conclusión

El diagnóstico realizado sobre Bancolombia permitió comprobar que la clasificación de datos según su nivel de estructura y la diferenciación entre analítica descriptiva y predictiva no son conceptos abstractos, sino herramientas que una entidad financiera colombiana real aplica activamente para enfrentar el reto de la detección de fraude en un entorno de creciente digitalización transaccional [1], [2].

Se identificaron y clasificaron cuatro tipos de datos generados por el proceso de monitoreo transaccional de Bancolombia —registros de transacciones, historial de comportamiento del cliente, reportes de fraude y conversaciones de atención al cliente—, evidenciando que un mismo proceso de negocio convive simultáneamente con información estructurada, semiestructurada y no estructurada, cada una con requerimientos de procesamiento distintos [1].

Se formularon además una pregunta de analítica descriptiva y una de analítica predictiva aplicadas al mismo proceso de fraude, lo cual permitió ilustrar con claridad la diferencia funcional entre ambos tipos de analítica: mientras la primera se limita a reportar cuántas transacciones fueron marcadas como sospechosas en el pasado, la segunda estima la probabilidad de que una transacción nueva sea fraudulenta antes de que se complete, precisamente el reto que motiva el desarrollo de modelos más contextualizados para reducir los falsos positivos [1].

Por otra parte, se representó mediante un diagrama simple el flujo completo de la información dentro del proceso de detección de fraude, desde la captura de la transacción hasta la generación de una alerta o el bloqueo automático de la operación, lo cual permitió comprender de forma visual cómo se articulan las distintas etapas del proceso de datos en un caso de negocio real del sector financiero.

Finalmente, se explicó en inglés la diferencia conceptual entre analítica descriptiva y predictiva, ejemplificando cada definición con evidencia concreta del contexto bancario colombiano —el reporte histórico de transacciones sospechosas y la estimación anticipada del riesgo de fraude—, demostrando que ambos conceptos pueden sustentarse con datos reales y no solo con definiciones teóricas [1], [2].

---

## 📚 Referencias (formato IEEE)

[1] S. A. Patiño Munera and J. A. Berrio Arenas, "Herramienta para detectar clientes potencialmente fraudulentos de Bancolombia," Proyecto Aplicado, Maestría en Ciencia de Datos, Pontificia Universidad Javeriana Cali, Cali, Colombia, 2025. [Online]. Available: https://vitela.javerianacali.edu.co/bitstreams/cb05abac-2ac6-4025-a639-41dd2d735ba5/download. [Accessed: Aug. 31, 2026].

[2] La República / DPL News, "Colombia: La inteligencia artificial ya está presente en 73% de las entidades bancarias," *DPL News*, 2025. [Online]. Available: https://dplnews.com/?p=269634. [Accessed: Aug. 31, 2026].

[3] Asobancaria, "Informe de Gestión Gremial 2024," *Asobancaria*, 2024. [Online]. Available: https://www.asobancaria.com/. [Accessed: Aug. 31, 2026].

[4] Bancolombia S.A., "Sitio web oficial," *Bancolombia*, 2026. [Online]. Available: https://www.bancolombia.com/. [Accessed: Aug. 31, 2026].

[5] IBM, "What is Big Data?," *IBM Think*, 2026. [Online]. Available: https://www.ibm.com/think/topics/big-data. [Accessed: Aug. 31, 2026].

[6] Qlik, "Embrace the Future — Make the Move from Descriptive to Prescriptive Analytics," *Qlik Blog*, 2022. [Online]. Available: https://www.qlik.com/blog/embrace-the-future-moving-from-descriptive-to-prescriptive-analytics. [Accessed: Aug. 31, 2026].

---

## 📁 Archivos de este repositorio

05-week/parcial-c1
├── README.md                       ← este archivo (resumen técnico)
├── Tipos_de_datos_Bancolombia.xlsx        ← anexo con la tabla de los 4 tipos de datos
└── images/
    └── diagrama_flujo_bancolombia.png
    
> Actividad desarrollada aplicando los conceptos de clasificación de datos y tipos de analítica a un caso real de negocio: Bancolombia.
