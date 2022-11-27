from typing import TYPE_CHECKING
from random import Random
if TYPE_CHECKING:
    from fangorn.seed.seed import Seed


CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'


class Destiny(Random):
    def __init__(self, seed: 'Seed'):
        self._seed = seed
        super().__init__(seed)

    def seed(self, new_seed, **kwargs):
        """Raises RuntimeError if you try to change the seed value.
        """
        if new_seed != self._seed:
            raise RuntimeError('Destiny is destiny!')
        super().seed(new_seed, **kwargs)

    def getseed(self):
        return self._seed

    def decide(self, probability: float = .5):
        """probability must be in range [0, 1],
        otherwise ValueError will be raised.
        """
        if 0 <= probability <= 1:
            return self.random() < probability
        raise ValueError('probability must be in range [0, 1]')

    def decimal(self, start: float, stop: float, decimal_places: int = 1):
        return round(self.uniform(start, stop), decimal_places)

    def percent(self, start: float, stop: float):
        """first and stop must be in range [0, 1],
        otherwise ValueError will be raised.
        """
        if 0 <= start <= 1 and 0 <= stop <= 1:
            return round(self.uniform(start, stop), 3)
        raise ValueError('start and stop must in the range [0, 1]')

    def random_name(self, min_length=4, max_length=10):
        length = self.randint(min_length, max_length)
        chars = (
            self.choice(CONSONANTS if i % 2 == 0 else VOWELS)
            for i in range(length)
        )
        return ''.join(chars).title()
