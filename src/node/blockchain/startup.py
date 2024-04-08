import logging

import aiohttp

from chain.block import get_last_block_previous_hash, add_new_blocks_from_node
from node.api.block import get_blocks_until_hash_from_node
from node.blockchain.balancer import get_suitable_node_url


async def start_node(session: aiohttp.ClientSession):
    suitable_node_url = await get_suitable_node_url(session=session)

    if suitable_node_url is None:
        # мы одни синкать нечего
        logging.info("No suitable node for sync")
        return

    # мы не одни начинаем качать блоки
    last_block_previous_hash = await get_last_block_previous_hash()

    # получили все новые блоки с транзакциями
    latest_blocks = await get_blocks_until_hash_from_node(
        url=suitable_node_url,
        session=session,
        last_block_previous_hash=last_block_previous_hash,
    )

    logging.info(f"got {len(latest_blocks.blocks)} new blocks after sync")

    await add_new_blocks_from_node(new_blocks=latest_blocks)
