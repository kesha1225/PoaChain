import asyncio

from chain.transaction import create_transaction

res = asyncio.run(
    create_transaction(
        sender_address="from",
        recipient_address="to",
        amount=100,
    )
)

print(res)
