from ..utils import Snowflake
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, data):
        self.id = int(data['id'])

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __repr__(self):
        return "<shitcord.Model id={.id}>".format(self)

    @property
    def created_at(self):
        return Snowflake(self.id).timestamp

    @abstractmethod
    def to_json(self):
        pass
