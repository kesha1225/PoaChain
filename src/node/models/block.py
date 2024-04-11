import pydantic

from chain.db import Block
from node.models.transaction import TransactionModel


class BlockModel(pydantic.BaseModel):
    block_number: int
    block_hash: str | None = None
    previous_hash: str
    merkle_root: str | None = None
    authority_id: str
    timestamp: int
    transactions: list[TransactionModel] | None = None


class NewBlocksModel(pydantic.BaseModel):
    blocks: list[BlockModel]
