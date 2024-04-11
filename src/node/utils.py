from node_constants import ALL_NODES, NodeConstant


def get_node_by_id(node_id: str) -> NodeConstant | None:
    for node in ALL_NODES:
        if node.title_id == node_id:
            return node

    return None
