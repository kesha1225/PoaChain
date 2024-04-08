import datetime

import pydantic


class TransactionModel(pydantic.BaseModel):
    sender_address: str
    recipient_address: str
    amount: int
    timestamp: datetime.datetime
    transaction_hash: str
