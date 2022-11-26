from base64 import b32encode


def encode_int(num: int) -> str:
    n_len = (num.bit_length() + 7) // 8
    n_bytes = num.to_bytes(n_len, byteorder='little', signed=True)

    base32 = b32encode(n_bytes)
    return base32.decode().strip('=')
