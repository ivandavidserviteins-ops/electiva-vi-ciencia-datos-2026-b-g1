# ERD en Mermaid (se renderiza directamente en GitHub)

```mermaid
erDiagram
    SECTOR17 ||--o{ SECTOR33 : "agrupa"
    SECTOR33 |o--o{ VALOR : "clasifica"
    SECCION_PRODUCTO ||--o{ VALOR : "ubica"
    TAMANO_INDICE |o--o{ VALOR : "dimensiona"
    VALOR ||--o{ COTIZACION : "tiene"
    VALOR ||--o{ VALOR_SEGMENTO : "pertenece a"
    SEGMENTO_MERCADO ||--o{ VALOR_SEGMENTO : "agrupa"

    SECTOR17 {
        int sector17_codigo PK
        text nombre UK
    }
    SECTOR33 {
        int sector33_codigo PK
        text nombre UK
        int sector17_codigo FK
    }
    TAMANO_INDICE {
        int tamano_codigo PK
        text nombre UK
    }
    SECCION_PRODUCTO {
        int seccion_id PK
        text nombre UK
    }
    SEGMENTO_MERCADO {
        int segmento_id PK
        text nombre UK
    }
    VALOR {
        text codigo_valor PK
        text nombre
        int universe0
        text fecha_efectiva
        int seccion_id FK
        int sector33_codigo FK "NULL"
        int tamano_codigo FK "NULL"
    }
    COTIZACION {
        text codigo_valor PK,FK
        text fecha_operacion PK
        real cierre
        real acciones_emitidas
        real capitalizacion
    }
    VALOR_SEGMENTO {
        text codigo_valor PK,FK
        int segmento_id PK,FK
    }
```
