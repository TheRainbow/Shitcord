from ..models.channel import TextChannel as Channel
from ..models.core import Model
from ..models.guild import Guild


class Invite(Model):
    def __init__(self, data, http):
        super().__init__(data, http)
        self._json = data

        self.code = data['code']
        self.guild = Guild(data['guild'], http)
        self.channel = Channel(data['channel'], http)
        self.approximate_presence_count = data['approximate_presence_count']
        self.approximate_member_count = data['approximate_member_count']

    def to_json(self, **kwargs):
        json = self._json
        if kwargs:
            json.update(kwargs)

        return json

    def __repr__(self):
        return '<shitcore.Invite id={}, code={}, channel={}>'.format(self.id, self.code, self.channel)
