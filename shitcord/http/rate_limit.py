# -*- coding: utf-8 -*-

import datetime
import logging
from email.utils import parsedate_to_datetime

import gevent

logger = logging.getLogger(__name__)


class APIResponse:
    def __init__(self, bucket, response, parsed):
        self._bucket = bucket
        self._response = response
        self._json = parsed
        self._headers = self._response.headers

        # Get all relevant headers for rate limit handling and immediately parse them into an useful format
        self.date = self._headers['Date']
        self.remaining = int(self._headers.get('X-RateLimit-Remaining', 0))
        self.reset = self.__parse_header(int(self._headers.get('X-RateLimit-Reset', 0)))
        self.is_global = self._headers.get('X-RateLimit-Global', False)

    def __repr__(self):
        return '<API Response for bucket {} with headers {}>'.format(self._bucket, self._headers)

    def update(self, headers):
        self.date = headers.get('Date')
        self.remaining = int(headers.get('X-RateLimit-Remaining'))
        self.reset = self.__parse_header(int(headers.get('X-RateLimit-Reset')))
        self.is_global = headers.get('X-RateLimit-Global', False)

    @property
    def is_rate_limited(self):
        return self._response.status_code == 429

    @property
    def will_rate_limit(self):
        return self._response.status_code != 429 and self.remaining == 0

    @property
    def global_limit(self):
        return self.is_rate_limited and self.is_global

    @property
    def retry_after(self):
        return self._json['retry_after'] / 1000.0

    def __parse_header(self, reset):
        now = parsedate_to_datetime(self.date)
        reset = datetime.datetime.fromtimestamp(reset, datetime.timezone.utc)
        return (reset - now).total_seconds() + .2

    def cooldown(self, duration):
        """This cools down a given route corresponding to a bucket."""

        logger.debug('Sleeping for {} seconds due to an exhausted/incoming rate limit...'.format(duration))
        return gevent.sleep(duration)


class Limiter:
    def __init__(self):
        self.no_global_limit = gevent.event.Event()
        self.no_global_limit.set()

    def __call__(self, bucket, response, parsed):
        response = APIResponse(bucket, response, parsed)
        self._cooldown_task(response)

    def _cooldown_task(self, response):
        duration, global_rate_limit = self.get_cooldown(response)

        gevent.spawn(response.cooldown, duration).get()
        if global_rate_limit:
            gevent.spawn_later(duration, self.no_global_limit.set())

    def get_cooldown(self, resp):
        if resp.will_rate_limit:
            duration = resp.reset
            logger.debug('Next request is going to cause a rate limit. We wait for a Rate Limit Reset in {} seconds.'.format(duration))

        elif resp.is_rate_limited:
            duration = resp.retry_after
            logger.debug('You are being rate limited. We will retry it in {} seconds.'.format(duration))

            if resp.global_limit:
                # Global rate limit. Not good.
                logger.debug('Global rate limit has been exhausted.')
                self.no_global_limit.clear()
        else:
            duration = 0

        return duration, resp.global_limit
