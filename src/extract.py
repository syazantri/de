import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)


def extract_from_csv(filepath: str) -> pd.DataFrame:
    logger.info(f"Reading data from {filepath}")
    df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    logger.info(f"Loaded {len(df)} rows from {filepath}")
    return df
