from sys import float_info
from unittest import mock
from pytest import raises, fail, fixture, mark, approx
from fangorn.models.destiny import Destiny


@fixture
def destiny():
    return Destiny('0')


def test_set_same_seed(destiny: Destiny):
    try:
        destiny.seed(destiny._seed)
    except RuntimeError:
        fail('Unexpected RuntimError')


def test_mutate_seed(destiny: Destiny):
    with raises(RuntimeError):
        destiny.seed('1')


def test_getseed(destiny: Destiny):
    assert destiny.getseed() == '0'


@mark.parametrize('prob', [
    float('nan'),
    -float_info.epsilon,
    float('inf'),
    1 + float_info.epsilon,
    float('-inf'),
])
def test_decide_invalid_probability(destiny: Destiny, prob: float):
    with raises(ValueError):
        destiny.decide(prob)


@mock.patch('random.Random.random', lambda _: .5)
@mark.parametrize('prob,expected', [
    (+1.0, True),
    (+0.8, True),
    (+0.5, False),
    (+0.2, False),
    (+0.0, False),
])
def test_decide(destiny: Destiny, prob: float, expected: bool):
    assert destiny.decide(prob) == expected


@mock.patch('random.Random.uniform', lambda *_: 1234.4321)
def test_decimal(destiny: Destiny):
    assert destiny.decimal(1000, 2000, 2) == approx(1234.43)


@mark.parametrize('percent', [
    float('nan'),
    -float_info.epsilon,
    float('inf'),
    1 + float_info.epsilon,
    float('-inf'),
])
def test_percent_invalid_percents(destiny: Destiny, percent: float):
    with raises(ValueError):
        destiny.decide(percent)


@mock.patch('random.Random.uniform', lambda *_: .12345678)
def test_percent(destiny: Destiny):
    assert destiny.percent(.1, .6) == approx(.123)


@mock.patch('random.Random.randint', lambda *_: 4)
@mock.patch('random.Random.choice', lambda _, chars: chars[0])
def test_random_name(destiny: Destiny):
    assert destiny.random_name(3, 10) == 'Baba'
