from cryptography.fernet import Fernet

from chain_config import WebConfig


def encrypt_text(text: str) -> str:
    cipher_suite = Fernet(bytes.fromhex(WebConfig.encryption_key))
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text.decode()


def decrypt_text(encrypted_text: str) -> str:
    cipher_suite = Fernet(bytes.fromhex(WebConfig.encryption_key))
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text
