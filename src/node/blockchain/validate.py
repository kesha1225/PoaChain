import time

from sqlalchemy.ext.asyncio import AsyncSession

from chain.block import get_last_block_timestamp, get_last_block, calculate_block_hash
from chain.constants import GENESIS_BLOCK_PREVIOUS_HASH
from chain.db.session import db_session
from chain.transaction import calculate_balance
from node.models.block import BlockModel
from node.models.transaction import TransactionModel


async def validate_transaction(
    session: AsyncSession, transaction: TransactionModel
) -> bool:
    if transaction.transaction_hash != transaction.generate_transaction_hash():
        return False

    if transaction.sender_address == transaction.recipient_address:
        return False

    if transaction.timestamp > int(time.time()):
        return False

    sender_balance = await calculate_balance(
        session=session, address=transaction.sender_address
    )

    if sender_balance < transaction.amount:
        return False

    last_block_timestamp = await get_last_block_timestamp(session=session)

    if last_block_timestamp != -1 and last_block_timestamp > transaction.timestamp:
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

    if block.timestamp > int(time.time()):
        return False

    if not is_genesis and block.timestamp < previous_block.timestamp:
        return False

    if block.block_hash != calculate_block_hash(block=block):
        return False

    return True
