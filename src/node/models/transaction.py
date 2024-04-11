import datetime
import hashlib

import pydantic


class TransactionModel(pydantic.BaseModel):
    sender_address: str
    recipient_address: str
    amount: int
    timestamp: int
    transaction_hash: str | None = None
