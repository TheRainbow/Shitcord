from datetime import datetime

DISCORD_EPOCH = 1420070400000


class Snowflake:
    def __init__(self, snowflake):
        self.flake = snowflake

        self.binary = '{0:08b}'.format(self.flake)
        self.timestamp = datetime.utcfromtimestamp(((self.flake >> 22) + DISCORD_EPOCH) / 1000)
        self.worker_id = (self.flake & 0x3E0000) >> 17
        self.process_id = (self.flake & 0x1F000) >> 12
        self.increment = self.flake & 0xFFF

    def create_snowflake(self, date: datetime, high=False):
        """
        Returns a snowflake pretending to be created at the given time.

        :param date:
            The datetime object the snowflake should pretend to be created on.
        :param high:
            Whether or not set the lower 22 bit to high or low.

        :return:
            A numeric snowflake. You already know.
        """

        unix_seconds = self._to_unix_seconds(date)
        milliseconds = int(unix_seconds * 1000 - DISCORD_EPOCH)

        return (milliseconds << 22) + (2 ** 22 - 1 if high else 0)

    @staticmethod
    def _to_unix_seconds(date):
        return (date - datetime(1970, 1, 1)).total_seconds()
