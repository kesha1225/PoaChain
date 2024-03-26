from typing import Union
from hashlib import pbkdf2_hmac, sha256
from mnemonic import Mnemonic

from nacl.bindings import crypto_sign_seed_keypair

from chain.constants import ADDRESS_PREFIX
from chain.crypto import bech32
from chain.crypto.converter import hex_to_int_list


def generate_mnemo_words() -> str:
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=256)


def to_seed(words: str) -> bytes:
    return pbkdf2_hmac("sha512", words.encode(), "mnemonic".encode(), 2048)


def to_unsigned_list_int(seed: bytes) -> list[int]:
    to_sha256 = sha256(seed).hexdigest()
    return [int(to_sha256[i : i + 2], 16) for i in range(0, len(to_sha256), 2)]


def generate_pk_sk(unsigned_list_int: list[int]) -> tuple[str, str]:
    public_key, secret_key = crypto_sign_seed_keypair(bytes(unsigned_list_int))
    return public_key.hex(), secret_key.hex()


def generate_wallet_address(public_key: str, prefix: str) -> str:
    convert_bits = bech32.convertbits(hex_to_int_list(public_key), 8, 5, True)
    return bech32.bech32_encode(prefix, convert_bits, 0)


def generate_wallet() -> tuple[str, str, str, str]:
    mnemo = generate_mnemo_words()
    seed = to_seed(mnemo)
    unsigned_int = to_unsigned_list_int(seed)
    pk, sk = generate_pk_sk(unsigned_int)
    address = generate_wallet_address(pk, prefix=ADDRESS_PREFIX)
    return address, mnemo, pk, sk


def restore_wallet(mnemonic: str) -> tuple[str, str, str, str]:
    seed = to_seed(mnemonic)
    unsigned_int = to_unsigned_list_int(seed)
    pk, sk = generate_pk_sk(unsigned_int)
    address = generate_wallet_address(pk, prefix=ADDRESS_PREFIX)
    return address, mnemonic, pk, sk
