"""initial

Revision ID: 7477f995b497
Revises: 
Create Date: 2024-03-26 13:48:15.091904

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7477f995b497"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "block",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("block_number", sa.Integer(), nullable=False),
        sa.Column("block_hash", sa.String(), nullable=False),
        sa.Column("previous_hash", sa.String(), nullable=False),
        sa.Column("nonce", sa.String(), nullable=False),
        sa.Column("merkle_root", sa.String(), nullable=False),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("block_hash"),
        sa.UniqueConstraint("block_number"),
        sa.UniqueConstraint("merkle_root"),
        sa.UniqueConstraint("nonce"),
        sa.UniqueConstraint("previous_hash"),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_address", sa.String(), nullable=False),
        sa.Column("recipient_address", sa.String(), nullable=False),
        sa.Column("amount", sa.DECIMAL(precision=2), nullable=False),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.Column("transaction_hash", sa.String(), nullable=False),
        sa.Column("block_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["block_id"],
            ["block.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transaction_hash"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("block")
    # ### end Alembic commands ###
