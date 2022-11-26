from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from effect import Effect
    from fighter import Fighter
    from destiny import Destiny


class Attack:
    def __init__(self, destiny: 'Destiny', attacker: 'Fighter',
                 defender: 'Fighter'):
        if attacker.team == defender.team:
            raise ValueError("We don't do friendly fire!")

        self._destiny = destiny
        self._attacker = attacker
        self._defender = defender
        self._effects: list['Effect'] = []

    @property
    def destiny(self):
        return self._destiny

    @property
    def attacker(self):
        return self._attacker

    @property
    def defender(self):
        return self._defender

    def add_effect(self, *new_effects: 'Effect'):
        self._effects.extend(new_effects)

    @property
    def effects(self):
        return iter(self._effects)

    def find_effect(self, effect_type: type['Effect']):
        return next(
            (e for e in self.effects if isinstance(e, effect_type)),
            None,
        )

    @property
    def total_negative_effect(self):
        return sum(
            e.health_effect for e in self.effects if e.health_effect < 0)

    @property
    def health_effect(self) -> float:
        return sum(e.health_effect for e in self.effects)
