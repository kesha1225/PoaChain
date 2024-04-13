from fastapi import APIRouter
from starlette.requests import Request

from chain.timestamps import get_current_accurate_timestamp
from chain.transaction import calculate_balance, create_transaction
from crypto.converter import expand_transaction_from_request, normalize_transaction
from crypto.sign import verify_transaction_sign


router = APIRouter()


@router.post("/mempool")
async def add_to_mempool_handler(request: Request):
    transaction_data = normalize_transaction((await request.json())["data"])

    is_valid = verify_transaction_sign(transaction=transaction_data)

    if not is_valid:
        return {
            "status": False,
            "code": "Bad signature",
            "description": "Неверная подпись",
        }

    transaction_model = expand_transaction_from_request(transaction=transaction_data)

    if transaction_model.amount < 1:
        return {
            "status": False,
            "code": "Bad amount",
            "description": "Слишком маленькая сумма.",
        }

    if transaction_model.sender_address == transaction_model.recipient_address:
        return {
            "status": False,
            "code": "Bad address",
            "description": "Нельзя отправить монеты самому себе.",
        }

    sender_balance = await calculate_balance(
        address=transaction_model.sender_address,
        exclude_hash=transaction_model.transaction_hash,
    )

    if sender_balance < transaction_model.amount:
        return {
            "status": False,
            "code": "Insufficient funds",
            "description": "Недостаточно средств.",
        }

    if transaction_model.timestamp > get_current_accurate_timestamp():
        return {
            "status": False,
            "code": "Invalid timestamp",
            "description": "Ошибка. Транзакция из будущего.",
        }

    await create_transaction(transaction=transaction_model)
    return {"status": True, "hash": transaction_model.transaction_hash}
