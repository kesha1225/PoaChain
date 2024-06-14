import aiohttp


def key_builder_is_alive(url: str, session: aiohttp.ClientSession) -> str | None:
    return f"is_node_online_{url}"


def key_builder_is_ready(url: str, session: aiohttp.ClientSession) -> str | None:
    return f"is_node_ready_{url}"


def key_builder_get_transactions_from_node(
    url: str, session: aiohttp.ClientSession, address: str, transaction_type: str
) -> str | None:
    return f"get_transactions_from_node_{url}_{address}_{transaction_type}"
