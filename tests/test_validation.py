import pandas as pd

from src.validate import validate


def make_row(**overrides) -> dict:
    """Return a valid row dict with any fields overridden by keyword args."""
    base = {
        "transaction_id": "TXN001",
        "user_id": "USR001",
        "merchant_id": "MER001",
        "transaction_timestamp": "2024-11-01 08:14:23",
        "amount": "75000.00",
        "currency": "IDR",
        "payment_method": "QRIS",
        "transaction_status": "SUCCESS",
        "created_at": "2024-11-01 08:14:25",
    }
    base.update(overrides)
    return base

def test_valid_row_passes():
    df = pd.DataFrame([make_row()])
    valid, rejected = validate(df)
    assert len(valid) == 1
    assert len(rejected) == 0


def test_multiple_valid_rows():
    rows = [make_row(transaction_id=f"TXN{i:03d}") for i in range(1, 6)]
    df = pd.DataFrame(rows)
    valid, rejected = validate(df)
    assert len(valid) == 5
    assert len(rejected) == 0

def test_null_transaction_id_rejected():
    df = pd.DataFrame([make_row(transaction_id="")])
    valid, rejected = validate(df)
    assert len(valid) == 0
    assert len(rejected) == 1
    assert "transaction_id" in rejected.iloc[0]["error_reason"]


def test_whitespace_only_transaction_id_rejected():
    df = pd.DataFrame([make_row(transaction_id="   ")])
    valid, rejected = validate(df)
    assert len(rejected) == 1


def test_duplicate_transaction_id_second_row_rejected():
    rows = [make_row(transaction_id="TXN001"), make_row(transaction_id="TXN001")]
    df = pd.DataFrame(rows)
    valid, rejected = validate(df)
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicate" in rejected.iloc[0]["error_reason"]

def test_negative_amount_rejected():
    df = pd.DataFrame([make_row(amount="-100.00")])
    valid, rejected = validate(df)
    assert len(valid) == 0
    assert len(rejected) == 1
    assert "amount" in rejected.iloc[0]["error_reason"]

def test_zero_amount_rejected():
    df = pd.DataFrame([make_row(amount="0")])
    valid, rejected = validate(df)
    assert len(rejected) == 1
    assert "amount" in rejected.iloc[0]["error_reason"]

def test_non_numeric_amount_rejected():
    df = pd.DataFrame([make_row(amount="free")])
    valid, rejected = validate(df)
    assert len(rejected) == 1
    assert "amount" in rejected.iloc[0]["error_reason"]

def test_null_currency_rejected():
    df = pd.DataFrame([make_row(currency="")])
    valid, rejected = validate(df)
    assert len(valid) == 0
    assert len(rejected) == 1
    assert "currency" in rejected.iloc[0]["error_reason"]

# transaction_timestamp checks
def test_invalid_timestamp_rejected():
    df = pd.DataFrame([make_row(transaction_timestamp="not-a-date")])
    valid, rejected = validate(df)
    assert len(valid) == 0
    assert len(rejected) == 1
    assert "transaction_timestamp" in rejected.iloc[0]["error_reason"]

def test_valid_iso_timestamp_accepted():
    df = pd.DataFrame([make_row(transaction_timestamp="2024-01-15T10:30:00")])
    valid, rejected = validate(df)
    assert len(valid) == 1

def test_invalid_status_rejected():
    df = pd.DataFrame([make_row(transaction_status="DECLINED")])
    valid, rejected = validate(df)
    assert len(valid) == 0
    assert len(rejected) == 1
    assert "transaction_status" in rejected.iloc[0]["error_reason"]

def test_valid_statuses_accepted():
    for status in ["SUCCESS", "FAILED", "PENDING"]:
        df = pd.DataFrame([make_row(transaction_id=f"TXN_{status}", transaction_status=status)])
        valid, rejected = validate(df)
        assert len(valid) == 1, f"Expected {status} to be valid"

def test_case_insensitive_status():
    df = pd.DataFrame([make_row(transaction_status="success")])
    valid, rejected = validate(df)
    assert len(valid) == 1

def test_row_with_multiple_errors():
    df = pd.DataFrame([make_row(amount="-50", currency="", transaction_status="EXPIRED")])
    valid, rejected = validate(df)
    assert len(rejected) == 1
    reason = rejected.iloc[0]["error_reason"]
    assert "amount" in reason
    assert "currency" in reason
    assert "transaction_status" in reason
