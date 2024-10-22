from sqlalchemy import Column, BIGINT, String, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_address = Column(String, nullable=False, index=True)
    recipient_address = Column(String, nullable=False, index=True)
    amount = Column(BIGINT, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"))
    block_number = Column(Integer)
    block = relationship("Block", back_populates="transactions")

    def dict(self) -> dict:
        return {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "transaction_hash": self.transaction_hash,
        }
