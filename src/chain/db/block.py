import hashlib
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from .transaction import Transaction
from .base import Base


class Block(Base):
    __tablename__ = "block"

    id = Column(Integer, primary_key=True)
    block_number = Column(Integer, unique=True, nullable=False)

    block_hash = Column(String, unique=True, nullable=False)
    previous_hash = Column(String, unique=True, nullable=False)
    merkle_root = Column(String, unique=True, nullable=True)
    authority_id = Column(String, nullable=False)

    timestamp = Column(BigInteger, nullable=False)

    transactions = relationship("Transaction", back_populates="block")

    def to_dict(self, transactions: list[Transaction]) -> dict:
        return {
            "block_number": self.block_number,
            "block_hash": self.block_hash,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "authority_id": self.authority_id,
            "timestamp": self.timestamp,
            "transactions": [transaction.to_dict() for transaction in transactions],
        }
