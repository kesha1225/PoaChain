import asyncio
import logging
import time

import aiohttp

from chain.block import get_last_block_timestamp, get_last_block, calculate_block_hash, create_block
from chain.constants import MIN_BLOCK_RELEASE_TIME
from chain.db import Block
from chain.transaction import get_unconfirmed_transactions, calculate_block_merkle_root
from chain_config import NodeConfig
from node.blockchain.balancer import get_active_nodes
from node.blockchain.validate import validate_block
from node.models.block import BlockModel


async def is_time_for_release():
    current_timestamp = int(time.time())
    last_block_timestamp = await get_last_block_timestamp()
    time_from_last_block = current_timestamp - last_block_timestamp
    return time_from_last_block >= MIN_BLOCK_RELEASE_TIME


async def release_block():
    unconfirmed_transactions = await get_unconfirmed_transactions()

    last_block = await get_last_block()
    new_block = BlockModel(
        block_number=last_block.block_number + 1,
        previous_hash=last_block.block_hash,
        authority_id=NodeConfig.title_id,
        timestamp=int(time.time())
    )

    new_block.block_hash = calculate_block_hash(block=new_block)
    new_block.merkle_root = calculate_block_merkle_root(transactions=unconfirmed_transactions)

    print(await validate_block(block=new_block))
    logging.info(f"releasing block {new_block}")
    return await create_block(block=new_block)


async def process_blocks_forever():
    # todo: мб в начало задержку чтобы успеть получать блоки от других
    session = aiohttp.ClientSession()

    while True:
        await asyncio.sleep(0.1)

        if not await is_time_for_release():
            continue

        active_nodes_count = len(await get_active_nodes(session=session))

        if not active_nodes_count:
            await release_block()
