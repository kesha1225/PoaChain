import aiohttp

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
