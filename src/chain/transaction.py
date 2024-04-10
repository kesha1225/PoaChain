import hashlib

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from chain.db import Transaction
from chain.db.session import db_session
from chain_config import NodeConfig
from node.models.transaction import TransactionModel


@db_session
async def create_transaction(
    session: AsyncSession,
    transaction: TransactionModel,
    block_id: int | None = None,
    with_commit: bool = True,
) -> Transaction:
    new_transaction = Transaction(
        sender_address=transaction.sender_address,
        recipient_address=transaction.recipient_address,
        amount=transaction.amount,
        timestamp=transaction.timestamp,
        transaction_hash=transaction.transaction_hash,
        block_id=block_id,
    )
    session.add(new_transaction)

    if with_commit:
        await session.commit()

    return new_transaction


@db_session
async def calculate_balance(session: AsyncSession, address: str) -> int | float:
    if address == NodeConfig.MONEY_ISSUER_ADDRESS:
        return float("inf")

    sent_amount_query = select(func.sum(Transaction.amount)).where(
        Transaction.sender_address == address
    )
    sent_amount = await session.scalar(sent_amount_query)

    received_amount_query = select(func.sum(Transaction.amount)).where(
        Transaction.recipient_address == address
    )
    received_amount = await session.scalar(received_amount_query)

    balance = (received_amount or 0) - (sent_amount or 0)

    return balance


@db_session
async def get_block_transactions(
    session: AsyncSession, block_id: int
) -> list[Transaction]:
    block_transactions = (
        await session.execute(
            select(Transaction).where(Transaction.block_id == block_id)
        )
    ).fetchall()

    return [transaction[0] for transaction in block_transactions]


@db_session
async def get_unconfirmed_transactions(session: AsyncSession) -> list[Transaction]:
    unconfirmed_transactions = (
        await session.execute(select(Transaction).where(Transaction.block_id.is_(None)))
    ).fetchall()

    return [transaction[0] for transaction in unconfirmed_transactions]


def calculate_block_merkle_root(transactions: list[Transaction]) -> str | None:
    merkle_tree = [tx.transaction_hash for tx in transactions]
    while len(merkle_tree) > 1:
        merkle_tree = [
            hashlib.sha256(
                merkle_tree[i].encode() + merkle_tree[i + 1].encode()
            ).hexdigest()
            for i in range(0, len(merkle_tree), 2)
        ]

    return merkle_tree[0] if merkle_tree else None
