import os

from dotenv import load_dotenv


load_dotenv(dotenv_path=os.getenv("DOTENV_FILE"))


class PostgresConfig:
    db_url = os.getenv("POSTGRES_URL")
    db_url_alembic = os.getenv("POSTGRES_URL_ALEMBIC")


class WebConfig:
    encryption_key = os.getenv("ENCRYPT_KEY")


class ChainConfig:
    address_prefix = "poa"


class NodeConfig:
    title_id = os.getenv("NODE_ID")
