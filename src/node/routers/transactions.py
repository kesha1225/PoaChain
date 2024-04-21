from fastapi import APIRouter
from starlette.requests import Request

from chain.transaction import get_transactions_by_address, get_transaction_by_hash

router = APIRouter()


@router.post("/get_transactions")
async def get_transactions_handler(request: Request):
    request_data = await request.json()
    address = request_data["address"]
    transactions_type = request_data["transaction_type"]

    return {
        "transactions": await get_transactions_by_address(
            address=address, transactions_type=transactions_type
        )
    }


@router.post("/get_transaction")
async def get_transaction_handler(request: Request):
    request_data = await request.json()
    transaction_hash = request_data["transaction_hash"]

    return {
        "transaction": await get_transaction_by_hash(transaction_hash=transaction_hash)
    }
