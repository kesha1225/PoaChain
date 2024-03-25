import pydantic


class UserInputMnemonic(pydantic.BaseModel):
    mnemonic: str
