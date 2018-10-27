from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, data):
        pass


class ModelParser(Parser):
    def __init__(self, model):
        self.model = model

    def parse(self, data):
        return self.model(data)


class NullParser(Parser):
    def parse(self, data):
        return data
