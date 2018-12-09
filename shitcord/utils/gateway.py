# -*- coding: utf-8 -*-

from collections import namedtuple
from contextlib import contextmanager

import gevent

from ..gateway import errors


class Limiter:
    def __init__(self, total, per):
        """
        A simple rate limiter to handle Gateway sending limits.
        A client is allowed to send up to 2 payloads per second, which counts up to a total of 30 payloads per 60 seconds.
        This class will simply be used to produce a delay before actually sending a payload.

        :param total:
            The total amount of allowed payloads...
        :param per:
            ...per the provided time interval in seconds.
        """

        self.total = total
        self.per = per
        self._lock = gevent.lock.Semaphore(self.total)

    def check(self):
        self._lock.acquire()

        def _release_lock():
            gevent.sleep(self.per)
            self._lock.release()

        gevent.spawn(_release_lock())


class SessionStartLimit(namedtuple('SessionStartLimit', 'total, remaining, reset_after lock')):
    __slots__ = ()

    def __new__(cls, total, remaining, reset_after, lock):
        """
        Representing a SessionStartLimit object that is included with the
        `Get Gateway Bot` endpoint.

        :param total:
            The total number of session starts the current user is allowed.
        :param remaining:
            The remaining number of session starts the current user is allowed.
        :param reset_after:
            The number in seconds after which the limit resets.
        """

        reset_after = reset_after / 1000  # Make seconds from the given milliseconds.

        return super().__new__(cls, total, remaining, reset_after, gevent.lock.RLock())

    @classmethod
    def from_payload(cls, payload):
        """
        Returns an instance of SessionStartLimit from a received Gateway payload.
        This is for internal purposes only.

        :param payload:
            The received payload from the Discord Gateway.

        :return:
            An instance of `SessionStartLimit`.
        """

        return cls(
            total=payload['total'],
            remaining=payload['remaining'],
            reset_after=payload['reset_after'],
            lock=gevent.lock.RLock(),
        )

    @property
    def limited(self):
        """
        Indicates whether the session start limit is exceeded.
        """

        return self.remaining == 0

    @contextmanager
    def safe_connect(self):
        """This contextmanager is used for safely connecting to the Discord Gateway.

        For the case you exceeded the limit for starting sessions,
        this will block until it is safe to attempt a connect.
        """

        if self.limited:
            duration = self.reset_after
        else:
            duration = 0

        timeout = gevent.Timeout(duration, errors.ConnectingFailed)
        timeout.start()

        try:
            yield self.lock.acquire()
        except Exception as e:
            if not isinstance(e, errors.ConnectingFailed):  # Suppress ConnectingFailed exceptions as they are intended.
                raise
        finally:
            timeout.close()
            self.lock.release()
