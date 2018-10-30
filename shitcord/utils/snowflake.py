from datetime import datetime

DISCORD_EPOCH = 1420070400000


class Snowflake:
    __slots__ = ('flake', 'binary', 'timestamp', 'worker_id', 'process_id', 'increment')

    def __init__(self, snowflake):
        self.flake = snowflake

        self.binary = '{0:08b}'.format(self.flake)
        self.timestamp = datetime.utcfromtimestamp(((self.flake >> 22) + DISCORD_EPOCH) / 1000)
        self.worker_id = (self.flake & 0x3E0000) >> 17
        self.process_id = (self.flake & 0x1F000) >> 12
        self.increment = self.flake & 0xFFF

    @classmethod
    def create_snowflake(cls, date: datetime, high=False):
        """
        Returns a snowflake pretending to be created at the given time.

        :param date:
            The datetime object the snowflake should pretend to be created on.
        :param high:
            Whether or not set the lower 22 bit to high or low.

        :return:
            A numeric snowflake. You already know.
        """

        unix_seconds = cls._to_unix_seconds(date)
        milliseconds = int(unix_seconds * 1000 - DISCORD_EPOCH)

        return (milliseconds << 22) + (2 ** 22 - 1 if high else 0)

    @staticmethod
    def _to_unix_seconds(date):
        return (date - datetime(1970, 1, 1)).total_seconds()

    def get_shard_id(self, shard_count):
        """
        Computes the shard ID from a given snowflake.
        This ONLY works if the snowflake this class was initialized with is a valid guild id!

        :param shard_count:
            The amount of shards the bot is using.

        :return:
            The shard's id
        """

        return (self.flake >> 22) % shard_count
