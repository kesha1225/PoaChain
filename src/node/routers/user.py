from fastapi import APIRouter
from starlette.requests import Request

from chain.transaction import calculate_balance

router = APIRouter()


@router.post("/get_balance")
async def get_balance_handler(request: Request):
    address = (await request.json())["address"]

    balance = await calculate_balance(address=address)
    if balance == float("inf"):
        balance = "ЭМИССИОНЕР"
    return {"balance": balance}
