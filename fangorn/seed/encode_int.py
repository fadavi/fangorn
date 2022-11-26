from base64 import b32encode


def encode_int(n: int) -> str:
    n_len = (n.bit_length() + 7) // 8
    n_bytes = n.to_bytes(n_len, byteorder='little', signed=True)

    base32 = b32encode(n_bytes)
    return base32.decode().strip('=')
