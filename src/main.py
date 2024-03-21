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


# todo: функция валидации блока
# todo: если блоков нет то создавать генезис блок
# todo: валидация транзакции
# todo: docker (база, блокчейн, веб)