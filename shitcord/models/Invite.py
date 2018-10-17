from shitcord import *


class Invite(Model):
    def __init__(self, data):
        super.__init__(data)

        self.code = data['code']
        self.guild = Guild(data['guild'])
        self.channel = Channel(data['channel'])
        self.approximate_presence_count = data['approximate_presence_count']
        self.approximate_member_count = data['approximate_member_count']

    def to_json(self):
        raise NotImplementedError("Ill do it later. 'later'")
