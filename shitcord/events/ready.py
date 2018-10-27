from shitcord.models.core import Model


class Ready(Model):

    def __init__(self, data):
        data.update({'id': 0})
        super().__init__(data)

    def to_json(self):
        raise NotImplementedError('I will do later')
