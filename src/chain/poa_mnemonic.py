import dataclasses
import hashlib
import hmac
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1

from chain.constants import ADDRESS_PREFIX


@dataclasses.dataclass
class PoaKeys:
    private_key: SigningKey
    public_key: bytes
    address: str


def get_data_from_mnemonic(mnemonic_phrase: str) -> PoaKeys:
    mnemo = Mnemonic()
    seed = mnemo.to_seed(mnemonic_phrase)
    private_key_bytes = hmac.new(seed, b"POASEED", hashlib.sha512).digest()
    private_key = SigningKey.from_string(private_key_bytes[:32], curve=SECP256k1)
    public_key = private_key.verifying_key.to_string()
    hashed_public_key = hashlib.sha3_256(public_key).digest()
    address = ADDRESS_PREFIX + hashed_public_key.hex()[-40:]
    return PoaKeys(private_key=private_key, public_key=public_key, address=address)


def is_valid_mnemonic(mnemonic_phrase: str) -> bool:
    return Mnemonic().check(mnemonic=mnemonic_phrase)
