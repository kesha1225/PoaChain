import dataclasses
import logging

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from chain.block import (
    get_last_block_previous_hash,
    create_block,
    add_new_blocks_from_node,
)
from chain.db.session import async_session
from chain.transaction import create_transaction
from node.api.block import get_blocks_until_hash_from_node
from node.blockchain.balancer import get_suitable_node_url
from node.blockchain.validate import validate_transaction, validate_block
from node.models.block import NewBlocksModel


@dataclasses.dataclass
class BlocksVerifyResult:
    status: bool
    suitable_node_url: str
    bad_block_hash: str | None = None
    new_blocks: NewBlocksModel | None = None


async def process_latest_blocks(
    session: AsyncSession,
    suitable_node_url: str,
    http_session: aiohttp.ClientSession,
    last_block_previous_hash: str,
    bad_hashes: list[str],
) -> BlocksVerifyResult:
    latest_blocks = await get_blocks_until_hash_from_node(
        url=suitable_node_url,
        session=http_session,
        last_block_previous_hash=last_block_previous_hash,
    )

    for block in latest_blocks.blocks:
        if block.block_hash in bad_hashes:
            return BlocksVerifyResult(
                status=False,
                suitable_node_url=suitable_node_url,
                bad_block_hash=block.block_hash,
            )

        if not await validate_block(session=session, block=block):
            return BlocksVerifyResult(
                status=False,
                suitable_node_url=suitable_node_url,
                bad_block_hash=block.block_hash,
            )

        for transaction in block.transactions:
            if not await validate_transaction(session=session, transaction=transaction):
                return BlocksVerifyResult(
                    status=False,
                    suitable_node_url=suitable_node_url,
                    bad_block_hash=block.block_hash,
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
    bad_hashes = []
    while not success:
        suitable_node_url = await get_suitable_node_url(
            session=session, exclude_urls=bad_urls
        )

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
                bad_hashes=bad_hashes,
            )

            sql_session.expunge_all()

        if verify_result.status:
            await add_new_blocks_from_node(new_blocks=verify_result.new_blocks)
            return

        bad_hashes.append(verify_result.bad_block_hash)
        bad_urls.append(verify_result.suitable_node_url)


# todo: проверить с третьей нодой что она одну заьракует а с третьей синк