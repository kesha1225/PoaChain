from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from web.encryption import decrypt_text
from web.file_response import get_html_file_data

router = APIRouter()


@router.get("/wallet")
async def wallet_handler():
    return HTMLResponse(content=get_html_file_data("wallet.html"))


@router.get("/get_wallet_data")
async def get_wallet_data_handler(request: Request):
    return {"address": decrypt_text(request.cookies["address"]), "balance": 32.22}
