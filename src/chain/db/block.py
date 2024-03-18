import hashlib
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Block(Base):
    __tablename__ = "block"

    id = Column(Integer, primary_key=True)
    block_number = Column(Integer, unique=True, nullable=False)

    block_hash = Column(String, unique=True, nullable=False)
    previous_hash = Column(String, unique=True, nullable=False)
    nonce = Column(String, unique=True, nullable=False)
    merkle_root = Column(String, unique=True, nullable=False)

    timestamp = Column(DateTime, nullable=False)

    transactions = relationship("Transaction", back_populates="block")

    def calculate_merkle_root(self):
        merkle_tree = [tx.transaction_hash for tx in self.transactions]
        while len(merkle_tree) > 1:
            merkle_tree = [
                hashlib.sha256(
                    merkle_tree[i].encode() + merkle_tree[i + 1].encode()
                ).hexdigest()
                for i in range(0, len(merkle_tree), 2)
            ]
        self.merkle_root = merkle_tree[0]

    def calculate_block_hash(self) -> str:
        block_data = f"{self.block_number}{self.previous_hash}{self.nonce}{self.merkle_root}{self.timestamp}"
        return hashlib.sha256(block_data.encode()).hexdigest()