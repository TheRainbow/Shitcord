from shitcord.models.core import Model


class Emoji(Model):
    def __init__(self, data):
        super().__init__(data)

        self.managed = bool(data['managed'])
        self.name = data['name']
        self.roles = [int(role) for role in data['roles']]
        self.require_colons = bool(data['require_colons'])
        self.animated = bool(data['animated'])
        try:
            self.id = int(data['id'])
        except KeyError:
            pass

    def to_json(self):
        raise NotImplementedError('Ill do it later. "later"')

    def __repr__(self):
        return '<shitcord.Emoji id=%d, name=%r, animated=%r>' % (self.id, self.name, self.animated)
