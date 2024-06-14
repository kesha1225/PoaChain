import logging

import aiohttp
from aiohttp import ClientConnectorError
from aiocache import cached

from node.cache import key_builder_is_alive, key_builder_is_ready
from node.constants import REQUEST_TTL


@cached(ttl=REQUEST_TTL, key_builder=key_builder_is_alive)
async def is_node_online(url: str, session: aiohttp.ClientSession) -> bool:
    try:
        response = await session.get(f"{url}/is_alive")
    except ClientConnectorError:
        return False
    except Exception as e:
        logging.error(f"bad conn to {url}/is_alive {e}")
        return False
    if response.status != 200:
        return False

    return (await response.json())["alive"]


@cached(ttl=REQUEST_TTL, key_builder=key_builder_is_ready)
async def is_node_ready(url: str, session: aiohttp.ClientSession) -> bool:
    try:
        response = await session.get(f"{url}/is_ready")
    except ClientConnectorError:
        return False
    except Exception as e:
        logging.error(f"bad conn to {url}/is_ready {e}")
        return False
    if response.status != 200:
        return False

    return (await response.json())["is_ready"]
