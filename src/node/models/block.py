import datetime

import pydantic

from node.models.transaction import TransactionModel


class BlockModel(pydantic.BaseModel):
    block_number: int
    block_hash: str
    previous_hash: str
    merkle_root: str
    authority_id: str
    timestamp: datetime.datetime
    transactions: list[TransactionModel]


class NewBlocksModel(pydantic.BaseModel):
    blocks: list[BlockModel]
