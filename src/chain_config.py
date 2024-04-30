import os

from dotenv import load_dotenv

from node_constants import ALL_NODES

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
    private_key = os.getenv("PRIVATE_KEY")
    money_issuer_address = (
        "poa1pvffe3vy778xaqlmen8frhnsz00yl385hq756uyypndy2q2ya7wstxsuym"
    )
    block_notify_message = "notify_about_block_{random_data}"
