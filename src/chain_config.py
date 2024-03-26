import os

from dotenv import load_dotenv


load_dotenv()


class PostgresConfig:
    db_url = os.getenv("POSTGRES_URL")
    db_url_alembic = os.getenv("POSTGRES_URL_ALEMBIC")


class WebConfig:
    encryption_key = os.getenv("ENCRYPT_KEY")


class ChainConfig:
    address_prefix = "poa"
