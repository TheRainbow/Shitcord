from ..models.core import Model


class Role(Model):
    def __init__(self, data, http):
        super().__init__(data, http)
        self._json = data

        self.hoist = data['hoist']
        self.name = data['name']
        self.mentionable = data['mentionable']
        self.color = data['color']
        self.position = data['position']
        self.id = data['id']
        self.managed = data['managed']
        self.permissions = data['permissions']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json

    def __repr__(self):
        return '<shitcore.Role id={}, name={}>' .format(self.id, self.name)
