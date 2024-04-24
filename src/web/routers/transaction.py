import base64

import aiohttp
import cryptography
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from crypto.converter import hex_to_int_list
from crypto.transfer import transfer_coins
from node.api.block import get_last_block_number_from_node
from node.api.status import is_node_online
from node.api.transaction import (
    send_transaction_to_mempool,
    get_transactions_from_node,
    get_transaction_from_node,
)
from node.utils import get_node_by_id
from node_constants import ALL_NODES
from web.encryption import decrypt_text
from web.file_response import get_html_file_data

router = APIRouter()


@router.post("/create_transaction")
async def create_transaction(request: Request):
    transaction_data = await request.json()

    public_key = list(
        bytes(hex_to_int_list(decrypt_text(transaction_data["publicKey"])))
    )
    private_key = list(
        bytes(hex_to_int_list(decrypt_text(transaction_data["privateKey"])))
    )

    try:
        encoded_transaction = transfer_coins(
            public_key=public_key,
            private_key=private_key,
            target_address=transaction_data["address"],
            amount=int(float(transaction_data["amount"]) * 100),
        )
    except Exception as e:
        return {"status": False, "message": str(e)}

    return {"status": True, "encoded_transaction": encoded_transaction}


@router.post("/send_transaction")
async def send_transaction(request: Request):
    transaction_data = await request.json()

    encoded_transaction = transaction_data["data"]
    node = transaction_data["node"]

    node = get_node_by_id(node_id=node)

    session = aiohttp.ClientSession()
    is_online = await is_node_online(url=node.url, session=session)

    if not is_online:
        await session.close()
        return {
            "status": False,
            "description": "Node not online",
        }

    return {
        "status": True,
        "result": await send_transaction_to_mempool(
            url=node.url, session=session, transaction_data=encoded_transaction
        ),
    }


@router.post("/get_transactions")
async def get_transactions(request: Request):
    request_data = await request.json()

    node = request_data["node"]

    try:
        address = decrypt_text(request_data["address"])
    except cryptography.fernet.InvalidToken:
        address = request_data["address"]
    transaction_type = request_data["type"]
    node = get_node_by_id(node_id=node)

    session = aiohttp.ClientSession()
    is_online = await is_node_online(url=node.url, session=session)

    if not is_online:
        await session.close()
        return {
            "transactions": [],
        }

    res = {"transactions": []}
    transactions = (
        await get_transactions_from_node(
            session=session,
            url=node.url,
            address=address,
            transaction_type=transaction_type,
        )
    )["transactions"]

    for tr in transactions:
        tr["is_income"] = tr["recipient_address"] == address
        res["transactions"].append(tr)

    await session.close()
    return res


@router.get("/transaction/{transaction}")
async def watch_transaction(request: Request):
    return HTMLResponse(content=get_html_file_data("transaction.html"))


@router.post("/get_transaction_data")
async def get_transaction_data_handler(request: Request):
    request_data = await request.json()
    node = request_data["node"]
    transaction = request_data["transaction"]

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
            "transaction_data": None,
            "balance": "Ошибка подключения",
            "nodes": nodes,
        }

    transaction_data = await get_transaction_from_node(
        url=node.url, session=session, transaction_hash=transaction
    )

    await session.close()
    return {
        "status": True,
        "node_none": node is None,
        "transaction_data": transaction_data,
        "nodes": nodes,
    }
