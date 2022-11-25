from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .fighter import Fighter


class Effect:
  def __init__(self, health_effect: float = 0, message: str = '',
               fighter: 'Fighter | None' = None):
    self._health_effect = health_effect
    self._message = message
    self._fighter = fighter

  @property
  def health_effect(self):
    return self._health_effect

  @property
  def message(self):
    return self._message

  @property
  def fighter(self):
    return self._fighter


class PositiveEffect(Effect):
  pass


class PrimaryDefence(Effect):
  pass


class NegativeEffect(Effect):
  pass


class PrimaryStrike(NegativeEffect):
  pass
