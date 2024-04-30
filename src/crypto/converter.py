import base64
from base64 import b64decode

from chain.constants import (
    PUBLIC_KEY_LENGTH,
    AMOUNT_LENGTH,
    TIMESTAMP_LENGTH,
    RANDOM_DATA_LENGTH,
    SIGN_LENGTH,
)
from chain.transaction import calculate_transaction_hash
from crypto.transfer import public_key_to_address
from node.models.transaction import TransactionModel


def hex_to_int_list(hex_string: str) -> list[int]:
    return [int(i) for i in bytes.fromhex(hex_string)]


def extract_address_from_transaction(transaction: list[int]) -> tuple[list[int], str]:
    data = transaction[:PUBLIC_KEY_LENGTH]
    transaction[:] = transaction[PUBLIC_KEY_LENGTH:]
    return data, public_key_to_address(data)


def extract_amount_from_transaction(transaction: list[int]) -> int:
    data = transaction[:AMOUNT_LENGTH]
    transaction[:] = transaction[AMOUNT_LENGTH:]
    return int.from_bytes(bytes(data), "big")


def extract_timestamp_from_transaction(transaction: list[int]) -> int:
    data = transaction[:TIMESTAMP_LENGTH]
    transaction[:] = transaction[TIMESTAMP_LENGTH:]

    return int.from_bytes(bytes(data), "big")


def normalize_transaction(transaction: str) -> list[int]:
    return list(b64decode(transaction))


def expand_transaction_from_request(transaction: list[int]) -> TransactionModel:
    from_pub_key, from_address = extract_address_from_transaction(
        transaction=transaction
    )
    to_pub_key, to_address = extract_address_from_transaction(transaction=transaction)
    amount = extract_amount_from_transaction(transaction=transaction)
    timestamp = extract_timestamp_from_transaction(transaction=transaction)

    transaction_model = TransactionModel(
        sender_address=from_address,
        recipient_address=to_address,
        amount=amount,
        timestamp=timestamp,
    )
    transaction_model.transaction_hash = calculate_transaction_hash(
        transaction=transaction_model
    )
    return transaction_model
