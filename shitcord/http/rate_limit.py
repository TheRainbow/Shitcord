# -*- coding: utf-8 -*-

import logging
import gevent
from gevent.event import Event
from email.utils import parsedate_to_datetime
import datetime

logger = logging.getLogger(__name__)


class APIResponse:
    def __init__(self, response, bucket):
        self.response = response
        self.bucket = bucket
        self.headers = response.headers

        self.remaining = int(self.headers.get('X-RateLimit-Remaining', 0))
        self.reset = int(self.headers.get('X-RateLimit-Reset', 0))

        self.duration = 0.  # This is the actual rate limit duration

    def __repr__(self):
        return '<API Response for bucket {} with headers: {}>'.format(self.bucket, self.headers)

    @property
    def is_rate_limited(self):
        return self.remaining == 0

    @property
    def rate_limit_duration(self):
        return self.duration

    @property
    def status_code(self):
        return self.response.status_code

    def get_rate_limit_seconds(self):
        """Returns the total seconds of the rate limit duration."""

        now = parsedate_to_datetime(self.headers['Date'])
        reset = datetime.datetime.fromtimestamp(int(self.reset), datetime.timezone.utc)

        return (reset - now).total_seconds() + .5

    def sleep(self):
        """Fuck those rate limits. Let's wait until they're gone."""

        delay = self.rate_limit_duration
        logger.debug('Sleeping for {} seconds due to a rate limit...'.format(delay))
        return gevent.sleep(delay)


class Limiter:
    def __init__(self):
        self.is_global = False

        self.no_global_limit = Event()
        self.no_global_limit.set()

    def __call__(self, response, bucket):
        self.response = APIResponse(response, bucket)

        return self.cooldown()

    def cooldown(self):
        """This actually cools down a route."""

        self.check_rate_limit()

        if self.response.is_rate_limited and self.response.rate_limit_duration > 0:
            gevent.spawn(self.response.sleep).get()

            if self.is_global:
                self.is_global = False
                self.no_global_limit.set()

    def check_rate_limit(self):
        """Checks the HTTP status code to indicate the current rate limit status."""

        if self.response.is_rate_limited and self.response.status_code != 429:
            duration = self.response.get_rate_limit_seconds()

            logger.debug('Rate limit for {}, seconds: {}'.format(self.response, duration))
            self.response.duration = duration

        elif self.response.status_code == 429:
            resp = self.response.response.json()

            retry_after = resp['retry_after'] / 1000.0
            logger.debug('You are being rate limited. We will retry it in {} seconds.'.format(retry_after))

            self.is_global = resp.get('global', False)
            if self.is_global:
                self.no_global_limit.clear()
                logger.debug('Dude, it\'s even a global rate limit! Let\'s sleep until that shit is done.')

            self.response.duration = retry_after
