def hex_to_int_list(hex_string: str) -> list[int]:
    return [int(i) for i in bytes.fromhex(hex_string)]
