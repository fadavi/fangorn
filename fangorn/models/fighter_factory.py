from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Callable
from .fighter import Fighter
from .skill.magic_shield import MagicShield
from .skill.rapid_strike import RapidStrike
if TYPE_CHECKING:
    from .destiny import Destiny


FighterCreator = Callable[[str], Fighter]


class BaseFighterFactory(ABC):
    def __init__(self, destiny: 'Destiny') -> None:
        self._destiny = destiny
        self._creators = self.init_creators()

    def by_name(self, team: str, name: str):
        name = name.strip().lower()
        create = self._creators.get(name)
        if create is None:
            raise RuntimeError(f'Invalid fighter "{name}"')
        return create(team)

    def by_team_arranges(
            self, team_arranges: Iterable[tuple[str, Iterable[str]]]):
        for team, fighter_names in team_arranges:
            for fighter_name in fighter_names:
                yield self.by_name(team, fighter_name)

    def supported_names(self):
        return self._creators.keys()

    @abstractmethod
    def init_creators(self) -> dict[str, FighterCreator]:
        raise NotImplementedError()


class FighterFactory(BaseFighterFactory):
    def init_creators(self) -> dict[str, FighterCreator]:
        return dict(
            orderus=self.create_orderus,
            beast=self.create_beast,
        )

    def create_orderus(self, team: str):
        destiny = self._destiny
        return Fighter(
            team=team,
            name='Orderus',
            strenght=destiny.decimal(70, 80),
            defence=destiny.decimal(45, 55),
            speed=destiny.decimal(40, 50),
            luck=destiny.percent(.1, .3),
            health=destiny.decimal(70, 100),
            skills=[
                RapidStrike(probability=.1),
                MagicShield(probability=.2, armor=.5),
            ]
        )

    def create_beast(self, team: str):
        destiny = self._destiny
        return Fighter(
            team=team,
            name=destiny.random_name(),
            strenght=destiny.decimal(60, 90),
            defence=destiny.decimal(40, 60),
            speed=destiny.decimal(40, 60),
            luck=destiny.percent(.25, 40),
            health=destiny.decimal(60, 90),
        )
