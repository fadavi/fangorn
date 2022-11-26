from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections.abc import Iterable
    from .attack import Attack
    from .battle import Battle
    from .fighter import Fighter


class BattleRunner(ABC):
    def __init__(self, battle: 'Battle', max_attacks: int) -> None:
        self._battle = battle
        self._max_attacks = max_attacks
        self._attacks_count = 0

    def is_finished(self):
        if self._attacks_count >= self._max_attacks:
            self.on_peace(self._attacks_count)
            return True
        if self._battle.is_draw():
            self.on_draw()
            return True
        winners = self._battle.winners()
        if winners is not None:
            self.on_win(winners)
            return True
        return False

    def finish_next_attack(self):
        if self._attacks_count == 0:
            self.on_start(self._battle)

        if self.is_finished():
            return False
        self._attacks_count += 1

        nth_attack = self._attacks_count
        attacker = self._battle.next_attacker()
        attack = self._battle.create_attack(attacker)

        if attack is None:
            self.on_not_attacking(self._attacks_count, attacker)
            return True

        self.on_before_attack(nth_attack, attack)

        attack = self._battle.finish_attack(attack)
        self.on_attack_finished(nth_attack, attack)

        attack.defender.health += attack.health_effect
        self.on_affected(nth_attack, attack)
        return True

    @abstractmethod
    def on_not_attacking(self, nth_attack: int, attacker: 'Fighter'):
        pass

    @abstractmethod
    def on_start(self, battle: 'Battle'):
        pass

    @abstractmethod
    def on_win(self, winners: 'Iterable[Fighter]'):
        pass

    @abstractmethod
    def on_draw(self):
        pass

    @abstractmethod
    def on_peace(self, n_attacks: int):
        pass

    @abstractmethod
    def on_before_attack(self, nth_attack: int, attack: 'Attack'):
        pass

    @abstractmethod
    def on_attack_finished(self, nth_attack: int, attack: 'Attack'):
        pass

    @abstractmethod
    def on_affected(self, nth_attack: int, attack: 'Attack'):
        pass
