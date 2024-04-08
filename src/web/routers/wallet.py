from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from node_constants import ALL_NODES
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

    # todo: тут поолучать баланс с ноды
    return {
        "address": address,
        "balance": format_balance(1),
        "nodes": [node.title_id for node in ALL_NODES],
    }
