from base64 import b85encode


def encode_int(num: int) -> str:
    n_len = (num.bit_length() + 7) // 8
    n_bytes = num.to_bytes(n_len, byteorder='little', signed=True)
    return b85encode(n_bytes).decode().strip('=')
