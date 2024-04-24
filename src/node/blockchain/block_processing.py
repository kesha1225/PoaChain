import asyncio
import logging

import aiohttp
from fastapi import FastAPI

from chain.block import (
    get_last_block_timestamp,
    get_last_block,
    calculate_block_hash,
    create_block,
    update_transactions_for_block,
)
from chain.constants import MIN_BLOCK_RELEASE_TIME
from chain.timestamps import get_current_accurate_timestamp
from chain.transaction import (
    get_unconfirmed_transactions,
    calculate_block_merkle_root,
    delete_transaction,
)
from chain_config import NodeConfig
from node.api.distributor import send_block_release_notify, send_block_release_created
from node.blockchain.balancer import get_active_ready_nodes
from node.blockchain.validate import validate_transaction
from node.models.block import BlockModel
from node.models.transaction import TransactionModel


async def is_time_for_release():
    current_timestamp = get_current_accurate_timestamp()
    last_block_timestamp = await get_last_block_timestamp()
    time_from_last_block = current_timestamp - last_block_timestamp
    return time_from_last_block >= MIN_BLOCK_RELEASE_TIME


async def get_valid_unconfirmed_transactions() -> list[TransactionModel]:
    unconfirmed_transactions = await get_unconfirmed_transactions()
    valid_unconfirmed_transactions = []

    for unconfirmed_transaction in unconfirmed_transactions:
        is_valid = await validate_transaction(transaction=unconfirmed_transaction)
        if not is_valid:
            await delete_transaction(transaction_id=unconfirmed_transaction.id)
            continue
        valid_unconfirmed_transactions.append(unconfirmed_transaction)

    return valid_unconfirmed_transactions


async def release_block(session: aiohttp.ClientSession):
    unconfirmed_transactions = await get_valid_unconfirmed_transactions()

    last_block = await get_last_block()
    new_block = BlockModel(
        block_number=last_block.block_number + 1,
        previous_hash=last_block.block_hash,
        authority_id=NodeConfig.title_id,
        timestamp=get_current_accurate_timestamp(),
    )

    new_block.merkle_root = calculate_block_merkle_root(
        transactions=unconfirmed_transactions
    )
    new_block.block_hash = calculate_block_hash(block=new_block)

    logging.info(f"releasing block {new_block}")

    await send_block_release_notify(session=session)
    new_block = await create_block(block=new_block)
    await update_transactions_for_block(
        block_id=new_block.id,
        block_number=new_block.block_number,
        transactions=unconfirmed_transactions,
    )
    await send_block_release_created(
        session=session, block=new_block, block_transactions=unconfirmed_transactions
    )


async def process_blocks_forever(app: FastAPI):
    await asyncio.sleep(3)
    session = aiohttp.ClientSession()
    while True:
        await asyncio.sleep(0.1)

        if not await is_time_for_release():
            continue

        active_ready_nodes = await get_active_ready_nodes(session=session)
        if not active_ready_nodes:
            app.is_ready = True
            await release_block(session=session)
            continue

        if not app.is_ready:
            continue

        if not app.is_waiting:
            await release_block(session=session)
            app.is_waiting = True
            continue
