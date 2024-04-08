import aiohttp
from aiohttp import ClientConnectorError


async def is_node_online(url: str, session: aiohttp.ClientSession) -> bool:
    try:
        response = await session.get(f"{url}/is_alive")
    except ClientConnectorError:
        return False
    if response.status != 200:
        return False

    return (await response.json())["alive"]
