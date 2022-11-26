from typing import TYPE_CHECKING
from random import Random
from string import ascii_lowercase
if TYPE_CHECKING:
    from ..seed.seed import Seed


VOWELS = 'aeiou'
CONSONANTS = ''.join(set(ascii_lowercase) - set(VOWELS))


class Destiny(Random):
    def __init__(self, seed: 'Seed') -> None:
        super().__init__(seed)
        self._seed = seed

    def getseed(self):
        return self._seed

    def decide(self, probability: float):
        return self.random() < probability

    def decimal(self, start: float, stop: float, decimal_places: int = 1):
        return round(self.uniform(start, stop), decimal_places)

    def percent(self, start: float, stop: float):
        return round(self.uniform(start, stop), 3)

    def random_name(self, min_length=4, max_length=10):
        length = self.randint(min_length, max_length)
        chars = (
            self.choice(CONSONANTS if i % 2 == 0 else VOWELS)
            for i in range(length)
        )
        return ''.join(chars).title()
