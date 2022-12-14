from typing import TYPE_CHECKING
from fangorn.models.effect import PrimaryDefence, PositiveEffect
from .skill import Skill
if TYPE_CHECKING:
    from fighter import Fighter
    from attack import Attack


class MagicShield(Skill):
    def __init__(self, probability: float, armor: float):
        super().__init__()
        self._probability = probability
        self._armor = armor

    def create_effect(self, owner: 'Fighter', health_effect: float):
        return PositiveEffect(
            health_effect=health_effect * self._armor,
            message='Magic Shield',
            fighter=owner,
        )

    def apply(self, owner: 'Fighter', attack: 'Attack'):
        if attack.defender != owner:
            return

        primary_defence = attack.find_effect(PrimaryDefence)
        if primary_defence is None:
            return

        if attack.destiny.decide(self._probability):
            eff = self.create_effect(owner, primary_defence.health_effect)
            attack.add_effect(eff)
