from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from chain.transaction import calculate_balance
from web.encryption import decrypt_text
from web.file_response import get_html_file_data
from web.utils import format_balance

router = APIRouter()


@router.get("/wallet")
async def wallet_handler():
    return HTMLResponse(content=get_html_file_data("wallet.html"))


@router.get("/get_wallet_data")
async def get_wallet_data_handler(request: Request):
    address = decrypt_text(request.cookies["address"])
    return {
        "address": address,
        "balance": format_balance(await calculate_balance(address=address)),
    }
