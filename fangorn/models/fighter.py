from typing import TYPE_CHECKING
from abc import ABC
from .effect import PrimaryStrike, PrimaryDefence
if TYPE_CHECKING:
  from collections.abc import Iterable
  from .skills.skill import Skill
  from .attack import Attack


class Fighter(ABC):
  def __init__(self, team: str, name: str, strenght: float, defence: float,
               speed: float, luck: float, health: float,
               skills: 'Iterable[Skill]' = []) -> None:
    super().__init__()
    self._team = team
    self._name = name
    self._strenght = max(0, strenght)
    self._defence = max(0, defence)
    self._speed = max(0, speed)
    self._luck = max(0, min(1, luck))
    self._health = max(0, health)
    self._skills = skills

  @property
  def team(self):
    return self._team

  @property
  def name(self):
    return self._name

  @property
  def strenght(self):
    return self._strenght

  @property
  def defence(self):
    return self._defence

  @property
  def speed(self):
    return self._speed

  @property
  def luck(self):
    return self._luck

  @property
  def health(self):
    return self._health

  @property
  def skills(self):
    return self._skills

  @health.setter
  def health(self, health):
    self._health = max(0, health)

  def is_teammate(self, fighter: 'Fighter'):
    return self.team == fighter.team

  @property
  def alive(self):
    return self.health > 0

  def do_primary_action(self, attack: 'Attack'):
    if attack.attacker == self:
      damage = PrimaryStrike(-self.strenght, 'Attack', fighter=self)
      attack.add_effect(damage)
    elif attack.defender == self:
      defence_value = min(self.defence, -attack.total_negative_effect)
      defence = PrimaryDefence(defence_value, 'Defence', fighter=self)
      attack.add_effect(defence)

  def apply_skills(self, attack: 'Attack'):
    for skill in self.skills:
      skill.apply(self, attack)

  def act(self, attack: 'Attack'):
    self.do_primary_action(attack)
    self.apply_skills(attack)

  def choose_target(self, fighters: 'Iterable[Fighter]'):
    # For now, let's always attack the weakest one:
    potential_targets = (f for f in fighters if f.alive and f.team != self.team)
    return min(potential_targets, default= None, key=lambda f: f.health)
