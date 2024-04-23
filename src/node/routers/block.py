from fastapi import APIRouter
from starlette.requests import Request

from chain.block import (
    get_last_block_number,
    get_blocks_until_previous_hash,
    get_blocks,
    get_blocks_count,
    get_block_by_hash,
)
from chain.transaction import get_block_transactions

router = APIRouter()


@router.get("/get_last_block_number")
async def get_last_block_number_handler():
    return {"last_block_number": await get_last_block_number()}


@router.post("/get_blocks_until_hash")
async def get_blocks_until_hash(request: Request):
    last_block_previous_hash = (await request.json())["last_block_previous_hash"]
    return {
        "blocks": [
            block.to_dict(transactions=await get_block_transactions(block_id=block.id))
            for block in await get_blocks_until_previous_hash(
                last_block_previous_hash=last_block_previous_hash
            )
        ]
    }


@router.post("/get_blocks")
async def get_blocks_handler(request: Request):
    limit = request.query_params.get("limit", 100)
    offset = request.query_params.get("offset", 0)

    return {
        "blocks": [
            block.to_dict(transactions=await get_block_transactions(block_id=block.id))
            for block in await get_blocks(limit=limit, offset=offset)
        ],
        "total_count": await get_blocks_count(),
    }


@router.post("/get_block")
async def get_block_handler(request: Request):
    request_data = await request.json()
    block_hash = request_data["block_hash"]

    return {"block": await get_block_by_hash(block_hash=block_hash)}
