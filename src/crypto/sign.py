import base64

from nacl.exceptions import BadSignatureError
from nacl.bindings import crypto_sign, crypto_sign_open

from crypto.converter import hex_to_int_list
from crypto.transfer import to_public_key


def sign_message(message: str, private_key: str) -> str:
    encoded_message = message.encode()
    result = crypto_sign(
        message=encoded_message, sk=bytes(hex_to_int_list(private_key))
    )
    return base64.b64encode(result[: -len(encoded_message)]).decode()


def sign_verify(signature: str, original_message: str, address: str) -> bool:
    public_key = to_public_key(address)
    base64_sig = base64.b64decode(signature)

    base64_sig += original_message.encode()
    try:
        result = crypto_sign_open(signed=base64_sig, pk=bytes(public_key))
    except BadSignatureError:
        return False

    return result.decode() == original_message
