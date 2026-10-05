# ERD v2 — Tokyo Stock Exchange: legacy boards → new segments

```mermaid
erDiagram
    LEGACY_BOARD  ||--o{ SECURITY : "was listed on"
    NEW_SEGMENT   |o--o{ SECURITY : "now belongs to"
    SECTOR        |o--o{ SECURITY : "classified in"
    SIZE_CLASS    |o--o{ SECURITY : "sized as"
    SECURITY      ||--o| QUOTE    : "has (if it traded)"

    LEGACY_BOARD {
        int  board_id PK
        text board_group UK "First Section, Second Section, Mothers, JASDAQ ..."
    }
    NEW_SEGMENT {
        int  segment_id PK
        text segment_name UK
        text segment_group "Prime | Standard | Growth"
    }
    SIZE_CLASS {
        text size_code PK
        text size_name
        int  size_rank "1 = Core30 ... 5 = Small 2"
    }
    SECTOR {
        text sector_code PK
        text sector_name
        text sector17_name "macro-sector kept as attribute"
    }
    SECURITY {
        text securities_code PK
        text name
        text legal_form "derived from name"
        text instrument_type "Equity | ETF/ETN | REIT/Fund"
        bool is_foreign
        bool in_universe
        date listing_date "NULL when source had placeholder 2000-01-01"
        int  board_id FK "NOT NULL"
        int  segment_id FK "NULL allowed"
        text sector_code FK "NULL allowed"
        text size_code FK "NULL allowed"
    }
    QUOTE {
        text securities_code PK, FK
        date trade_date PK
        float close
        int  issued_shares
        int  market_cap
    }
```

## Cardinalities

| Relationship | Cardinality | Meaning |
|---|---|---|
| LEGACY_BOARD → SECURITY | 1 : N, mandatory | every security came from exactly one legacy board / product group |
| NEW_SEGMENT → SECURITY | 0..1 : N, **optional** | funds and some equities have no new segment (stored as `NULL`, not as a fake label) |
| SECTOR → SECURITY | 0..1 : N, optional | funds are "not applicable"; some equities are unclassified |
| SIZE_CLASS → SECURITY | 0..1 : N, optional | only TOPIX constituents have a size class |
| SECURITY → QUOTE | 1 : 0..1 per date | a quote exists only if the security traded on the snapshot date (4,121 of 4,417) |

## Design decisions (different from v1)

* The ERD is centred on the **market reform**: the old board (`LEGACY_BOARD`) and the new segment (`NEW_SEGMENT`) are both entities, so the migration can be answered with two joins.
* Foreign keys are **optional** where the source has legitimately missing data; the database keeps `NULL` instead of inventing categories, and queries use `LEFT JOIN`.
* `QUOTE` is separate and only populated when a price exists, so there are no rows full of NULL prices.
* The 17-sector name is kept as an attribute of `SECTOR` (acceptable 2NF trade-off) to keep the model compact.
