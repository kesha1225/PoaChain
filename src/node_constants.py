import dataclasses


@dataclasses.dataclass
class NodeConstant:
    url: str
    public_key: str
    title_id: str


YANDEX_NODE = NodeConstant(
    title_id="Yandex-1", url="http://127.0.0.1:1234", public_key="111"
)
SBER_NODE = NodeConstant(
    title_id="Sber-1", url="http://127.0.0.1:3456", public_key="222"
)
GAZ_NODE = NodeConstant(title_id="GAZ-1", url="http://127.0.0.1:7890", public_key="333")

ALL_NODES = [YANDEX_NODE, SBER_NODE, GAZ_NODE]
