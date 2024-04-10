import base64

from cryptography.hazmat.primitives.asymmetric import ed25519
from nacl.bindings import crypto_sign

from chain.constants import PUBLIC_KEY_LENGTH, TRANSACTION_PURE_LENGTH
from crypto.converter import hex_to_int_list


def sign_message(message: str, private_key: str) -> str:
    encoded_message = message.encode()
    result = crypto_sign(
        message=encoded_message, sk=bytes(hex_to_int_list(private_key))
    )
    return base64.b64encode(result[: -len(encoded_message)]).decode()


def verify_sign(transaction: list[int]) -> bool:
    public_key = transaction[:PUBLIC_KEY_LENGTH]
    original_msg = transaction[:TRANSACTION_PURE_LENGTH]
    sign = transaction[TRANSACTION_PURE_LENGTH:]

    pk2 = ed25519.Ed25519PublicKey.from_public_bytes(bytes(public_key))

    try:
        pk2.verify(bytes(sign), bytes(original_msg))
        return True
    except Exception as e:
        return False
