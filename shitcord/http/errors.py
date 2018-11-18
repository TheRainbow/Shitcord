# -*- coding: utf-8 -*-
from enum import Enum


class HTTPCodes(Enum):

    BAD_REQUEST                 = 400
    UNAUTHORIZED                = 401
    FORBIDDEN                   = 403
    NOT_FOUND                   = 404
    METHOD_NOT_ALLOWED          = 405
    INTERNAL_SERVER_ERROR       = 500
    NOT_IMPLEMENTED             = 501
    GATEWAY_UNAVAILABLE         = 502
    SERVICE_UNAVAILABLE         = 503
    GATEWAY_TIMEOUT             = 504
    HTTP_VERSION_NOT_SUPPORTED  = 505
    NOT_EXTENDED                = 510



class JSONCodes(Enum):

    UNKNOWN_ACCOUNT                                 = 10001
    UNKNOWN_APPLICATION                             = 10002
    UNKNOWN_CHANNEL                                 = 10003
    UNKNOWN_GUILD                                   = 10004
    UNKNOWN_INTEGRATION                             = 10005
    UNKNOWN_INVITE                                  = 10006
    UNKNOWN_MEMBER                                  = 10007
    UNKNOWN_MESSAGE                                 = 10008
    UNKNOWN_OVERWRITE                               = 10009
    UNKNOWN_PROVIDER                                = 10010
    UNKNOWN_ROLE                                    = 10011
    UNKNOWN_TOKEN                                   = 10012
    UNKNOWN_USER                                    = 10013
    UNKNOWN_EMOJI                                   = 10014
    UNKNOWN_WEBHOOK                                 = 10015
    BOTS_CANNOT_USE_THIS_ENDPOINT                   = 20001
    ONLY_BOTS_CAN_USE_THIS_ENDPOINT                 = 20002
    MAXIMUM_GUILDS_REACHED                          = 30001
    MAXIMUM_FRIENDS_REACHED                         = 30002
    MAXIMUM_PINS_REACHED                            = 30003
    MAXIMUM_GUILD_ROLES_REACHED                     = 30005
    MAXIMUM_REACTIONS_REACHED                       = 30010
    MAXIMUM_GUILD_CHANNELS_REACHED                  = 30013
    UNAUTHORIZED                                    = 40001
    MISSING_ACCESS                                  = 50001
    INVALID_ACCOUNT_TYPE                            = 50002
    CANNOT_EXECUTE_ON_DM_CHANNEL                    = 50003
    WIDGET_DISABLED                                 = 50004
    CANNOT_EDIT_MESSAGE_BY_ANOTHER_USER             = 50005
    CANNOT_SEND_EMPTY_MESSAGE                       = 50006
    CANNOT_SEND_MESSAGE_TO_USER                     = 50007
    CANNOT_SEND_MESSAGE_IN_VOICE                    = 50008
    CHANNEL_VERIFICATION_TOO_HIGH                   = 50009
    OAUTH2_APPLICATION_DOES_NOT_HAVE_A_BOT          = 50010
    OAUTH2_APPLICATION_LIMIT_REACHED                = 50011
    INVALID_OAUTH2_STATE                            = 50012
    MISSING_PERMISSIONS                             = 50013
    INVALID_AUTH_TOKEN                              = 50014
    NOTE_IS_TOO_LONG                                = 50015
    TOO_MANY_OR_FEW_MESSAGES_TO_DELETE              = 50016
    MESSAGE_CAN_ONLY_PINNED_IN_MESSAGE_CHANNEL      = 50019
    INVITE_TOKEN_INVALID_OR_TAKEN                   = 50020
    CANNOT_EXECUTE_ON_SYSTEM_MESSAGE                = 50021
    INVALID_OAUTH2_ACCESS_TOKEN                     = 50025
    MESSAGE_TO_OLD_TO_BULK_DELETE                   = 50034
    INVALID_FORM_BODY                               = 50035
    INVITE_WAS_ACCEPTED_WHERE_BOT_IS_NOT_IN         = 50036
    INVALID_API_VERSION                             = 50041
    REACTION_BLOCK                                  = 90001


class ShitRequestFailedError(Exception):
    """Yeah, mate, stupid thing. Your fuck failed and you received a non-success status code."""

    def __init__(self, response, data, bucket, *, retries=None):
        self.response = response
        self.bucket = bucket

        self.status_code = None
        self.errors = None
        self.message = None

        self.failed = 'Your shit {0.bucket} failed with code {0.status_code.value} (HTTP code {0.response.status_code}): {0.message}'
        if retries:
            self.failed += ' after fucking {} retries!'.format(retries)

        # Try to get any useful information from the data
        if isinstance(data, dict):
            self.raw_status_code = data.get('code', 0)
            if self.raw_status_code <= 600:
                self.status_code = HTTPCodes(self.raw_status_code)
            else:
                self.status_code = JSONCodes(self.raw_status_code)
            self.errors = data.get('errors', {})
            self.message = data.get('message', '')
        else:
            self.message = data
            self.status_code = 0

        if self.errors:
            error_list = '\n'.join('{}: {}'.format(key, value) for key, value in self.errors.items())
            self.failed += '\nHere\'s a bunch of errors for you. Have fun with that crap:\n' + error_list

        super().__init__(self.failed.format(self))
