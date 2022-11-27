import binascii
import json
from unittest import mock
from pytest import raises
from fangorn.seed import seed


@mock.patch('random.randrange', lambda _: 1000)
@mock.patch('fangorn.seed.seed.encode_int', lambda _: 'fakeseed')
def test_generate():
    assert seed.generate() == 'fakeseed'


@mock.patch('fangorn.seed.seed.version', '')
def test_seed_against_empty_version():
    assert seed.seed_version() == '0.0'


@mock.patch('fangorn.seed.seed.version', '5')
def test_seed_major_only():
    assert seed.seed_version() == '5.0'


@mock.patch('fangorn.seed.seed.version', '4.3')
def test_seed_major_minor_only():
    assert seed.seed_version() == '4.3'


@mock.patch('fangorn.seed.seed.version', '1.4.24')
def test_seed_complete_version():
    assert seed.seed_version() == '1.4'


@mock.patch('fangorn.seed.seed.seed_version', lambda: '1.0')
def test_serialize():
    assert seed.serialize('fakeseed') == 'WyIxLjAiLCJmYWtlc2VlZCJd'


@mock.patch('base64.b64decode', **{
    'return_value.raiseError.side_effect': binascii.Error()
})
def test_deserialize_invalid_base64(_):
    with raises(ValueError, match='Invalid seed'):
        seed.deserialize('serializedseed')


@mock.patch('base64.b64decode', lambda _: 'invalidjson')
@mock.patch('json.loads', **{
    'return_value.raiseError.side_effect': json.JSONDecodeError('', '', 0)
})
def test_deserialize_invalid_json(_):
    with raises(ValueError, match='Invalid seed'):
        seed.deserialize('serializedseed')


@mock.patch('base64.b64decode', lambda _: 'fakejson')
@mock.patch('json.loads', lambda _: {'non': 'array'})
def test_deserialize_non_array_json():
    with raises(ValueError, match='Invalid seed'):
        seed.deserialize('serializedseed')


@mock.patch('base64.b64decode', lambda _: 'fakejson')
@mock.patch('json.loads', lambda _: ['1.5', 'fakeseed'])
@mock.patch('fangorn.seed.seed.version', '2.2')
def test_deserialize_version_mismatch():
    with raises(ValueError, match='Unsupported seed version'):
        seed.deserialize('serializedseed')


@mock.patch('fangorn.seed.seed.generate', lambda: 'generatedseed')
def test_deserialize_or_generate_against_none():
    assert seed.deserialize_or_generate(None) == 'generatedseed'


@mock.patch('fangorn.seed.seed.deserialize', lambda _: 'deserializedseed')
def test_deserialize_or_generate_against_non_none():
    assert seed.deserialize_or_generate('serializedseed') == 'deserializedseed'
