import datetime
import hashlib

import pydantic


class TransactionModel(pydantic.BaseModel):
    sender_address: str
    recipient_address: str
    amount: int
    timestamp: int
    transaction_hash: str | None = None

    def generate_transaction_hash(self) -> str:
        transaction_str = (
            f"{self.sender_address}{self.recipient_address}"
            f"{self.amount}{self.timestamp}"
        )
        return hashlib.sha256(transaction_str.encode()).hexdigest()
