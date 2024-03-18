import datetime
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession

from chain.db import Transaction
from chain.db.session import db_session


def generate_transaction_hash(transaction: Transaction) -> str:
    transaction_str = (
        f"{transaction.sender_address}{transaction.recipient_address}"
        f"{transaction.amount}{transaction.timestamp}"
    )
    return hashlib.sha256(transaction_str.encode()).hexdigest()


@db_session
async def create_transaction(
    session: AsyncSession, sender_address: str, recipient_address: str, amount: int
) -> Transaction:
    new_transaction = Transaction(
        sender_address=sender_address,
        recipient_address=recipient_address,
        amount=amount,
        timestamp=datetime.datetime.now(),
    )
    new_transaction.transaction_hash = generate_transaction_hash(transaction=new_transaction)

    session.add(new_transaction)

    await session.commit()

    return new_transaction
