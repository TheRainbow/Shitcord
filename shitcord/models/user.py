from shitcord.models.core import Model


class User(Model):

    def __init__(self, data):
        super().__init__(data)

        self.username = data['username']
        self.discriminator = data['discriminator']
        self.avatar_hash = data['avatar']
        self.bot = bool(data.get('bot', False))
        self.mfa_enabled = data.get('mfa_enabled')
        self.locale = data.get('locale')
        self.verified = data.get('locale', True)
        self.email = data.get('email')

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
