from sqlalchemy.ext.asyncio import AsyncSession

from chain.block import get_last_block, calculate_block_hash, create_block
from chain.constants import GENESIS_BLOCK_PREVIOUS_HASH
from chain.db.session import db_session
from chain.timestamps import get_current_accurate_timestamp
from chain.transaction import (
    calculate_balance,
    create_transaction,
    calculate_transaction_hash,
)
from node.models.block import BlockModel, NewBlocksModel
from node.models.transaction import TransactionModel
from node.structs.block import BlocksVerifyResult


@db_session
async def validate_transaction(
    session: AsyncSession, transaction: TransactionModel
) -> bool:
    if transaction.transaction_hash != calculate_transaction_hash(
        transaction=transaction
    ):
        return False

    if transaction.sender_address == transaction.recipient_address:
        return False

    if transaction.timestamp > get_current_accurate_timestamp():
        return False

    sender_balance = await calculate_balance(
        session=session, address=transaction.sender_address
    )

    if sender_balance < transaction.amount:
        return False

    return True


@db_session
async def validate_block(session: AsyncSession, block: BlockModel):
    previous_block = await get_last_block(session=session)

    is_genesis = block.previous_hash == GENESIS_BLOCK_PREVIOUS_HASH

    if not is_genesis and block.previous_hash != previous_block.block_hash:
        return False

    if not is_genesis and block.block_number - 1 != previous_block.block_number:
        return False

    if block.timestamp > get_current_accurate_timestamp():
        return False

    if not is_genesis and block.timestamp < previous_block.timestamp:
        return False

    if block.block_hash != calculate_block_hash(block=block):
        return False

    return True


async def validate_block_with_transactions(
    session: AsyncSession,
    block: BlockModel,
) -> BlocksVerifyResult:
    if not await validate_block(session=session, block=block):
        return BlocksVerifyResult(
            status=False,
        )

    for transaction in block.transactions:
        if not await validate_transaction(session=session, transaction=transaction):
            return BlocksVerifyResult(status=False)

        await create_transaction(
            session=session, transaction=transaction, with_commit=False
        )

    await create_block(session=session, block=block, with_commit=False)

    return BlocksVerifyResult(status=True, new_blocks=NewBlocksModel(blocks=[block]))
