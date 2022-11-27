from pytest import mark
from fangorn.seed.encode_int import encode_int


@mark.parametrize('num,expected', [
    (0, '00'),
    (+1, '0R'),
    (+8374923847123992, '7{u-9^1vMc'),
    (-1, '{{'),
    (-9921312389238293, '>v2_cp1|Dy')
])
def test_various_ints(num: int, expected: str):
    assert encode_int(num) == expected
