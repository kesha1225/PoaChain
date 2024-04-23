import aiohttp
from aiohttp import ClientConnectorError

from node.models.block import NewBlocksModel


async def get_last_block_number_from_node(
    url: str, session: aiohttp.ClientSession
) -> int:
    response = await session.get(f"{url}/get_last_block_number")

    if response.status != 200:
        return -1

    return (await response.json())["last_block_number"]


async def get_blocks_until_hash_from_node(
    url: str, session: aiohttp.ClientSession, last_block_previous_hash: str
) -> NewBlocksModel:
    response = await session.post(
        f"{url}/get_blocks_until_hash",
        json={"last_block_previous_hash": last_block_previous_hash},
    )

    if response.status != 200:
        return NewBlocksModel(blocks=[])

    return NewBlocksModel(**await response.json())


async def get_blocks_from_node(
    url: str, session: aiohttp.ClientSession, limit: int, offset: int
) -> NewBlocksModel:
    response = await session.post(
        f"{url}/get_blocks",
        params={"limit": limit, "offset": offset},
    )

    if response.status != 200:
        return NewBlocksModel(blocks=[])

    return NewBlocksModel(**await response.json())


async def get_block_from_node(
    url: str, session: aiohttp.ClientSession, block_hash: str
) -> dict:
    try:
        response = await session.post(
            f"{url}/get_block",
            json={"block_hash": block_hash},
        )
    except ClientConnectorError:
        return {"block": None}
    if response.status != 200:
        return {"block": None}

    return await response.json()
