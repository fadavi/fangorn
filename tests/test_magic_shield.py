from unittest.mock import MagicMock, patch
from pytest import fixture, mark
from fangorn.models.skill.magic_shield import MagicShield


@fixture
def magic_shield():
    return MagicShield(.3, .7)


def test_create_effect(magic_shield: MagicShield):
    owner = MagicMock()
    effect = magic_shield.create_effect(owner, 12.12)
    assert type(effect).__name__ == 'PositiveEffect'


def test_apply_another_defender(magic_shield: MagicShield):
    owner = MagicMock()
    attack = MagicMock(defender=MagicMock())
    magic_shield.apply(owner, attack)


def test_apply_no_primary_defence(magic_shield: MagicShield):
    attack = MagicMock(defender=MagicMock())

    attack.find_effect.return_value = None
    magic_shield.apply(attack.defender, attack)
    assert attack.find_effect.call_count == 1


@patch('fangorn.models.skill.magic_shield.MagicShield.create_effect',
       lambda *_: MagicMock())
@mark.parametrize('decision,added_effects', [
    (False, 0),
    (True, 1),
])
def test_apply_by_chance(magic_shield: MagicShield,
                         decision: bool,
                         added_effects: int):
    attack = MagicMock(defender=MagicMock())
    attack.find_effect.return_value = MagicMock()
    attack.destiny.decide.return_value = decision

    magic_shield.apply(attack.defender, attack)
    assert attack.add_effect.call_count == added_effects
