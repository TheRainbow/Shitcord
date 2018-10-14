# -*- coding: utf-8 -*-

from enum import Enum


class Methods(Enum):
    GET    = 'GET'
    POST   = 'POST'
    PUT    = 'PUT'
    PATCH  = 'PATCH'
    DELETE = 'DELETE'


class Endpoints:
    # Guild
    GUILD                             = '/guilds'
    CREATE_GUILD                      = (Methods.POST, GUILD)
    GET_GUILD                         = (Methods.GET, GUILD + '/{guild}')
    MODIFY_GUILD                      = (Methods.PATCH, GUILD + '/{guild}')
    DELETE_GUILD                      = (Methods.DELETE, GUILD + '/{guild}')
    GET_GUILD_CHANNELS                = (Methods.GET, GUILD + '/{guild}/channels')
    CREATE_GUILD_CHANNEL              = (Methods.POST, GUILD + '/{guild}/channels')
    MODIFY_GUILD_CHANNEL_POSITIONS    = (Methods.PATCH, '/{guild}/channels')
    GET_GUILD_MEMBER                  = (Methods.GET, GUILD + '/{guild}/members/{member}')
    LIST_GUILD_MEMBERS                = (Methods.GET, GUILD + '/{guild}/members')
    ADD_GUILD_MEMBER                  = (Methods.PUT, GUILD + '/{guild}/members/{member}')
    MODIFY_GUILD_MEMBER               = (Methods.PATCH, GUILD + '/{guild}/members/{member}')
    MODIFY_CURRENT_USER_NICK          = (Methods.PATCH, GUILD + '/{guild}/members/@me/nick')
    ADD_GUILD_MEMBER_ROLE             = (Methods.PUT, GUILD + '/{guild}/members/{member}/roles/{role}')
    REMOVE_GUILD_MEMBER_ROLE          = (Methods.DELETE, GUILD + '/{guild}/members/{member}/roles/{role}')
    REMOVE_GUILD_MEMBER               = (Methods.DELETE, GUILD + '/{guild}/members/{member}')
    GET_GUILD_BANS                    = (Methods.GET, GUILD + '/{guild}/bans')
    GET_GUILD_BAN                     = (Methods.GET, GUILD + '/{guild}/bans/{user}')
    CREATE_GUILD_BAN                  = (Methods.PUT, GUILD + '/{guild}/bans/{user}')
    REMOVE_GUILD_BAN                  = (Methods.DELETE, GUILD + '/{guild}/bans/{user}')
    GET_GUILD_ROLES                   = (Methods.GET, GUILD + '/{guild}/roles')
    CREATE_GUILD_ROLE                 = (Methods.POST, GUILD + '/{guild}/roles')
    MODIFY_GUILD_ROLE_POSITIONS       = (Methods.PATCH, GUILD + '/{guild}/roles')
    MODIFY_GUILD_ROLE                 = (Methods.PATCH, GUILD + '/{guild}/roles/{role}')
    DELETE_GUILD_ROLE                 = (Methods.DELETE, GUILD + '/{guild}/roles/{role}')
    GET_GUILD_PRUNE_COUNT             = (Methods.GET, GUILD + '/{guild}/prune')
    BEGIN_GUILD_PRUNE                 = (Methods.POST, GUILD + '/{guild}/prune')
    GET_GUILD_VOICE_REGIONS           = (Methods.GET, GUILD + '/{guild}/regions')
    GET_GUILD_INVITES                 = (Methods.GET, GUILD + '/{guild}/invites')
    GET_GUILD_INTEGRATIONS            = (Methods.GET, GUILD + '/{guild}/integrations')
    CREATE_GUILD_INTEGRATION          = (Methods.POST, GUILD + '/{guild}/integrations')
    MODIFY_GUILD_INTEGRATION          = (Methods.PATCH, GUILD + '/{guild}/integrations/{integration}')
    DELETE_GUILD_INTEGRATION          = (Methods.DELETE, GUILD + '/{guild}/integrations/{integration}')
    SYNC_GUILD_INTEGRATION            = (Methods.POST, GUILD + '/{guild}/integrations/{integration}/sync')
    GET_GUILD_EMBED                   = (Methods.GET, GUILD + '/{guild}/embed')
    MODIFY_GUILD_EMBED                = (Methods.PATCH, GUILD + '/{guild}/embed')
    GET_GUILD_VANITY_URL              = (Methods.GET, GUILD + '/{guild}/vanity-url')

    # Channel
    CHANNEL                           = '/channels/{channel}'
    GET_CHANNEL                       = (Methods.GET, CHANNEL)
    MODIFY_CHANNEL                    = (Methods.PATCH, CHANNEL)
    DELETE_CHANNEL                    = (Methods.DELETE, CHANNEL)
    GET_CHANNEL_MESSAGES              = (Methods.GET, CHANNEL + '/messages')
    GET_CHANNEL_MESSAGE               = (Methods.GET, CHANNEL + '/messages/{message}')
    CREATE_MESSAGE                    = (Methods.POST, CHANNEL + '/messages')
    CREATE_REACTION                   = (Methods.PUT, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')
    DELETE_OWN_REACTION               = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')
    DELETE_USER_REACTION              = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/{user}')
    GET_REACTIONS                     = (Methods.GET, CHANNEL + '/messages/{message}/reactions/{emoji}')
    DELETE_ALL_REACTIONS              = (Methods.DELETE, CHANNEL + '/messages/{message}/reactions')
    EDIT_MESSAGE                      = (Methods.PATCH, CHANNEL + '/messages/{message}')
    DELETE_MESSAGE                    = (Methods.DELETE, CHANNEL + '/messages/{message}')
    BULK_DELETE_MESSAGES              = (Methods.POST, CHANNEL + '/messages/bulk-delete')
    EDIT_CHANNEL_PERMISSIONS          = (Methods.PUT, CHANNEL + '/permissions/{permission}')
    GET_CHANNEL_INVITES               = (Methods.GET, CHANNEL + '/invites')
    CREATE_CHANNEL_INVITE             = (Methods.POST, CHANNEL + '/invites')
    DELETE_CHANNEL_PERMISSION         = (Methods.DELETE, CHANNEL + '/permissions/{permission}')
    TRIGGER_TYPING_INDICATOR          = (Methods.POST, CHANNEL + '/typing')
    GET_PINNED_MESSAGES               = (Methods.GET, CHANNEL + '/pins')
    ADD_PINNED_CHANNEL_MESSAGE        = (Methods.PUT, CHANNEL + '/pins/{message}')
    DELETE_PINNED_CHANNEL_MESSAGE     = (Methods.DELETE, CHANNEL + '/pins/{message}')
    GROUP_DM_ADD_RECIPIENT            = (Methods.PUT, CHANNEL + '/recipients/{user}')
    GROUP_DM_REMOVE_RECIPIENT         = (Methods.DELETE, CHANNEL + '/recipients/{user}')

    # Audit Log
    GET_GUILD_AUDIT_LOG               = (Methods.GET, GUILD + '/audit-logs')

    # Emoji
    EMOJI                             = '/emojis'
    LIST_GUILD_EMOJIS                 = (Methods.GET, GUILD + EMOJI)
    GET_GUILD_EMOJI                   = (Methods.GET, GUILD + EMOJI + '/{emoji}')
    CREATE_GUILD_EMOJI                = (Methods.POST, GUILD + EMOJI)
    MODIFY_GUILD_EMOJI                = (Methods.PATCH, GUILD + EMOJI + '/{emoji}')
    DELETE_GUILD_EMOJI                = (Methods.DELETE, GUILD + EMOJI + '/{emoji}')

    # Invite
    INVITE                            = '/invites/{invite}'
    GET_INVITE                        = (Methods.GET, INVITE)
    DELETE_INVITE                     = (Methods.DELETE, INVITE)

    # User
    USER                              = '/users'
    GET_CURRENT_USER                  = (Methods.GET, USER + '/@me')
    GET_USER                          = (Methods.GET, USER + '/{user}')
    MODIFY_CURRENT_USER               = (Methods.PATCH, USER + '/@me')
    GET_CURRENT_USER_GUILDS           = (Methods.GET, USER + '/@me/guilds')
    LEAVE_GUILD                       = (Methods.DELETE, USER + '/@me/guilds/{guild}')
    GET_USER_DMS                      = (Methods.GET, USER + '/@me/channels')
    CREATE_DM                         = (Methods.POST, USER + '/@me/channels')
    CREATE_GROUP_DM                   = (Methods.POST, USER + '/@me/channels')
    GET_USER_CONNECTIONS              = (Methods.GET, USER + '/@me/connections')

    # Voice
    VOICE                             = '/voice'
    LIST_VOICE_REGIONS                = (Methods.GET, VOICE + '/regions')

    # Webhook
    WEBHOOK                           = '/webhooks/{webhook}'
    CREATE_WEBHOOK                    = (Methods.POST, CHANNEL + '/webhooks')
    GET_CHANNEL_WEBHOOKS              = (Methods.GET, CHANNEL + '/webhooks')
    GET_GUILD_WEBHOOKS                = (Methods.GET, GUILD + '/webhooks')
    GET_WEBHOOK                       = (Methods.GET, WEBHOOK)
    GET_WEBHOOK_WITH_TOKEN            = (Methods.GET, WEBHOOK + '/{token}')
    MODIFY_WEBHOOK                    = (Methods.PATCH, WEBHOOK)
    MODIFY_WEBHOOK_WITH_TOKEN         = (Methods.PATCH, WEBHOOK + '/{token}')
    DELETE_WEBHOOK                    = (Methods.DELETE, WEBHOOK)
    DELETE_WEBHOOK_WITH_TOKEN         = (Methods.DELETE, WEBHOOK + '/{token}')
    EXECUTE_WEBHOOK                   = (Methods.POST, WEBHOOK + '/{token}')
    EXECUTE_SLACK_COMPATIBLE_WEBHOOK  = (Methods.POST, WEBHOOK + '/{token}/slack')
    EXECUTE_GITHUB_COMPATIBLE_WEBHOOK = (Methods.POST, WEBHOOK + '/{token}/github')

    # OAuth2
    OAUTH                             = '/oauth2/applications'
    GET_CURRENT_APPLICATION_INFO      = (Methods.GET, OAUTH + '/@me')

    # Gateway
    GATEWAY                           = '/gateway'
    GET_GATEWAY                       = (Methods.GET, GATEWAY)
    GET_GATEWAY_BOT                   = (Methods.GET, GATEWAY + '/bot')
