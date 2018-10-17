from shitcord.models.core import Model


class Role(Model):
    def __init__(self, data):
        super().__init__(data)

        self.hoist = data['hoist']
        self.name = data['name']
        self.mentionable = bool(data['mentionable'])
        self.color = int(data['color'])
        self.position = int(data['position'])
        self.id = int(data['id'])
        self.managed = bool(data['managed'])
        self.permissions = int(data['permissions'])

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
