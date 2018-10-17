from shitcord import *


class Invite(Model):
    def __init__(self, data):
        super.__init__(data)

        self.code = data['code']
        self.guild = guild(data['guild'])
        self.channel = channel(data['channel'])
        self.approximate_presence_count = data['approximate_presence_count']
        self.approximate_member_count = data['approximate_member_count']

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
