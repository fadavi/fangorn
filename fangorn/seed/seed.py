from base64 import b64decode, b64encode
from random import randrange
from sys import maxsize
import json
from fangorn import __version__ as version
from .encode_int import encode_int


Seed = str


def generate() -> Seed:
    int_seed = randrange(maxsize)
    str_seed = encode_int(int_seed)
    return str_seed


def seed_version():
    if version in (None, ''):
        return '0.0'

    parts = version.split('.')
    if len(parts) == 1:
        return f'{parts[0]}.0'
    return f'{parts[0]}.{parts[1]}'


def serialize(seed: Seed) -> str:
    payload = [seed_version(), seed]
    payload_json = json.dumps(payload, separators=(',', ':'))
    encoded_payload = b64encode(payload_json.encode('ascii'))
    return encoded_payload.decode().strip('=')


def deserialize(encoded_payload: str) -> Seed:
    """Raises ValueError if the encoded_payload is invalid
    or belongs to an unsupported version.
    """
    try:
        payload_json = b64decode(encoded_payload.encode('ascii') + b'==')
        payload = json.loads(payload_json)
    except ValueError as err:
        raise ValueError('Invalid seed') from err

    if not isinstance(payload, list) or len(payload) != 2:
        raise ValueError('Invalid seed')
    if payload[0] != seed_version():
        print(payload[0])
        raise ValueError('Unsupported seed version')

    return payload[1]


def deserialize_or_generate(encoded: str | None) -> Seed:
    if encoded is None:
        return generate()
    return deserialize(encoded)
