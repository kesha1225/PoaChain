import hashlib
import logging
import traceback

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from chain.constants import NO_BLOCK_PREVIOUS_HASH
from chain.db import Block, Transaction
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
async def get_block_by_hash(session: AsyncSession, block_hash: str) -> Block | None:
    block = (
        await session.execute(select(Block).where(Block.block_hash == block_hash))
    ).first()

    if block is None:
        return None

    return block[0]


@db_session
async def get_block_by_number(session: AsyncSession, block_number: int) -> Block | None:
    block = (
        await session.execute(
            select(Block).where(Block.block_number == int(block_number))
        )
    ).first()

    if block is None:
        return None

    return block[0]


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

    return last_block.timestamp


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

    try:
        if with_commit:
            await session.commit()
    except Exception as e:
        logging.error(f"error block {traceback.format_exc()}")
        return new_block

    return new_block


async def add_new_blocks_from_node(
    new_blocks: NewBlocksModel, with_commit: bool = True
) -> None:
    for block in new_blocks.blocks:
        new_block = await create_block(block=block, with_commit=with_commit)

        for transaction in block.transactions:
            await create_transaction(
                transaction=transaction,
                block_id=new_block.id,
                block_number=new_block.block_number,
                with_commit=with_commit,
            )


def calculate_block_hash(block: BlockModel) -> str:
    block_data = (
        f"{block.block_number}{block.previous_hash}{block.authority_id}"
        f"{block.merkle_root}{block.timestamp}"
    )
    return hashlib.sha256(block_data.encode()).hexdigest()


@db_session
async def update_transactions_for_block(
    session: AsyncSession,
    block_id: int,
    block_number: int,
    transactions: list[Transaction],
) -> None:
    await session.execute(
        update(Transaction)
        .values(block_id=block_id, block_number=block_number)
        .where(Transaction.id.in_([transaction.id for transaction in transactions]))
    )

    await session.commit()


@db_session
async def get_blocks(session: AsyncSession, limit: int, offset: int) -> list[Block]:
    last_blocks = await session.execute(
        select(Block).order_by(-Block.block_number).offset(offset).limit(limit)
    )

    return list(reversed([block[0] for block in last_blocks.all()]))


@db_session
async def get_blocks_count(session: AsyncSession) -> int:
    all_blocks = await session.execute(select(func.count()).select_from(Block))
    return all_blocks.scalar()
