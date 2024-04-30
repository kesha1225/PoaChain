import dataclasses
from operator import attrgetter


@dataclasses.dataclass
class NodeConstant:
    url: str
    public_key: str
    title_id: str


def sort_nodes(nodes: list[NodeConstant]) -> list[NodeConstant]:
    return sorted(nodes, key=attrgetter("title_id", "url", "public_key"))


YANDEX_NODE = NodeConstant(
    title_id="Yandex-1",
    url="http://127.0.0.1:1234",
    public_key="3076124a6d30a1125e916bbbc99a8470f25ced4c777c1fd9c14d68fb275a3641",
)
SBER_NODE = NodeConstant(
    title_id="Sber-1",
    url="http://127.0.0.1:3456",
    public_key="b0b9d00d6a948e70c05173f2888150ae3945ae619526b85e0bba796ba68c5f92",
)
GAZ_NODE = NodeConstant(
    title_id="GAZ-1",
    url="http://127.0.0.1:7890",
    public_key="b49a1e105f4e8921d980d6f65791a7d843724b92f69d92065243e917c19427f4",
)

ALL_NODES = sort_nodes([YANDEX_NODE, SBER_NODE, GAZ_NODE])
