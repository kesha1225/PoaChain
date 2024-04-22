import aiohttp
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from node.api.block import get_blocks_from_node
from node.api.status import is_node_online
from node.utils import get_node_by_id
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
        return {"blocks": []}

    if not await is_node_online(url=node.url, session=session):
        await session.close()
        return {"blocks": []}

    result_blocks = await get_blocks_from_node(
        url=node.url, session=session, limit=limit, offset=offset
    )
    await session.close()
    return result_blocks
