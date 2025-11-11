from collections import OrderedDict as dict
from uuid import uuid4


class Entity(object):
    """ A container with a unique id for holding components.

    Entity have a relationship to their components.

    >>> e = Entity('player', 0)
    >>> e
    <Entity player:0>
    >>> print(e)
    OrderedDict()
    >>> e.health = 1
    >>> print(e)
    OrderedDict([('health', 1)])
    >>> print(e.health)
    1
    >>> print(e['health'])
    1
    >>> e['health'] = 10
    >>> e.health
    10
    """


    __slots__ = ['uid', 'name', 'components']


    def __init__(self, name=None, uid=None):
        """ Initialization of the object with a random unique id unless specified """
        self.uid = uuid4() if uid == None else uid
        self.name = name or ""
        self.components = dict()

    def __repr__(self):
        """ Representation of the object in the style: <Entity name:uid> """
        cname = self.__class__.__name__
        name = self.name or "None"
        return "<{} {}:{}>".format(cname, name, self.uid)

    def __str__(self):
        """ Returns the collection of components stored in the entity """
        # TODO implement iteration by yourself
        return str(self.components)

    def __getitem__(self, key):
        """ Returns a component value for given key """
        return self.components[key]

    def __setitem__(self, key, value):
        """ Sets a component value using key / value """
        self.components[key] = value

    def __getattr__(self, key):
        """ Allows access to the properties/components as an attribute """
        if key in super(Entity, self).__getattribute__('__slots__'):
            return super(Entity, self).__getattr__(key)
        return self.components[key]

    def copy(self):
        copy = Entity(self.name, self.uid)
        copy.components = self.components
        return copy


    def __setattr__(self, key, value):
        """ Allows access to the properties/components as an attribute """
        if key in super(Entity, self).__getattribute__('__slots__'):
            super(Entity, self).__setattr__(key, value)
        else:
            # Even if it is not technically a component, still add it
            #  as a simple 'attribute' component.
            self.components[key] = value



if __name__ == '__main__':
    from doctest import testmod

    testmod()