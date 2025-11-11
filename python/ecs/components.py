from collections import OrderedDict as dict
from random import randint
from Component import Component


class HealthComponent(Component):
    """ Contains the current and max value for health of an entity

    >>> from Entity import Entity
    >>> player = Entity('player', 0)
    >>> player.health = HealthComponent(current=100)
    >>> player.health
    <HealthComponent entity:player>
    >>> print(player.health)
    {
        "current": 100,
        "max": 100
    }
    >>> print(player.health.current)
    100
    >>> player.health.current -= 20
    >>> print(player.health.current)
    80
    """

    defaults = dict([('current', 100), ('max', 100)])

    @property
    def alive(self):
        """ Returns True if healthpoints are left, otherwise False """
        return self.current > 0

class DamageComponent(Component):
    """ Simple damage data for an given entity """

    defaults = dict([('normal', 10), ('critical', 15), ('critical_percentage', 15)])


    def __call__(self):
        """ Returns a damage calculation based on the properties of the component

        >>> from Entity import Entity
        >>> player = Entity('player', 0)
        >>> player.damage = DamageComponent(entity=player, normal=15, critical=20)
        >>> player.damage()
        15
        """
        crit = randint(0, 100) <= (self.critical_percentage - 1)
        damage = self.normal
        if crit: damage = self.critical
        return damage



if __name__=='__main__':
    from doctest import testmod

    testmod()