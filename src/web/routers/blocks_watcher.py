import aiohttp
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from node.api.block import (
    get_blocks_from_node,
    get_last_block_number_from_node,
    get_block_from_node,
)
from node.api.status import is_node_online
from node.utils import get_node_by_id
from node_constants import ALL_NODES
from web.file_response import get_html_file_data

router = APIRouter()


@router.get("/blocks")
async def watch_blocks(request: Request):
    return HTMLResponse(content=get_html_file_data("blocks.html"))


@router.post("/blocks_latest")
async def latest_blocks(request: Request):
    request_data = await request.json()
    node = request_data["node"]
    limit = request_data.get("limit", 100)
    offset = request_data.get("offset", 0)

    node = get_node_by_id(node_id=node)
    session = aiohttp.ClientSession()

    if node is None:
        await session.close()
        return {"blocks": [], "total_count": 0}

    if not await is_node_online(url=node.url, session=session):
        await session.close()
        return {"blocks": [], "total_count": 0}

    result_blocks = await get_blocks_from_node(
        url=node.url, session=session, limit=limit, offset=offset
    )
    await session.close()
    return result_blocks


@router.get("/block/{block_hash}")
async def watch_block(request: Request):
    return HTMLResponse(content=get_html_file_data("block.html"))


@router.get("/transaction/{transaction}")
async def watch_transaction(request: Request):
    return HTMLResponse(content=get_html_file_data("transaction.html"))


@router.post("/get_block_data")
async def get_block_data_handler(request: Request):
    request_data = await request.json()
    node = request_data["node"]
    block_hash = request_data["block"]

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
            "block_data": None,
            "balance": "Ошибка подключения",
            "nodes": nodes,
        }

    transaction_data = await get_block_from_node(
        url=node.url, session=session, block_hash=block_hash
    )

    await session.close()
    return {
        "status": True,
        "node_none": node is None,
        "block_data": transaction_data,
        "nodes": nodes,
    }
