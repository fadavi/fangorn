from argparse import ArgumentParser
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collections.abc import Iterable


DEFAULT_MAX_ATTACKS = 20

# Not bad!
TEAM_PATTERN = r'\s*([^,:]+)(?::|,|$)'


class CliOptions:
    def __init__(self, seed: str | None, max_attacks: int,
                 teams: list[tuple[str, list[str]]], delay: float):
        self.seed = seed
        self.max_attacks = max_attacks
        self.teams = teams
        self.delay = delay


def parse_team_arrange(team: str):
    try:
        parts = re.findall(TEAM_PATTERN, team)
    except BaseException:
        raise RuntimeError(f'Invalid team arrange: "{team}"')

    if len(parts) < 2:
        raise RuntimeError(
            f'Team arrange should contain the team name and at least one fighter')

    name: str = parts[0]
    fighters: list[str] = parts[1:]
    return (name, fighters)


def team_arranges(teams: 'Iterable[str] | None'):
    if teams is None:
        return []
    return [parse_team_arrange(t) for t in teams]


def parse_args():
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

    args = parser.parse_args()
    return CliOptions(
        seed=None if args.seed is None else args.seed.strip(),
        max_attacks=args.max_attacks,
        teams=team_arranges(args.teams),
        delay=args.delay,
    )
