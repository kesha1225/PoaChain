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
