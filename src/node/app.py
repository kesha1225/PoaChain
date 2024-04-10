import asyncio
import logging

import aiohttp
from fastapi import FastAPI

from .blockchain.startup import start_node
from .routers import alive_router, block_router, receive_transaction_router


app = FastAPI()


async def _startapp():
    session = aiohttp.ClientSession()
    await start_node(session=session)
    await session.close()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(_startapp())


logging.basicConfig(level="INFO")
app.include_router(alive_router)
app.include_router(block_router)
app.include_router(receive_transaction_router)
