import dataclasses
from mnemonic import Mnemonic
from ecdsa import SigningKey

from chain.crypto.generate_wallet import restore_wallet


@dataclasses.dataclass
class PoaKeys:
    private_key: str
    public_key: str
    address: str


def get_data_from_mnemonic(mnemonic_phrase: str) -> PoaKeys:
    address, mnemonic, pk, sk = restore_wallet(mnemonic=mnemonic_phrase)
    return PoaKeys(private_key=sk, public_key=pk, address=address)


def is_valid_mnemonic(mnemonic_phrase: str) -> bool:
    return Mnemonic().check(mnemonic=mnemonic_phrase)
