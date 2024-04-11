import dataclasses

from node.models.block import NewBlocksModel


@dataclasses.dataclass
class BlocksVerifyResult:
    status: bool
    suitable_node_url: str | None = None
    new_blocks: NewBlocksModel | None = None
