import aiohttp
import cryptography
from cryptography.fernet import InvalidToken
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from node.api.block import get_last_block_number_from_node
from node.api.status import is_node_online
from node.api.user import get_address_balance
from node.utils import get_node_by_id
from node_constants import ALL_NODES
from web.encryption import decrypt_text
from web.file_response import get_html_file_data


router = APIRouter()


@router.get("/wallet")
async def wallet_handler():
    return HTMLResponse(content=get_html_file_data("wallet.html"))


@router.post("/get_wallet_data")
async def get_wallet_data_handler(request: Request):
    request_data = await request.json()
    node = request_data["node"]

    try:
        address = decrypt_text(request_data["address"])
    except cryptography.fernet.InvalidToken:
        address = request_data["address"]

    node = get_node_by_id(node_id=node)

    session = aiohttp.ClientSession()

    if node is None:
        is_online = False
    else:
        is_online = await is_node_online(url=node.url, session=session)

    nodes = []

    for _node in ALL_NODES:
        _is_node_online = await is_node_online(url=_node.url, session=session)
        if _is_node_online:
            blocks_count = await get_last_block_number_from_node(
                url=_node.url, session=session
            )
        else:
            blocks_count = -1

        nodes.append(
            {
                "title_id": _node.title_id,
                "is_online": _is_node_online,
                "blocks_count": blocks_count,
            }
        )

    if not is_online:
        await session.close()
        return {
            "status": False,
            "node_none": node is None,
            "description": "Node not online",
            "address": address,
            "balance": "Ошибка подключения",
            "nodes": nodes,
        }

    balance = await get_address_balance(url=node.url, session=session, address=address)
    if isinstance(balance, int):
        balance = round(balance / 100, 2)

    await session.close()
    return {
        "status": True,
        "node_none": node is None,
        "address": address,
        "balance": balance,
        "nodes": nodes,
    }
