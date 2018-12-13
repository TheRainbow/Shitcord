from .core import Model


class _Connection:
    def __init__(self, payload):
        self.id = payload['id']
        self.name = payload['name']
        self.type = payload['type']
        self.revoked = payload['revoked']
        self.integrations = payload['integrations']


class BaseUser(Model):
    def __init__(self, data, http):
        self._json = data
        super().__init__(data.get('id'), http)

        self.name = data.get('username')
        self.discriminator = data.get('discriminator')
        self.avatar = data.get('avatar')
        self.bot = data.get('bot')
        self.mfa = data.get('mfa_enabled')
        self.locale = data.get('locale')
        self.verified = data.get('verified')
        self.email = data.get('email')

    def __repr__(self):
        raise NotImplementedError

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json


class User(BaseUser):
    def __init__(self, data, http):
        super().__init__(data, http)

    def __repr__(self):
        return '<shitcord.User id={} name={} discriminator={} bot={}>'.format(self.id, self.name, self.discriminator, self.bot)
