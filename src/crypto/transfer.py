import time
from typing import Union
from base64 import b64encode
from random import random

from nacl.bindings import crypto_sign_open
from nacl.bindings.crypto_sign import crypto_sign

from chain_config import ChainConfig
from crypto import bech32
from crypto.bech32 import Encoding


def address_to_public_key(address: str) -> list[int]:
    prefix, list_int, encoding = bech32.bech32_decode(address)
    public_key = bech32.convertbits(list_int, 5, 8, False)
    return public_key


def public_key_to_address(public_key: list[int]) -> str:
    list_int = bech32.convertbits(public_key, 8, 5, True)
    address = bech32.bech32_encode(
        ChainConfig.address_prefix, list_int, Encoding.BECH32
    )
    return address


def to_2(value: int) -> list[int]:
    return [(value >> 8) & 0xFF, value & 0xFF]


def to_4(value: int) -> list[int]:
    res = [
        (value & 0xFF000000) >> 24,
        (value & 0x00FF0000) >> 16,
        (value & 0x0000FF00) >> 8,
        (value & 0x000000FF) >> 0,
    ]
    return res


def set_list(trx: list[int], address: list[int]) -> None:
    trx += address


def set_amount(trx: list[int], amount: Union[int, float]) -> None:
    amount_to_bytes: bytes = int(amount).to_bytes(8, "big")
    to_list: list[int] = [int(i) for i in amount_to_bytes]

    trx += to_list


def sign(trx: list[int], sk: list[int]) -> None:
    signature = crypto_sign(bytes(trx), bytes(sk))
    trx += signature[:64]


def sign_transaction(trx: list[int], sk: list[int]) -> None:
    timestamp = int(time.time())

    trx += to_4(timestamp)
    trx += to_4(int(random() * 9999))

    trx.append(0)
    sign(trx, sk)


def transfer_coins(
    public_key: list[int],
    private_key: list[int],
    target_address: str,
    amount: Union[int, float],
) -> str:
    trx: list[int] = []

    set_list(trx, public_key)

    to_pk = address_to_public_key(target_address)
    set_list(trx, to_pk)
    set_amount(trx, amount)

    sign_transaction(trx, private_key)

    return b64encode(bytes(trx)).decode()
