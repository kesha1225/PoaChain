import asyncio
import random

import aiohttp

from chain.db import Block, Transaction
from chain_config import NodeConfig
from crypto.sign import sign_message
from node.blockchain.balancer import get_active_nodes, get_active_ready_nodes
from node.models.block import BlockModel
from node.models.transaction import TransactionModel


async def send_block_release_notify(session: aiohttp.ClientSession) -> None:
    active_nodes = await get_active_nodes(session=session)
    message = str(NodeConfig.block_notify_message.format(random_data=random.random()))

    tasks = []

    for node in active_nodes:
        tasks.append(
            session.post(
                f"{node.url}/receive_notify",
                json={
                    "notify_data": {
                        "node_id": NodeConfig.title_id,
                        "message": message,
                        "sign": sign_message(
                            message=message, private_key=NodeConfig.private_key
                        ),
                    }
                },
            )
        )

    await asyncio.gather(*tasks)


async def send_block_release_created(
    session: aiohttp.ClientSession,
    block: Block,
    block_transactions: list[TransactionModel],
) -> None:
    active_nodes = await get_active_ready_nodes(session=session)
    block_data = BlockModel(**block.to_dict(transactions=block_transactions))

    tasks = []

    for node in active_nodes:
        tasks.append(
            session.post(
                f"{node.url}/receive_block",
                json={
                    "block_data": {
                        "block_data": block_data.dict(),
                        "sign": sign_message(
                            message=str(block_data.dict()),
                            private_key=NodeConfig.private_key,
                        ),
                    }
                },
            )
        )

    await asyncio.gather(*tasks)
