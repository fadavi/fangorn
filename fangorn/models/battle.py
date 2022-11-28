from collections.abc import Iterable
from typing import TYPE_CHECKING
from abc import ABC
from .attack import Attack
if TYPE_CHECKING:
    from fighter import Fighter
    from destiny import Destiny


class Battle(ABC):
    def __init__(self,
                 destiny: 'Destiny',
                 fighters: Iterable['Fighter']):
        """Raises ValueError if fighters is empty.
        """
        super().__init__()
        self._destiny = destiny
        self._fighters = list(fighters)
        self._attack_counts = {f: 0 for f in self._fighters}
        if len(self._fighters) == 0:
            raise ValueError('fighters cannot be an empty iterable')

    @property
    def destiny(self):
        return self._destiny

    def alive_fighters(self):
        return (af for af in self._fighters if af.alive)

    def alive_fighters_attack_counts(self):
        return filter(lambda tup: tup[0].alive, self._attack_counts.items())

    def alive_fighters_having_fewest_attacks(self):
        fighters: list['Fighter'] = []
        fewest_attacks: int = -1
        for f, a in self.alive_fighters_attack_counts():
            if fewest_attacks == -1 or a < fewest_attacks:
                fewest_attacks = a
                fighters = [f]
            elif a == fewest_attacks:
                fighters.append(f)
        return fighters

    def potential_attackers(self):
        """A fighter is a potential attacker when they preferably have 
        had the least attacks so far, and have got the most speed and luck.
        """
        potential_attackers: list['Fighter'] = []
        best_speed: float = -1
        best_luck: float = -1
        for f in self.alive_fighters_having_fewest_attacks():
            if best_speed == -1 or f.speed > best_speed:
                best_speed, best_luck = f.speed, f.luck
                potential_attackers = [f]
            elif f.speed != best_speed:
                continue
            if f.luck > best_luck:
                best_luck = f.luck
                potential_attackers = [f]
            elif f.luck == best_luck:
                potential_attackers.append(f)
        return potential_attackers

    def is_draw(self):
        return not any(self.alive_fighters())

    def winners(self):
        """Returns the alive winners.
        None means the battle is draw or is not finished yet.
        """
        alive_fighters = self.alive_fighters()

        first_alive = next(alive_fighters, None)
        if first_alive is None:
            return None
        if any(af for af in alive_fighters if not af.is_teammate(first_alive)):
            return None

        return self.alive_fighters()

    def next_attacker(self):
        potential_attackers = self.potential_attackers()

        if len(potential_attackers) == 0:
            raise RuntimeError('Failed to choose an attacker')
        if len(potential_attackers) == 1:
            return potential_attackers[0]
        else:
            return self._destiny.choice(potential_attackers)

    def create_attack(self, attacker: 'Fighter'):
        """None means the attacker prefers to not attack.
        """
        self._attack_counts[attacker] += 1

        defender = attacker.choose_target(self.alive_fighters())
        if defender is None:
            # No problem, they prefer to do nothing!
            return None

        return Attack(self._destiny, attacker, defender)

    def shuffled_others(self, *omitted_fighters: 'Fighter'):
        """Omits provided omitted_fighters
        and returns other fighters, shuffled.
        """
        others = [f for f in self.alive_fighters()
                  if f not in omitted_fighters]
        self._destiny.shuffle(others)
        return others

    def finish_attack(self, attack: 'Attack'):
        """An attack will be finished finished
        when all fighters has done their turn.
        """
        attacker, defender = attack.attacker, attack.defender
        others = self.shuffled_others(attacker, defender)

        attacker.act(attack)
        for f in others:
            if attacker.is_teammate(f):
                f.act(attack)

        for f in others:
            if not attacker.is_teammate(f) and not defender.is_teammate(f):
                f.act(attack)

        defender.act(attack)
        for f in others:
            if defender.is_teammate(f):
                f.act(attack)

        return attack
