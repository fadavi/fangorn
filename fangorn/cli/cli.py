from typing import TYPE_CHECKING
from time import sleep
from fangorn.models.fighter_factory import FighterFactory
from fangorn.models.battle_runner import BattleRunner
from fangorn.models.destiny import Destiny
from fangorn.models.battle import Battle
from fangorn.seed import seed
from .parse_args import parse_args
if TYPE_CHECKING:
    from collections.abc import Iterable
    from fangorn.models.fighter import Fighter
    from fangorn.models.attack import Attack


class CliBattleRunner(BattleRunner):
    def __init__(
            self,
            battle: 'Battle',
            max_attacks: int,
            delay: float = 0) -> None:
        super().__init__(battle, max_attacks)
        self._delay = delay

    def fighter(self, fighter: 'Fighter'):
        return f'{fighter.name}@{fighter.team}'

    def decimal(self, num: float):
        return f'{num:+.2f}'

    def print(self, message: str):
        print(message)
        if self._delay > 0:
            sleep(self._delay)

    def on_not_attacking(self, _: int, attacker: 'Fighter'):
        self.print(f'{attacker.name} somehow decided to do not attack!')

    def on_start(self, battle: 'Battle'):
        encoded_seed = seed.serialize(battle.destiny.getseed())
        self.print(f'BATTLE SEED: {encoded_seed}')

        fighters = list(battle.alive_fighters())
        self.print(f'There are {len(fighters)} fighters in the battle')

    def on_win(self, winners: 'Iterable[Fighter]'):
        winners_list = list(winners)
        first = winners_list[0]
        if len(winners_list) == 1:
            self.print(f'{self.fighter(first)} won the battle!')
        else:
            self.print(f'Team {first.team} won the battle')

    def on_draw(self):
        self.print("No one is alive; so, it's a draw!?")

    def on_peace(self, n_attacks: int):
        self.print(f'Fighters are too tired after {n_attacks} attacks. PEACE!')

    def on_before_attack(self, nth_attack: int, attack: 'Attack'):
        attacker = self.fighter(attack.attacker)
        defender = self.fighter(attack.defender)
        msg = [f'! Attack {nth_attack}:',
               f'! {attacker} attacks {defender}']
        self.print('\n'.join(msg))

    def on_attack_finished(self, _: int, attack: 'Attack'):
        for effect in attack.effects:
            health_effect = self.decimal(effect.health_effect)
            msg = ''
            if effect.fighter is not None:
                msg += self.fighter(effect.fighter) + ': '
            if effect.message is not None:
                msg += effect.message + f' ({health_effect})'
            else:
                msg += health_effect
            self.print(msg)

    def on_affected(self, _: int, attack: 'Attack'):
        defender = self.fighter(attack.defender)
        if attack.defender.alive:
            health = self.decimal(attack.defender.health)
            self.print(f'{defender} health: {health}')
        else:
            self.print(f'{defender} died! RIP.')


def main():
    opts = parse_args()

    the_seed = seed.deserialize_or_generate(opts.seed)
    destiny = Destiny(the_seed)

    team_arranges = opts.teams
    if len(team_arranges) == 0:
        team_arranges = [
            ('Hunters', ['orderus']),
            ('Beasts', ['beast']),
        ]

    fighter_factory = FighterFactory(destiny)
    fighters = list(fighter_factory.by_team_arranges(team_arranges))

    battle = Battle(destiny, fighters)
    runner = CliBattleRunner(battle, opts.max_attacks, opts.delay)

    while runner.finish_next_attack():
        pass
