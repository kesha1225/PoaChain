import logging

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from chain.block import (
    get_last_block_previous_hash,
    create_block,
    add_new_blocks_from_node,
    get_blocks_count,
    calculate_block_hash,
)
from chain.db.session import async_session
from chain.transaction import create_transaction
from chain_config import NodeConfig
from node.api.block import get_blocks_until_hash_from_node
from node.blockchain.balancer import get_suitable_node_url
from node.blockchain.validate import validate_transaction, validate_block
from node.models.block import BlockModel
from node.structs.block import BlocksVerifyResult


async def process_latest_blocks(
    session: AsyncSession,
    suitable_node_url: str,
    http_session: aiohttp.ClientSession,
    last_block_previous_hash: str,
) -> BlocksVerifyResult:
    latest_blocks = await get_blocks_until_hash_from_node(
        url=suitable_node_url,
        session=http_session,
        last_block_previous_hash=last_block_previous_hash,
    )

    for block in latest_blocks.blocks:
        if not await validate_block(session=session, block=block):
            return BlocksVerifyResult(
                status=False,
                suitable_node_url=suitable_node_url,
            )

        for transaction in block.transactions:
            if not await validate_transaction(session=session, transaction=transaction):
                return BlocksVerifyResult(
                    status=False,
                    suitable_node_url=suitable_node_url,
                )

            await create_transaction(
                session=session, transaction=transaction, with_commit=False
            )

        await create_block(session=session, block=block, with_commit=False)

    logging.info(f"got {len(latest_blocks.blocks)} new blocks after sync")
    return BlocksVerifyResult(
        status=True, suitable_node_url=suitable_node_url, new_blocks=latest_blocks
    )


async def start_node(session: aiohttp.ClientSession):
    success = False

    bad_urls = []
    while not success:
        suitable_node_url = await get_suitable_node_url(
            session=session, exclude_urls=bad_urls
        )
        logging.info(f"Trying sync with {suitable_node_url}")

        if suitable_node_url is None:
            # мы одни синкать нечего
            logging.info("No suitable node for sync")
            return

        # мы не одни начинаем качать блоки
        last_block_previous_hash = await get_last_block_previous_hash()

        async with async_session() as sql_session:
            # получили все новые блоки с транзакциями
            verify_result = await process_latest_blocks(
                session=sql_session,
                last_block_previous_hash=last_block_previous_hash,
                http_session=session,
                suitable_node_url=suitable_node_url,
            )

            sql_session.expunge_all()

        if verify_result.status:
            await add_new_blocks_from_node(new_blocks=verify_result.new_blocks)
            return

        bad_urls.append(verify_result.suitable_node_url)


async def after_start_node():
    blocks_count = await get_blocks_count()
    if blocks_count > 0:
        return

    genesis_block = BlockModel(
        block_number=1,
        previous_hash="genesis",
        authority_id=NodeConfig.title_id,
        timestamp=1,
    )
    genesis_block.block_hash = calculate_block_hash(block=genesis_block)

    await create_block(block=genesis_block)
