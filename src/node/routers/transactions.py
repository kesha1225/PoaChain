from fastapi import APIRouter
from starlette.requests import Request

from chain.block import get_block_by_hash, get_block_by_number
from chain.transaction import get_transactions_by_address, get_transaction_by_hash, get_transactions_by_block_hash

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


@router.post("/get_transactions_by_block")
async def get_transactions_by_block_handler(request: Request):
    request_data = await request.json()
    block_hash = request_data["block_hash"]

    return {
        "transactions": await get_transactions_by_block_hash(
            block_hash=block_hash
        )
    }


@router.post("/get_transaction")
async def get_transaction_handler(request: Request):
    request_data = await request.json()
    transaction_hash = request_data["transaction_hash"]

    data = await get_transaction_by_hash(transaction_hash=transaction_hash)
    if data is None:
        return {"transaction": None}

    result = data.dict()

    if data.block_number:
        block = await get_block_by_number(block_number=data.block_number)
        result["authority_id"] = block.authority_id
        result["block_number"] = block.block_number
        result["block_hash"] = block.block_hash
    else:
        result["block_number"] = "Не подтверждено."
        result["authority_id"] = "Не подтверждено."
        result["block_hash"] = ""

    return {"transaction": result}
