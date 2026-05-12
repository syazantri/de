import argparse
import uuid

from src.extract import extract_from_csv
from src.load import load_rejected, load_valid, log_pipeline_run
from src.monitor import print_pipeline_report
from src.transform import transform
from src.utils import get_logger
from src.validate import validate

logger = get_logger("pipeline")


def run(input_file: str) -> str:
    run_id = str(uuid.uuid4())[:8]
    logger.info(f"Starting pipeline run {run_id} | input={input_file}")

    status = "SUCCESS"
    error_msg = None
    total = valid_count = rejected_count = dup_count = 0

    try:
        raw_df = extract_from_csv(input_file)
        total = len(raw_df)

        valid_df, rejected_df = validate(raw_df)

        dup_count = (
            int(rejected_df["error_reason"].str.contains("duplicate", na=False).sum())
            if not rejected_df.empty
            else 0
        )

        clean_df = transform(valid_df)

        valid_count = load_valid(clean_df)
        rejected_count = load_rejected(rejected_df)

        if not rejected_df.empty:
            out_path = f"data/processed/rejected_{run_id}.csv"
            rejected_df.to_csv(out_path, index=False)
            logger.info(f"Rejected records saved to {out_path}")

    except Exception as exc:
        status = "FAILED"
        error_msg = str(exc)
        logger.error(f"Pipeline failed: {exc}")

    log_pipeline_run(
        run_id=run_id,
        source_file=input_file,
        total=total,
        valid=valid_count,
        rejected=rejected_count,
        duplicates=dup_count,
        status=status,
        error_msg=error_msg,
    )

    print_pipeline_report()
    return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transaction Data Pipeline")
    parser.add_argument(
        "--input",
        default="data/raw/transactions_sample.csv",
        help="Path to the raw transaction CSV (default: data/raw/transactions_sample.csv)",
    )
    args = parser.parse_args()
    run(args.input)
