from abc import ABC
from .models.battle import Battle


class BattleRunner(ABC):
    def __init__(self, battle: Battle, max_attacks: int):
        self._battle = battle
        self._max_attacks = max_attacks
