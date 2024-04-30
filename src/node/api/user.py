import aiohttp
from aiohttp import ClientConnectorError


async def get_address_balance(
    url: str, session: aiohttp.ClientSession, address: str
) -> bool:
    try:
        response = await session.post(f"{url}/get_balance", json={"address": address})
    except ClientConnectorError:
        return False
    if response.status != 200:
        return False

    return (await response.json())["balance"]
