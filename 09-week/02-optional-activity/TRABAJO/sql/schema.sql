PRAGMA foreign_keys = ON;

CREATE TABLE legacy_board (            -- pre-2022 TSE board structure (Section/Products)
  board_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  board_group TEXT NOT NULL UNIQUE      -- First Section, Second Section, Mothers, JASDAQ Standard, ...
);
CREATE TABLE new_segment (             -- post-reform market segments
  segment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  segment_name  TEXT NOT NULL UNIQUE,
  segment_group TEXT NOT NULL           -- Prime | Standard | Growth
);
CREATE TABLE size_class (              -- TOPIX size series
  size_code TEXT PRIMARY KEY,
  size_name TEXT NOT NULL,
  size_rank INTEGER NOT NULL            -- 1 = Core30 (largest) ... 5 = Small 2
);
CREATE TABLE sector (                  -- 33-sector classification; 17-sector kept as an attribute
  sector_code   TEXT PRIMARY KEY,
  sector_name   TEXT NOT NULL,
  sector17_name TEXT NOT NULL
);
CREATE TABLE security (
  securities_code TEXT PRIMARY KEY,
  name            TEXT NOT NULL,
  legal_form      TEXT NOT NULL,
  instrument_type TEXT NOT NULL CHECK (instrument_type IN ('Equity','ETF/ETN','REIT/Fund')),
  is_foreign      INTEGER NOT NULL CHECK (is_foreign IN (0,1)),
  in_universe     INTEGER NOT NULL CHECK (in_universe IN (0,1)),
  listing_date    TEXT,                                     -- NULL = placeholder date in source (2000-01-01)
  board_id        INTEGER NOT NULL REFERENCES legacy_board(board_id),
  segment_id      INTEGER REFERENCES new_segment(segment_id), -- NULL = no new segment (funds, or equity without assignment)
  sector_code     TEXT    REFERENCES sector(sector_code),     -- NULL = not applicable / unclassified
  size_code       TEXT    REFERENCES size_class(size_code)    -- NULL = not in a TOPIX size series
);
CREATE TABLE quote (                   -- exists only for securities that traded on the snapshot date
  securities_code TEXT NOT NULL REFERENCES security(securities_code),
  trade_date      TEXT NOT NULL,
  close           REAL NOT NULL,
  issued_shares   INTEGER NOT NULL,
  market_cap      INTEGER NOT NULL,
  PRIMARY KEY (securities_code, trade_date)
);
CREATE INDEX idx_security_board ON security(board_id);
CREATE INDEX idx_security_size  ON security(size_code);
