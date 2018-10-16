from abc import ABC, abstractmethod
from datetime import datetime


class Model(ABC):
    def __init__(self, data):
        self.id = int(data['id'])

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __repr__(self):
        return "<shitcord.Model id={.id}>".format(self)

    @property
    def created_at(self):
        when = (self.id >> 22) + 1420070400000
        return datetime.fromtimestamp(when)

    @abstractmethod
    def to_json(self):
        pass
