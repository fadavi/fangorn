from unittest.mock import MagicMock
from fangorn.models.effect import Effect


def test_effect():
    fighter = MagicMock()
    effect = Effect(1, 'message', fighter)
    assert effect.health_effect == 1
    assert effect.message == 'message'
    assert effect.fighter == fighter
