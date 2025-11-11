import json


class Component():
    """ Contains a set of unique properties or attributes that can be
    associated with an Entity.

    Components have a tiglty coupled relationship with an entity.

    >>> from components import HealthComponent
    >>> from Entity import Entity
    >>> e = Entity("Player", 0)
    >>> e.health = HealthComponent()
    >>> print(e.health)
    {
        "current": 100,
        "max": 100
    }
    """


    __slots__ = ['entity']
    defaults = dict()
    Catalog = dict()
    ComponentTypes = dict()


    def __new__(cls, entity=None, **properties):
        cname = cls.__name__
        if cname not in Component.ComponentTypes:
            Component.ComponentTypes[cname] = cls
            cls.Catalog = {}
        if entity is not None:
            if entity not in cls.Catalog:
                component = super(Component, cls).__new__(cls)
                cls.Catalog[entity] = component
            else:
                component = cls.Catalog[entity]
        else:
            component = super(Component, cls).__new__(cls)
        return component

    def __init__(self, entity=None, **properties):
        """ Properties """
        self.entity = entity
        for prop, val in self.defaults.items():
            setattr(self, prop, properties.get(prop, val))

    def __repr__(self):
        """ Representation of the object in the style: <Component entity_name:entity_id> """
        cname = self.__class__.__name__
        entity_info = 'entity:None'
        if self.entity:
            # if we have an entity, look if this component is stored in it
            for prop_name, component in self.entity.components.items():
                if component == self:
                    entity_info = "entity:{}".format(self.entity.name)
                    break
        return "<{} {}>".format(cname, entity_info)

    def __str__(self):
        """ Dump out the JSON of the properties """
        keys = self.defaults.keys()
        data = dict()
        for key in keys:
            if key != 'defaults':
                data[key] = getattr(self, key)
        json_string = '\n'.join(
                line.rstrip()
                for line in json.dumps(data, indent=4).split('\n')
                )
        return json_string

    def restart(self):
        for prop_name, value in self.defaults.items():
            setattr(self, prop_name, value)


if __name__ == '__main__':
    from doctest import testmod

    testmod()