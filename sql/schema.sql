CREATE TABLE IF NOT EXISTS transactions (
    transaction_id        VARCHAR(50)    PRIMARY KEY,
    user_id               VARCHAR(50)    NOT NULL,
    merchant_id           VARCHAR(50)    NOT NULL,
    transaction_timestamp TIMESTAMP      NOT NULL,
    amount                NUMERIC(15, 2) NOT NULL CHECK (amount > 0),
    currency              VARCHAR(3)     NOT NULL,
    payment_method        VARCHAR(50),
    transaction_status    VARCHAR(20)    NOT NULL
                              CHECK (transaction_status IN ('SUCCESS', 'FAILED', 'PENDING')),
    created_at            TIMESTAMP      NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions_rejected (
    id           SERIAL    PRIMARY KEY,
    raw_data     TEXT,
    error_reason TEXT,
    rejected_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pipeline_run_log (
    id              SERIAL      PRIMARY KEY,
    run_id          VARCHAR(50) NOT NULL,
    run_timestamp   TIMESTAMP   DEFAULT NOW(),
    source_file     VARCHAR(255),
    total_rows      INTEGER,
    valid_rows      INTEGER,
    rejected_rows   INTEGER,
    duplicate_count INTEGER,
    status          VARCHAR(20),
    error_message   TEXT
);
