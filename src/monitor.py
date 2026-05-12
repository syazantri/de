from sqlalchemy import text
from src.utils import get_db_engine, get_logger

logger = get_logger(__name__)

_SEP = "=" * 56


def print_pipeline_report() -> None:
    engine = get_db_engine()

    with engine.connect() as conn:
        latest = conn.execute(
            text(
                """
                SELECT run_id, run_timestamp, source_file,
                       total_rows, valid_rows, rejected_rows, duplicate_count, status
                FROM pipeline_run_log
                ORDER BY run_timestamp DESC
                LIMIT 1
                """
            )
        ).fetchone()

        null_counts = conn.execute(
            text(
                """
                SELECT
                    COUNT(*) FILTER (WHERE transaction_id IS NULL)     AS null_transaction_id,
                    COUNT(*) FILTER (WHERE user_id IS NULL)            AS null_user_id,
                    COUNT(*) FILTER (WHERE amount IS NULL)             AS null_amount,
                    COUNT(*) FILTER (WHERE currency IS NULL)           AS null_currency,
                    COUNT(*) FILTER (WHERE transaction_status IS NULL) AS null_status
                FROM transactions
                """
            )
        ).fetchone()

        status_dist = conn.execute(
            text(
                """
                SELECT transaction_status, COUNT(*) AS count
                FROM transactions
                GROUP BY transaction_status
                ORDER BY count DESC
                """
            )
        ).fetchall()

        rejected_reasons = conn.execute(
            text(
                """
                SELECT error_reason, COUNT(*) AS count
                FROM transactions_rejected
                GROUP BY error_reason
                ORDER BY count DESC
                LIMIT 5
                """
            )
        ).fetchall()

    print(f"\n{_SEP}")
    print("  TRANSACTION PIPELINE MONITOR REPORT")
    print(_SEP)

    if latest:
        print(f"\n  Latest Run")
        print(f"  {'Run ID':<20}: {latest.run_id}")
        print(f"  {'Timestamp':<20}: {latest.run_timestamp}")
        print(f"  {'Source file':<20}: {latest.source_file}")
        print(f"  {'Status':<20}: {latest.status}")
        print(f"  {'Total rows':<20}: {latest.total_rows}")
        print(f"  {'Valid rows':<20}: {latest.valid_rows}")
        print(f"  {'Rejected rows':<20}: {latest.rejected_rows}")
        print(f"  {'Duplicates':<20}: {latest.duplicate_count}")
    else:
        print("\n  No pipeline runs recorded yet.")

    print(f"\n  Null Counts (transactions table)")
    if null_counts:
        print(f"  {'transaction_id':<20}: {null_counts.null_transaction_id}")
        print(f"  {'user_id':<20}: {null_counts.null_user_id}")
        print(f"  {'amount':<20}: {null_counts.null_amount}")
        print(f"  {'currency':<20}: {null_counts.null_currency}")
        print(f"  {'status':<20}: {null_counts.null_status}")

    print(f"\n  Transaction Status Breakdown")
    for row in status_dist:
        print(f"  {row.transaction_status:<20}: {row.count}")

    if rejected_reasons:
        print(f"\n  Top Rejection Reasons")
        for row in rejected_reasons:
            print(f"  {row.count:>4}x  {row.error_reason}")

    print(f"\n{_SEP}\n")
