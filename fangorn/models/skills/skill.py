from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from fighter import Fighter
  from attack import Attack


class Skill(ABC):
  @abstractmethod
  def apply(self, owner: 'Fighter', attack: 'Attack'):
    raise NotImplementedError()
