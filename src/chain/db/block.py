import hashlib
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Block(Base):
    __tablename__ = "block"

    id = Column(Integer, primary_key=True)
    block_number = Column(Integer, unique=True, nullable=False)
    previous_hash = Column(String, nullable=False)
    nonce = Column(String, nullable=False)
    merkle_root = Column(String, nullable=False)
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
