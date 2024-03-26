from mnemonic import Mnemonic
from fastapi import APIRouter

from crypto.poa_mnemonic import get_data_from_mnemonic, is_valid_mnemonic
from web.encryption import encrypt_text
from web.models.mnemonic import UserInputMnemonic

router = APIRouter()


@router.get("/new_mnemonic")
async def generate_mnemonic():
    return {"mnemonic": Mnemonic().generate()}


@router.post("/get_data_from_mnemonic")
async def get_data_from_mnemonic_handler(user_mnemonic: UserInputMnemonic):
    mnemonic_phrase = user_mnemonic.mnemonic

    if not is_valid_mnemonic(mnemonic_phrase=mnemonic_phrase):
        return {"ok": False, "error": "Invalid mnemonic phrase"}

    mnemonic_data = get_data_from_mnemonic(mnemonic_phrase=mnemonic_phrase)

    return {
        "ok": True,
        "wallet_data": {
            "private_key": encrypt_text(mnemonic_data.private_key),
            "public_key": encrypt_text(mnemonic_data.public_key),
            "address": encrypt_text(mnemonic_data.address),
        },
    }
