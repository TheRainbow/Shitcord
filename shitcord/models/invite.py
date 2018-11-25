from shitcord.models.channel import TextChannel as Channel
from shitcord.models.core import Model
from shitcord.models.guild import Guild


class Invite(Model):
    def __init__(self, data, http):
        super().__init__(data, http)

        self.code = data['code']
        self.guild = Guild(data['guild'], http)
        self.channel = Channel(data['channel'], http)
        self.approximate_presence_count = data['approximate_presence_count']
        self.approximate_member_count = data['approximate_member_count']

    def to_json(self):
        raise NotImplementedError('Ill do it later. "later"')

    def __repr__(self):
        return '<shitcore.Invite id=%d, code=%s, channel=%r>' % (self.id, self.code, self.channel)
