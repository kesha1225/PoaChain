from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from chain.constants import GENESIS_BLOCK_PREVIOUS_HASH, NO_BLOCK_PREVIOUS_HASH
from chain.db import Block
from chain.db.session import db_session
from chain.transaction import create_transaction
from node.models.block import NewBlocksModel, BlockModel


@db_session
async def get_last_block(session: AsyncSession) -> Block | None:
    last_block = (
        await session.execute(
            select(Block).order_by(Block.block_number.desc()).limit(1)
        )
    ).first()

    if last_block is None:
        return None

    return last_block[0]


@db_session
async def get_last_block_number(session: AsyncSession) -> int:
    last_block = await get_last_block(session=session)
    if last_block is None:
        return -1

    return last_block.block_number


@db_session
async def get_last_block_timestamp(session: AsyncSession) -> int:
    last_block = await get_last_block(session=session)
    if last_block is None:
        return -1

    return last_block.block_number


async def get_last_block_previous_hash() -> str:
    last_block = await get_last_block()

    if last_block is None:
        return NO_BLOCK_PREVIOUS_HASH

    return last_block.previous_hash


@db_session
async def get_blocks_until_previous_hash(
    session: AsyncSession, last_block_previous_hash: str
) -> list[Block]:
    last_block = await get_last_block()

    blocks = []
    while last_block_previous_hash != last_block.previous_hash:
        blocks.append(last_block)

        last_block = (
            await session.execute(
                select(Block).where(Block.block_hash == last_block.previous_hash)
            )
        ).fetchone()

        if last_block is None:
            break

        last_block = last_block[0]

    return list(reversed(blocks))


@db_session
async def create_block(
    session: AsyncSession, block: BlockModel, with_commit: bool = True
) -> Block:
    new_block = Block(
        block_number=block.block_number,
        block_hash=block.block_hash,
        previous_hash=block.previous_hash,
        merkle_root=block.merkle_root,
        authority_id=block.authority_id,
        timestamp=block.timestamp,
    )

    session.add(new_block)

    if with_commit:
        await session.commit()

    return new_block


async def add_new_blocks_from_node(
    new_blocks: NewBlocksModel, with_commit: bool = True
) -> None:
    for block in new_blocks.blocks:
        new_block = await create_block(block=block, with_commit=with_commit)

        for transaction in block.transactions:
            await create_transaction(
                transaction=transaction, block_id=new_block.id, with_commit=with_commit
            )
