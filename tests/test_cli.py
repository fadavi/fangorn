from unittest import mock
from pytest import mark, raises
from fangorn.cli import cli


@mock.patch('time.sleep', lambda _: None)
@mock.patch('fangorn.seed.seed.deserialize_or_generate', lambda _: '0')
@mark.parametrize('args', [
    None,
    ['-d0'],
    ['-tHunters:orderus,orderus', '-tBeasts:beast,beast'],
    ['-tHunters:orderus', '-tBeasts1:beast', '-tBeasts2:beast'],
    ['-x-1'],
    ['-x0'],
    ['-x1'],
    ['-x1000'],
])
def test_successful(args):
    cli.main(args)


def test_invalid_seed():
    with raises(ValueError, match='Invalid seed'):
        cli.main(['-sInvalidSeed'])
