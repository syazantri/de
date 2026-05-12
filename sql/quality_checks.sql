SELECT
    COUNT(*) FILTER (WHERE transaction_id IS NULL)                              AS null_transaction_ids,
    COUNT(*) FILTER (WHERE user_id IS NULL)                                     AS null_user_ids,
    COUNT(*) FILTER (WHERE merchant_id IS NULL)                                 AS null_merchant_ids,
    COUNT(*) FILTER (WHERE amount IS NULL OR amount <= 0)                       AS invalid_amounts,
    COUNT(*) FILTER (WHERE currency IS NULL OR TRIM(currency) = '')             AS null_currencies,
    COUNT(*) FILTER (WHERE transaction_status NOT IN ('SUCCESS','FAILED','PENDING')) AS invalid_statuses
FROM transactions;

SELECT transaction_id, COUNT(*) AS occurrences
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

SELECT
    MIN(amount)  AS min_amount,
    MAX(amount)  AS max_amount,
    ROUND(AVG(amount)::numeric, 2) AS avg_amount,
    COUNT(*)     AS total_rows
FROM transactions;

SELECT
    transaction_status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
FROM transactions
GROUP BY transaction_status
ORDER BY count DESC;

SELECT payment_method, COUNT(*) AS count
FROM transactions
GROUP BY payment_method
ORDER BY count DESC;

SELECT currency, COUNT(*) AS count
FROM transactions
GROUP BY currency
ORDER BY count DESC;

SELECT
    MIN(transaction_timestamp) AS earliest_txn,
    MAX(transaction_timestamp) AS latest_txn
FROM transactions;
