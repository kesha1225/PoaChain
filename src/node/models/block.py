import datetime
import hashlib

import pydantic

from node.models.transaction import TransactionModel


class BlockModel(pydantic.BaseModel):
    block_number: int
    block_hash: str
    previous_hash: str
    merkle_root: str
    authority_id: str
    timestamp: int
    transactions: list[TransactionModel]

    def calculate_block_hash(self) -> str:
        block_data = (
            f"{self.block_number}{self.previous_hash}{self.authority_id}"
            f"{self.merkle_root}{self.timestamp}"
        )
        return hashlib.sha256(block_data.encode()).hexdigest()


class NewBlocksModel(pydantic.BaseModel):
    blocks: list[BlockModel]
