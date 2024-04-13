import base64

import aiohttp
from fastapi import APIRouter
from starlette.requests import Request

from crypto.converter import hex_to_int_list
from crypto.transfer import transfer_coins
from node.api.status import is_node_online
from node.api.transaction import send_transaction_to_mempool
from node.utils import get_node_by_id
from web.encryption import decrypt_text

router = APIRouter()


@router.post("/create_transaction")
async def create_transaction(request: Request):
    transaction_data = await request.json()

    public_key = list(bytes(hex_to_int_list(decrypt_text(transaction_data["publicKey"]))))
    private_key = list(bytes(hex_to_int_list(decrypt_text(transaction_data["privateKey"]))))

    encoded_transaction = transfer_coins(
        public_key=public_key,
        private_key=private_key,
        target_address=transaction_data["address"],
        amount=int(float(transaction_data["amount"]) * 100)
    )

    return {"encoded_transaction": encoded_transaction}


@router.post("/send_transaction")
async def send_transaction(request: Request):
    transaction_data = (await request.json())

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
