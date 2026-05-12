import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)

VALID_STATUSES = {"SUCCESS", "FAILED", "PENDING"}


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    error_reasons = []

    for _, row in df.iterrows():
        errors = []

        # transaction_id must not be null or empty
        txn_id = str(row.get("transaction_id", "")).strip()
        if not txn_id:
            errors.append("transaction_id is null or empty")

        # amount must be a positive number
        try:
            amount = float(row.get("amount", "0"))
            if amount <= 0:
                errors.append(f"amount must be > 0, got {amount}")
        except (ValueError, TypeError):
            errors.append(f"amount is not a valid number: {row.get('amount')!r}")

        # currency must not be null or empty
        currency = str(row.get("currency", "")).strip()
        if not currency:
            errors.append("currency is null or empty")

        # transaction_timestamp must be parseable as a datetime
        ts_raw = row.get("transaction_timestamp", "")
        try:
            pd.to_datetime(ts_raw)
        except Exception:
            errors.append(f"transaction_timestamp is not parseable: {ts_raw!r}")

        # transaction_status must be one of the allowed values
        status = str(row.get("transaction_status", "")).strip().upper()
        if status not in VALID_STATUSES:
            errors.append(
                f"transaction_status '{status}' is invalid "
                f"(expected one of: {', '.join(sorted(VALID_STATUSES))})"
            )

        error_reasons.append("; ".join(errors))

    df = df.copy()
    df["_error_reason"] = error_reasons

    failed_mask = df["_error_reason"] != ""
    valid_df = df[~failed_mask].copy()
    rejected_df = df[failed_mask].copy()
    dup_mask = valid_df.duplicated(subset=["transaction_id"], keep="first")
    dup_df = valid_df[dup_mask].copy()
    dup_df["_error_reason"] = "duplicate transaction_id"

    valid_df = valid_df[~dup_mask].copy()
    rejected_df = pd.concat([rejected_df, dup_df], ignore_index=True)

    valid_df = valid_df.drop(columns=["_error_reason"])
    rejected_df = rejected_df.rename(columns={"_error_reason": "error_reason"})

    dup_count = int(dup_mask.sum())
    logger.info(
        f"Validation complete: {len(valid_df)} valid, "
        f"{len(rejected_df)} rejected ({dup_count} duplicate)"
    )
    return valid_df, rejected_df
