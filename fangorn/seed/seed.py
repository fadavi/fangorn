from base64 import b64decode, b64encode
from .. import __version__ as version
from sys import maxsize
from random import randrange
from .encode_int import encode_int
import json


Seed = str


def generate() -> Seed:
    int_seed = randrange(maxsize)
    str_seed = encode_int(int_seed)
    return str_seed


def seed_version():
    parts = version.split('.')
    if len(parts) == 0:
        return '0.0'
    if len(parts) == 1:
        return f'{parts[0]}.0'
    return f'{parts[0]}.{parts[1]}'


def serialize(seed: Seed) -> str:
    payload = [seed_version(), seed]
    payload_json = json.dumps(payload, separators=(',', ':'))
    payload_enc = b64encode(payload_json.encode('ascii'))
    return payload_enc.decode().strip('=')


def deserialize(payload_enc: str) -> Seed:
    try:
        payload_json = b64decode(payload_enc.encode('ascii') + b'==')
        payload = json.loads(payload_json)
    except BaseException as ex:
        raise RuntimeError('Invalid seed') from ex

    if not isinstance(payload, list) or len(payload) != 2:
        raise RuntimeError('Invalid seed')
    if payload[0] != seed_version():
        print(payload[0])
        raise RuntimeError('Unsupported seed version')

    return payload[1]


def deserialize_or_generate(encoded: str | None) -> Seed:
    if encoded is None:
        return generate()
    return deserialize(encoded)
