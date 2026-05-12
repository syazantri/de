import os
import logging
from sqlalchemy import create_engine, Engine
from dotenv import load_dotenv

load_dotenv()


def get_db_engine() -> Engine:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    db = os.getenv("POSTGRES_DB", "transactions_db")
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)
