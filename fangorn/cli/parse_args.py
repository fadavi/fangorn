from argparse import ArgumentParser
from dataclasses import dataclass
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


DEFAULT_MAX_ATTACKS = 20

# Not bad!
TEAM_PATTERN = r'\s*([^,:]+)(?::|,|$)'


@dataclass
class CliOptions:
    seed: str | None
    max_attacks: int
    teams: dict[str, list[str]]
    delay: float


def parse_team_arrange(team: str):
    try:
        parts = re.findall(TEAM_PATTERN, team)
    except BaseException as ex:
        raise RuntimeError(f'Invalid team arrange: "{team}"') from ex

    if len(parts) < 2:
        raise RuntimeError('Team arrange should contain the team name and ' +
                           'at least one fighter')

    name: str = parts[0]
    fighters: list[str] = parts[1:]
    return (name, fighters)


def team_arranges(teams: 'Iterable[str] | None'):
    if teams is None:
        return dict(Hunters=['orderus'],
                    Beasts=['beast'])
    return dict(parse_team_arrange(t) for t in teams)


def parse_args(args: 'Sequence[str] | None' = None):
    parser = ArgumentParser(prog='Fangorn')
    parser.add_argument('-s', '--seed',
                        required=False,
                        type=str)
    parser.add_argument('-x', '--max-attacks',
                        required=False,
                        type=int,
                        default=DEFAULT_MAX_ATTACKS)
    parser.add_argument('-t', '--team',
                        required=False,
                        type=str,
                        dest='teams',
                        action='append')
    parser.add_argument('-d', '--delay',
                        required=False,
                        type=float,
                        default=.5)

    opts = parser.parse_args(args)
    return CliOptions(
        seed=None if opts.seed is None else opts.seed.strip(),
        max_attacks=opts.max_attacks,
        teams=team_arranges(opts.teams),
        delay=opts.delay,
    )
