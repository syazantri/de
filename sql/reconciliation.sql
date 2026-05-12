SELECT
    (SELECT COUNT(*) FROM transactions)          AS loaded_count,
    (SELECT COUNT(*) FROM transactions_rejected) AS rejected_count,
    (SELECT COUNT(*) FROM transactions)
        + (SELECT COUNT(*) FROM transactions_rejected) AS total_processed;

SELECT
    run_id,
    run_timestamp,
    source_file,
    total_rows,
    valid_rows,
    rejected_rows,
    duplicate_count,
    status,
    error_message
FROM pipeline_run_log
ORDER BY run_timestamp DESC
LIMIT 5;

SELECT
    error_reason,
    COUNT(*) AS count
FROM transactions_rejected
GROUP BY error_reason
ORDER BY count DESC;

SELECT
    run_id,
    run_timestamp,
    total_rows,
    valid_rows,
    rejected_rows,
    ROUND(rejected_rows * 100.0 / NULLIF(total_rows, 0), 2) AS rejection_rate_pct,
    status
FROM pipeline_run_log
ORDER BY run_timestamp DESC;

SELECT
    DATE(transaction_timestamp) AS txn_date,
    COUNT(*)                    AS total_txns,
    COUNT(*) FILTER (WHERE transaction_status = 'SUCCESS') AS success_count,
    COUNT(*) FILTER (WHERE transaction_status = 'FAILED')  AS failed_count,
    COUNT(*) FILTER (WHERE transaction_status = 'PENDING') AS pending_count,
    SUM(amount) FILTER (WHERE transaction_status = 'SUCCESS') AS total_success_amount
FROM transactions
GROUP BY DATE(transaction_timestamp)
ORDER BY txn_date DESC;
