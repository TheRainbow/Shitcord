# -*- coding: utf-8 -*-

import shitcord

import logging
import sys
from random import randint

import gevent
import requests

from . import rate_limit
from .errors import ShitRequestFailedError

logger = logging.getLogger(__name__)


def _parse_response(response):
    if response.headers['Content-Type'] == 'application/json':
        return response.json()
    return response.text.encode('utf-8')


class HTTP:
    """
    This represents a shitty HTTP client that wraps around the requests library and makes all the requests to the Discord API, handles rate limits
    as well and parses the responses.
    """

    BASE_URL = 'https://discordapp.com/api/v6'
    MAX_RETRIES = 5

    LOG_SUCCESS = 'Gratz! {bucket} ({url}) has received {text}!'
    LOG_FAILED = 'Request to {bucket} ({url}) failed with status code {code}: {error}. Retrying after {seconds} seconds.'

    def __init__(self, token, **kwargs):
        self._session = kwargs.get('session', requests.Session())
        self._token = token
        self._lock = gevent.lock.RLock()
        self.limiter = rate_limit.Limiter()

        # Headers stuff
        self.headers = {
            'User-Agent': self.create_user_agent(),
            'Authorization': kwargs.get('application_type', 'Bot') + ' ' + self._token,
        }

    def make_request(self, route, fmt=None, **kwargs):
        """
        Makes a request to a given endpoint with a shit set of arguments.

        :param route:
            `shitcord.http.Routes` is what you need. To make sure your endpoint is valid.
        :param fmt:
            A dictionary containing all the necessary key-value-pairs to properly format the URL for the request.
        :param kwargs:
            Arguments that will be passed along to the requests library.

        :return:
            The API's response as a dictionary.
        """

        fmt = fmt or {}
        retries = kwargs.pop('retries', 0)

        # Prepare the headers
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers

        method = route[0].value
        endpoint = route[1].format(**fmt)
        bucket = (method, endpoint)
        logger.debug('Bucket: {}, Kwargs: {}'.format(bucket, kwargs))

        if not self.limiter.no_global_limit.is_set():
            self.limiter.no_global_limit.wait()

        url = (self.BASE_URL + endpoint)
        response = self._session.request(method, url, **kwargs)
        data = _parse_response(response)
        status = response.status_code

        # Rate Limit stuff
        self.limiter(bucket, response, data)

        if 200 <= status < 300:
            # Status codes 200, 201, 204 indicate successful requests. So just return the JSON response.
            logger.debug(self.LOG_SUCCESS.format(bucket=bucket, url=url, text=data))
            return data

        elif status != 429 and 400 <= status < 500:
            # These status codes are only caused by the user and won't disappear with another request.
            # It'd be just a waste of performance to attempt sending another request.
            raise ShitRequestFailedError(response, data, bucket)

        else:
            # Some retarded shit happened here. Let's try that again.
            retries += 1
            if retries > self.MAX_RETRIES:
                raise ShitRequestFailedError(response, data, bucket, retries=self.MAX_RETRIES)

            backoff = self.backoff()
            logger.debug(self.LOG_FAILED.format(bucket=bucket, url=url, code=status, error=response.content, seconds=backoff))

            gevent.sleep(backoff)
            return self.make_request(route, fmt, retries=retries, **kwargs)

    def make_iter_request(self, route, fmt=None, **kwargs):
        """
        Makes a request to a given endpoint with a shit set of arguments.

        The only difference to `make_request` is that this method will use
        iteration for the retries instead of recursion.

        Mainly for experimental purposes on performance.

        :param route:
            `shitcord.http.Routes` is what you need. To make sure your endpoint is valid.
        :param fmt:
            A dictionary containing all the necessary key-value-pairs to properly format the URL for the request.
        :param kwargs:
            Arguments that will be passed along to the requests library.

        :return:
            The API's response as a dictionary.
        """

        fmt = fmt or {}

        # Prepare the headers
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers

        method = route[0].value
        endpoint = route[1].format(**fmt)
        bucket = (method, endpoint)
        logger.debug('Bucket: {}, Kwargs: {}'.format(bucket, kwargs))

        if not self.limiter.no_global_limit.is_set():
            self.limiter.no_global_limit.wait()

        url = (self.BASE_URL + endpoint)

        with self._lock:
            for retry in range(self.MAX_RETRIES):
                response = self._session.request(method, url, **kwargs)
                data = _parse_response(response)
                status = response.status_code

                # Rate Limit stuff
                self.limiter(bucket, response, data)

                if 200 <= status < 300:
                    # Status codes 200, 201, 204 indicate successful requests. So just return the JSON response.
                    logger.debug(self.LOG_SUCCESS.format(bucket=bucket, url=url, text=data))
                    return data

                elif status != 429 and 400 <= status < 500:
                    # These status codes are only caused by the user and won't disappear with another request.
                    # It'd be just a waste of performance to attempt sending another request.
                    raise ShitRequestFailedError(response, data, bucket)

                else:
                    # Some retarded shit happened here. Let's try that again.
                    if retry > self.MAX_RETRIES:
                        raise ShitRequestFailedError(response, data, bucket, retries=self.MAX_RETRIES)

                    backoff = self.backoff()
                    logger.debug(self.LOG_FAILED.format(bucket=bucket, url=url, code=status, error=response.content, seconds=backoff))
                    gevent.sleep(backoff)

    def close(self):
        self._session.close()
        self._session = None

    def recreate(self, *, session=None):
        if not self._session:
            self._session = session or requests.Session()

    @staticmethod
    def backoff():
        """Generates a random backoff that will be used as the delay before the lib retries to make a request to the Discord API."""

        return randint(100, 50000) / 1000.0

    @staticmethod
    def create_user_agent():
        fmt = '{0.__title__} ({0.__url__}, v{0.__version__}) / Python {1[0]}.{1[1]}.{1[2]} / requests {2}'
        return fmt.format(shitcord, sys.version_info, requests.__version__)
