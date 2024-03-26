from sqlalchemy import Column, BIGINT, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_address = Column(String, nullable=False, index=True)
    recipient_address = Column(String, nullable=False, index=True)
    amount = Column(BIGINT, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"))
    block = relationship("Block", back_populates="transactions")
