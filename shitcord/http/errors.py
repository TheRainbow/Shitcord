# -*- coding: utf-8 -*-


class ShitRequestFailedError(Exception):
    """Yeah, mate, stupid thing. Your fuck failed and you received a non-success status code."""

    def __init__(self, response, data, bucket, *, retries=None):
        self.response = response
        self.bucket = bucket

        self.status_code = None
        self.errors = None
        self.message = None

        self.failed = 'Your shit {0.bucket} failed with code {0.status_code} (HTTP code {0.response.status_code}): {0.message}'
        if retries:
            self.failed += ' after fucking {} retries!'.format(retries)

        # Try to get any useful information from the data
        if isinstance(data, dict):
            self.status_code = data.get('code', 0)
            self.errors = data.get('errors', {})
            self.message = data.get('message', '')
        else:
            self.message = data
            self.status_code = 0

        if self.errors:
            error_list = '\n'.join('{}: {}'.format(key, value) for key, value in self.errors.items())
            self.failed += '\nHere\'s a bunch of errors for you. Have fun with that crap:\n' + error_list

        super().__init__(self.failed.format(self))
