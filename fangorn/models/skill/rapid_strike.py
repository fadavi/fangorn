from typing import TYPE_CHECKING
from fangorn.models.effect import PrimaryStrike, NegativeEffect
from .skill import Skill
if TYPE_CHECKING:
    from fighter import Fighter
    from attack import Attack


class RapidStrike(Skill):
    def __init__(self, probability: float, max_repeats: int = 1):
        super().__init__()
        self._probability = probability
        self._max_repeats = max_repeats

    def create_effect(self, owner: 'Fighter', health_effect: float):
        return NegativeEffect(
            health_effect,
            message='Rapid Strike',
            fighter=owner,
        )

    def apply(self, owner: 'Fighter', attack: 'Attack'):
        if attack.attacker != owner:
            return

        primary_strike = attack.find_effect(PrimaryStrike)
        if primary_strike is None:
            return

        for _ in range(self._max_repeats):
            if attack.destiny.decide(self._probability):
                eff = self.create_effect(owner, primary_strike.health_effect)
                attack.add_effect(eff)
