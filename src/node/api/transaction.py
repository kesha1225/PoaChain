import aiohttp
from aiohttp import ClientConnectorError


async def send_transaction_to_mempool(
    url: str, session: aiohttp.ClientSession, transaction_data: str
) -> bool:
    try:
        response = await session.post(f"{url}/mempool", json={"data": transaction_data})
    except ClientConnectorError:
        return False
    if response.status != 200:
        return False

    return await response.json()


async def get_transactions_from_node(
    url: str, session: aiohttp.ClientSession, address: str, transaction_type: str
) -> dict:
    try:
        response = await session.post(
            f"{url}/get_transactions",
            json={"address": address, "transaction_type": transaction_type},
        )
    except ClientConnectorError:
        return {"transactions": []}
    if response.status != 200:
        return {"transactions": []}

    return await response.json()


async def get_transactions_by_block_from_node(
    url: str, session: aiohttp.ClientSession, block_hash: str
) -> dict:
    try:
        response = await session.post(
            f"{url}/get_transactions_by_block",
            json={"block_hash": block_hash},
        )
    except ClientConnectorError:
        return {"transactions": []}
    if response.status != 200:
        return {"transactions": []}

    return await response.json()


async def get_transaction_from_node(
    url: str, session: aiohttp.ClientSession, transaction_hash: str
) -> dict:
    try:
        response = await session.post(
            f"{url}/get_transaction",
            json={"transaction_hash": transaction_hash},
        )
    except ClientConnectorError:
        return {"transaction": None}
    if response.status != 200:
        return {"transaction": None}

    return await response.json()
