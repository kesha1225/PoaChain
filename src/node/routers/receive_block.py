import aiohttp
from fastapi import APIRouter
from starlette.requests import Request

from chain.block import add_new_blocks_from_node
from chain.db.session import async_session
from crypto.sign import text_sign_verify
from node.blockchain.balancer import is_previous_node
from node.blockchain.validate import validate_block_with_transactions
from node.models.block import BlockModel
from node.utils import get_node_by_id

router = APIRouter()


@router.get("/is_ready")
async def is_ready_handler(request: Request):
    return {"is_ready": request.app.is_ready}


@router.post("/receive_notify")
async def receive_notify_handler(request: Request):
    notify_data = (await request.json())["notify_data"]
    node_id = notify_data["node_id"]
    node_message = notify_data["message"]
    node_sign = notify_data["sign"]

    node = get_node_by_id(node_id=node_id)

    if node is None:
        return {"status": False, "description": "Node not found"}

    verify_result = text_sign_verify(
        signature=node_sign, original_message=node_message, public_key=node.public_key
    )

    if not verify_result:
        return {"status": False, "description": "Bad sign"}

    request.app.is_ready = True
    return {"status": True}


@router.post("/receive_block")
async def receive_block_handler(request: Request):
    block_data_raw = (await request.json())["block_data"]
    block_data = BlockModel(**block_data_raw["block_data"])
    node_sign = block_data_raw["sign"]

    node = get_node_by_id(node_id=block_data.authority_id)

    if node is None:
        return {"status": False, "description": "Node not found"}

    verify_result = text_sign_verify(
        signature=node_sign,
        original_message=str(block_data.dict()),
        public_key=node.public_key,
    )

    if not verify_result:
        return {"status": False, "description": "Bad sign"}

    async with async_session() as sql_session:
        verify_result = await validate_block_with_transactions(
            session=sql_session, block=block_data
        )

        sql_session.expunge_all()

    if not verify_result.status:
        return {"status": False, "description": "Bad verify"}

    await add_new_blocks_from_node(new_blocks=verify_result.new_blocks)

    if await is_previous_node(session=aiohttp.ClientSession(), node=node):
        request.app.is_waiting = False

    return {"status": True}
