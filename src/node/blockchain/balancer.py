import aiohttp

from chain_config import NodeConfig
from node.api.status import is_node_online, is_node_ready
from node.api.block import get_last_block_number_from_node
from node.utils import get_node_by_id
from node_constants import ALL_NODES, NodeConstant, sort_nodes


async def get_suitable_node_url(
    session: aiohttp.ClientSession, exclude_urls: list[str]
) -> str | None:
    biggest_block_number = -1
    suitable_node_url = None

    for node in ALL_NODES:
        if node.title_id == NodeConfig.title_id:
            continue

        if node.url in exclude_urls:
            continue

        if not await is_node_online(url=node.url, session=session):
            continue

        last_node_block_number = await get_last_block_number_from_node(
            url=node.url, session=session
        )

        if last_node_block_number > biggest_block_number:
            biggest_block_number = last_node_block_number
            suitable_node_url = node.url

    return suitable_node_url


async def get_active_nodes(session: aiohttp.ClientSession) -> list[NodeConstant]:
    result = []

    for node in ALL_NODES:
        if node.title_id == NodeConfig.title_id:
            continue

        if not await is_node_online(url=node.url, session=session):
            continue

        result.append(node)

    return sort_nodes(result)


async def get_active_ready_nodes(session: aiohttp.ClientSession) -> list[NodeConstant]:
    result = []

    for node in ALL_NODES:
        if node.title_id == NodeConfig.title_id:
            continue

        if not await is_node_online(url=node.url, session=session):
            continue

        if not await is_node_ready(url=node.url, session=session):
            continue

        result.append(node)

    return sort_nodes(result)


async def is_previous_node(session: aiohttp.ClientSession, node: NodeConstant) -> bool:
    active_ready_nodes = await get_active_ready_nodes(session=session)

    current_node = get_node_by_id(node_id=NodeConfig.title_id)
    active_ready_nodes.append(current_node)
    active_ready_nodes = sort_nodes(active_ready_nodes)

    current_node_index = active_ready_nodes.index(current_node)
    previous_node = active_ready_nodes[current_node_index - 1]

    return node.title_id == previous_node.title_id
