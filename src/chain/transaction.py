import hashlib
import logging

from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_, or_

from chain.db import Transaction, Block
from chain.db.session import db_session
from chain_config import NodeConfig
from node.models.transaction import TransactionModel


@db_session
async def create_transaction(
    session: AsyncSession,
    transaction: TransactionModel,
    block_id: int | None = None,
    block_number: int | None = None,
    with_commit: bool = True,
) -> Transaction:
    new_transaction = Transaction(
        sender_address=transaction.sender_address,
        recipient_address=transaction.recipient_address,
        amount=transaction.amount,
        timestamp=transaction.timestamp,
        transaction_hash=transaction.transaction_hash,
        block_id=block_id,
        block_number=block_number,
    )
    session.add(new_transaction)

    if with_commit:
        await session.commit()

    return new_transaction


@db_session
async def calculate_balance(
    session: AsyncSession, address: str, exclude_hash: str | None = None
) -> int | float:
    if address == NodeConfig.money_issuer_address:
        return float("inf")

    sent_amount_query = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.sender_address == address,
            Transaction.transaction_hash != exclude_hash,
        ),
    )
    sent_amount = await session.scalar(sent_amount_query)

    received_amount_query = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.recipient_address == address,
            Transaction.transaction_hash != exclude_hash,
        ),
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
async def get_unconfirmed_transactions(session: AsyncSession) -> list[TransactionModel]:
    unconfirmed_transactions = (
        await session.execute(select(Transaction).where(Transaction.block_id.is_(None)))
    ).fetchall()

    return [transaction[0] for transaction in unconfirmed_transactions]


@db_session
async def get_transactions_by_address(
    session: AsyncSession, address: str, transactions_type: str
) -> list[TransactionModel]:

    if transactions_type == "all":
        query = or_(
            Transaction.sender_address == address,
            Transaction.recipient_address == address,
        )
    elif transactions_type == "from":
        query = Transaction.sender_address == address
    else:
        query = Transaction.recipient_address == address

    transactions = (
        await session.execute(
            select(Transaction).where(query).order_by(Transaction.timestamp)
        )
    ).fetchall()
    return [transaction[0] for transaction in transactions]


@db_session
async def get_transactions_by_block_hash(
    session: AsyncSession, block_hash: str
) -> list[TransactionModel]:

    block = (
        await session.execute(select(Block).where(Block.block_hash == block_hash))
    ).first()

    if block is None:
        return []

    transactions = (
        await session.execute(
            select(Transaction).where(Transaction.block_number == block[0].block_number)
        )
    ).fetchall()
    return [transaction[0] for transaction in transactions]


@db_session
async def get_transaction_by_hash(
    session: AsyncSession, transaction_hash: str
) -> TransactionModel | None:

    transaction = (
        await session.execute(
            select(Transaction).where(Transaction.transaction_hash == transaction_hash)
        )
    ).fetchone()

    if transaction is None:
        return

    transaction = transaction[0]

    return transaction


@db_session
async def delete_transaction(session: AsyncSession, transaction_id: int) -> None:
    await session.execute(delete(Transaction).where(Transaction.id == transaction_id))
    await session.commit()


def calculate_block_merkle_root(
    transactions: list[Transaction | TransactionModel],
) -> str | None:
    merkle_tree = [tx.transaction_hash for tx in transactions]

    while len(merkle_tree) > 1:
        new_level = []
        for i in range(0, len(merkle_tree), 2):
            left = merkle_tree[i]
            right = merkle_tree[i + 1] if i + 1 < len(merkle_tree) else merkle_tree[i]
            new_hash = hashlib.sha256(left.encode() + right.encode()).hexdigest()
            new_level.append(new_hash)
        merkle_tree = new_level

    return merkle_tree[0] if merkle_tree else None


def calculate_transaction_hash(transaction: Transaction | TransactionModel) -> str:
    transaction_str = (
        f"{transaction.sender_address}{transaction.recipient_address}"
        f"{transaction.amount}{transaction.timestamp}"
    )
    return hashlib.sha256(transaction_str.encode()).hexdigest()
