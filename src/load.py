import json
from datetime import datetime

import pandas as pd
from sqlalchemy import text

from src.utils import get_db_engine, get_logger

logger = get_logger(__name__)


def load_valid(df: pd.DataFrame) -> int:
    if df.empty:
        logger.info("No valid rows to load")
        return 0

    engine = get_db_engine()

    # Write to a temporary staging table, then merge into the target
    df.to_sql("transactions_staging", engine, if_exists="replace", index=False)

    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                INSERT INTO transactions
                    (transaction_id, user_id, merchant_id, transaction_timestamp,
                     amount, currency, payment_method, transaction_status, created_at)
                SELECT
                    transaction_id, user_id, merchant_id, transaction_timestamp,
                    amount, currency, payment_method, transaction_status, created_at
                FROM transactions_staging
                ON CONFLICT (transaction_id) DO NOTHING
                """
            )
        )
        conn.execute(text("DROP TABLE IF EXISTS transactions_staging"))
        conn.commit()

    loaded = result.rowcount
    logger.info(f"Loaded {loaded} new rows into transactions table")
    return loaded


def load_rejected(rejected_df: pd.DataFrame) -> int:
    if rejected_df.empty:
        return 0

    engine = get_db_engine()
    records = []

    for _, row in rejected_df.iterrows():
        row_data = row.drop(labels=["error_reason"], errors="ignore").to_dict()
        records.append(
            {
                "raw_data": json.dumps(row_data, default=str),
                "error_reason": row.get("error_reason", "unknown"),
                "rejected_at": datetime.utcnow(),
            }
        )

    pd.DataFrame(records).to_sql(
        "transactions_rejected", engine, if_exists="append", index=False
    )

    logger.info(f"Stored {len(records)} rejected rows into transactions_rejected")
    return len(records)


def log_pipeline_run(
    run_id: str,
    source_file: str,
    total: int,
    valid: int,
    rejected: int,
    duplicates: int,
    status: str,
    error_msg: str = None,
) -> None:
    engine = get_db_engine()
    with engine.connect() as conn:
        conn.execute(
            text(
                """
                INSERT INTO pipeline_run_log
                    (run_id, source_file, total_rows, valid_rows, rejected_rows,
                     duplicate_count, status, error_message)
                VALUES
                    (:run_id, :source_file, :total, :valid, :rejected,
                     :duplicates, :status, :error_msg)
                """
            ),
            {
                "run_id": run_id,
                "source_file": source_file,
                "total": total,
                "valid": valid,
                "rejected": rejected,
                "duplicates": duplicates,
                "status": status,
                "error_msg": error_msg,
            },
        )
        conn.commit()
    logger.info(f"Pipeline run {run_id} logged with status={status}")
