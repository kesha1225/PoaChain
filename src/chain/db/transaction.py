from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_address = Column(String, nullable=False)
    recipient_address = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    block_id = Column(Integer, ForeignKey("block.id"))
    block = relationship("Block", back_populates="transactions")
