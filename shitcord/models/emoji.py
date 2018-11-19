from .core import Model


class BaseEmoji(Model):
    def __init__(self, data, http):
        self._json = data
        super().__init__(data['http'], http)

        self.name = data['name']

    def __repr__(self):
        raise NotImplementedError

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class Emoji(BaseEmoji):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.name = data['name']
        self.roles = data.get('roles')
        self.user = data.get('user')
        self.require_colons = data.get('colons')
        self.managed = data.get('managed')
        self.animated = data.get('animated')

    def __repr__(self):
        return '<shitcord.Emoji id={} name={}>'.format(self.id, self.name)


class PartialEmoji(BaseEmoji):
    def __init__(self, data, http):
        super().__init__(data, http)

    def __repr__(self):
        return '<shitcord.PartialEmoji id={} name={}>'.format(self.id, self.name)
