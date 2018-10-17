# -*- coding: utf-8 -*-

import logging
from .http import HTTP
from .routes import Endpoints
from gevent.local import local
import json
from contextlib import contextmanager
from urllib.parse import quote

logger = logging.getLogger(__name__)


class API:
    """This represents an API client for making requests to the Discord REST API."""

    def __init__(self, token):
        self.http = HTTP(token)
        self._cache = local()

    def make_request(self, route, fmt=None, **kwargs):
        """This will actually be used for HTTP requests to the Discord API."""

        response = self.http.make_request(route, fmt, **kwargs)
        self._capture_response(response)

        return response

    def _capture_response(self, response):
        if not hasattr(self._cache, 'responses'):
            self._cache.responses = []

        self._cache.responses.append(response)
        logger.debug('Added response {} to cache.'.format(response))

    @contextmanager
    def raw_responses(self):
        """
        A Context Manager that captures all responses from the requests that were made.
        It can be used to view raw API responses for example.

        PLEASE DO ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING!
        """

        responses = self._cache.responses

        try:
            yield responses
        finally:
            delattr(self._cache, 'responses')

    @staticmethod
    def _optional(**kwargs):
        return {key: value for key, value in kwargs.items() if value is not None}

    def _reason_header(self, reason):
        return self._optional(**{'X-Audit-Log-Reason': quote(reason, safe='/ ') if reason else None})

    # ----------------------------------- Guild ----------------------------------- #

    def create_guild(self,
                     name,
                     region,
                     icon=None,
                     verification_level=0,
                     default_message_notifications=0,
                     explicit_content_filter=2,
                     roles=None,
                     channels=None):
        payload = {
            'name': name,
            'region': region,
            'verification_level': verification_level,
            'default_message_notifications': default_message_notifications,
            'explicit_content_filter': explicit_content_filter,
        }

        payload.update(self._optional(icon=icon, roles=roles, channels=channels))

        return self.make_request(Endpoints.CREATE_GUILD, json=payload)

    def get_guild(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD, dict(guild=guild_id))

    def modify_guild(self,
                     guild_id,
                     name=None,
                     region=None,
                     verification_level=None,
                     default_message_notifications=None,
                     explicit_content_filter=None,
                     afk_channel_id=None,
                     afk_timeout=None,
                     icon=None,
                     owner_id=None,
                     splash=None,
                     system_channel_id=None,
                     reason=None):
        return self.make_request(Endpoints.MODIFY_GUILD, dict(guild=guild_id), headers=self._reason_header(reason), json=self._optional(
            name=name,
            region=region,
            verification_level=verification_level,
            default_message_notifications=default_message_notifications,
            explicit_content_filter=explicit_content_filter,
            afk_channel_id=afk_channel_id,
            afk_timeout=afk_timeout,
            icon=icon,
            owner_id=owner_id,
            splash=splash,
            system_channel_id=system_channel_id,
        ))

    def delete_guild(self, guild_id):
        return self.make_request(Endpoints.DELETE_GUILD, dict(guild=guild_id))

    def get_guild_channels(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_CHANNELS, dict(guild=guild_id))

    def create_guild_channel(self,
                             guild_id,
                             name,
                             channel_type=None,
                             topic=None,
                             bitrate=None,
                             user_limit=None,
                             permission_overwrites=None,
                             parent_id=None,
                             nsfw=None,
                             reason=None):
        payload = {
            'name': name
        }.update(self._optional(
            type=channel_type,
            topic=topic,
            bitrate=bitrate,
            user_limit=user_limit,
            permission_overwrites=permission_overwrites,
            parent_id=parent_id,
            nsfw=nsfw
        ))

        return self.make_request(Endpoints.CREATE_GUILD_CHANNEL, dict(guild=guild_id), headers=self._reason_header(reason), json=payload)

    def modify_guild_channel_positions(self, guild_id, channel_id, position, reason=None):
        payload = {
            'id': channel_id,
            'position': position,
        }

        return self.make_request(Endpoints.MODIFY_GUILD_CHANNEL_POSITIONS, dict(guild=guild_id), headers=self._reason_header(reason), json=payload)

    def get_guild_member(self, guild_id, user_id):
        return self.make_request(Endpoints.GET_GUILD_MEMBER, dict(guild=guild_id, user=user_id))

    def list_guild_members(self, guild_id, limit=None, after=None):
        return self.make_request(Endpoints.LIST_GUILD_MEMBERS, dict(guild=guild_id), params=self._optional(
            limit=limit,
            after=after,
        ))

    def add_guild_member(self, guild_id, user_id, access_token, nick=None, roles=None, mute=None, deaf=None):
        payload = {
            'access_token': access_token,
        }.update(self._optional(
            nick=nick,
            roles=roles,
            mute=mute,
            deaf=deaf,
        ))

        return self.make_request(Endpoints.ADD_GUILD_MEMBER, dict(guild=guild_id, user=user_id), json=payload)

    def modify_guild_member(self, guild_id, user_id, nick=None, roles=None, mute=None, deaf=None, channel_id=None, reason=None):
        return self.make_request(Endpoints.MODIFY_GUILD_MEMBER, dict(guild=guild_id, user=user_id), headers=self._reason_header(reason),
                                 json=self._optional(
            nick=nick,
            roles=roles,
            mute=mute,
            deaf=deaf,
            channel_id=channel_id
        ))

    def modify_current_user_nick(self, guild_id, nick):
        return self.make_request(Endpoints.MODIFY_CURRENT_USER_NICK, dict(guild=guild_id), json={'nick': nick})

    def add_guild_member_role(self, guild_id, user_id, role_id, reason=None):
        return self.make_request(Endpoints.ADD_GUILD_MEMBER_ROLE, dict(guild=guild_id, user=user_id, role=role_id),
                                 headers=self._reason_header(reason))

    def remove_guild_member_role(self, guild_id, user_id, role_id, reason=None):
        return self.make_request(Endpoints.REMOVE_GUILD_MEMBER_ROLE, dict(guild=guild_id, user=user_id, role=role_id),
                                 headers=self._reason_header(reason))

    def remove_guild_member(self, guild_id, user_id, reason=None):
        return self.make_request(Endpoints.REMOVE_GUILD_MEMBER, dict(guild=guild_id, user=user_id), headers=self._reason_header(reason))

    def get_guild_bans(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_BANS, dict(guild=guild_id))

    def get_guild_ban(self, guild_id, user_id):
        return self.make_request(Endpoints.GET_GUILD_BAN, dict(guild=guild_id, user=user_id))

    def create_guild_ban(self, guild_id, user_id, delete_message_days=0, reason=None):
        payload = {
            'delete-message-days': delete_message_days,
            'reason': reason,
        }

        return self.make_request(Endpoints.CREATE_GUILD_BAN, dict(guild=guild_id, user=user_id), headers=self._reason_header(reason), params=payload)

    def remove_guild_ban(self, guild_id, user_id, reason=None):
        return self.make_request(Endpoints.REMOVE_GUILD_BAN, dict(guild=guild_id, user=user_id), headers=self._reason_header(reason))

    def get_guild_roles(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_ROLES, dict(guild=guild_id))

    def create_guild_role(self, guild_id, name=None, permissions=None, color=None, hoist=None, mentionable=None, reason=None):
        return self.make_request(Endpoints.CREATE_GUILD_ROLE, dict(guild=guild_id), headers=self._reason_header(reason), json=self._optional(
            name=name,
            permissions=permissions,
            color=color,
            hoist=hoist,
            mentionable=mentionable
        ))

    def modify_guild_role_positions(self, guild_id, role_id, position, reason=None):
        payload = {
            'id': role_id,
            'position': position,
        }

        return self.make_request(Endpoints.MODIFY_GUILD_ROLE_POSITIONS, dict(guild=guild_id), headers=self._reason_header(reason), json=payload)

    def modify_guild_role(self, guild_id, role_id, name=None, permissions=None, color=None, hoist=None, mentionable=None, reason=None):
        payload = self._optional(
            name=name,
            permissions=permissions,
            color=color,
            hoist=hoist,
            mentionable=mentionable,
        )

        return self.make_request(Endpoints.MODIFY_GUILD_ROLE, dict(guild=guild_id, role=role_id), headers=self._reason_header(reason), json=payload)

    def delete_guild_role(self, guild_id, role_id, reason=None):
        return self.make_request(Endpoints.DELETE_GUILD_ROLE, dict(guild=guild_id, role=role_id), headers=self._reason_header(reason))

    def get_guild_prune_count(self, guild_id, days=None):
        return self.make_request(Endpoints.GET_GUILD_PRUNE_COUNT, dict(guild=guild_id), params=self._optional(days=days))

    def begin_guild_prune(self, guild_id, days=None):
        return self.make_request(Endpoints.BEGIN_GUILD_PRUNE, dict(guild=guild_id), params=self._optional(days=days))

    def get_guild_voice_regions(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_VOICE_REGIONS, dict(guild=guild_id))

    def get_guild_invites(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_INVITES, dict(guild=guild_id))

    def get_guild_integrations(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_INTEGRATIONS, dict(guild=guild_id))

    def create_guild_integration(self, guild_id, integration_type, integration_id):
        payload = {
            'type': integration_type,
            'id': integration_id,
        }

        return self.make_request(Endpoints.CREATE_GUILD_INTEGRATION, dict(guild=guild_id), json=payload)

    def modify_guild_integration(self, guild_id, integration_id, expire_behavior=None, expire_grace_period=None, enable_emoticons=None):
        return self.make_request(Endpoints.MODIFY_GUILD_INTEGRATION, dict(guild=guild_id, integration=integration_id), json=self._optional(
            expire_behavior=expire_behavior,
            expire_grace_period=expire_grace_period,
            enable_emoticons=enable_emoticons,
        ))

    def delete_guild_integration(self, guild_id, integration_id):
        return self.make_request(Endpoints.DELETE_GUILD_INTEGRATION, dict(guild=guild_id, integration=integration_id))

    def sync_guild_integration(self, guild_id, integration_id):
        return self.make_request(Endpoints.SYNC_GUILD_INTEGRATION, dict(guild=guild_id, integration=integration_id))

    def get_guild_embed(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_EMBED, dict(guild=guild_id))

    def modify_guild_embed(self, guild_id, enabled=None, channel_id=None):
        return self.make_request(Endpoints.MODIFY_GUILD_EMBED, dict(guild=guild_id), json=self._optional(
            enabled=enabled,
            channel_id=channel_id,
        ))

    def get_guild_vanity_url(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_VANITY_URL, dict(guild=guild_id))

    # ----------------------------------- Channel ----------------------------------- #

    def get_channel(self, channel_id):
        return self.make_request(Endpoints.GET_CHANNEL, dict(channel=channel_id))

    def modify_channel(self,
                       channel_id,
                       name=None,
                       position=None,
                       topic=None,
                       nsfw=None,
                       rate_limit_per_user=None,
                       bitrate=None,
                       user_limit=None,
                       permission_overwrites=None,
                       parent_id=None,
                       reason=None):
        return self.make_request(Endpoints.MODIFY_CHANNEL, dict(channel=channel_id), headers=self._reason_header(reason), json=self._optional(
            name=name,
            position=position,
            topic=topic,
            nsfw=nsfw,
            rate_limit_per_user=rate_limit_per_user,
            bitrate=bitrate,
            user_limit=user_limit,
            permission_overwrites=permission_overwrites,
            parent_id=parent_id,
        ))

    def delete_channel(self, channel_id, reason=None):
        return self.make_request(Endpoints.DELETE_CHANNEL, dict(channel=channel_id), headers=self._reason_header(reason))

    def get_channel_messages(self, channel_id, around=None, before=None, after=None, limit=None):
        return self.make_request(Endpoints.GET_CHANNEL_MESSAGES, dict(channel=channel_id), params=self._optional(
            around=around,
            before=before,
            after=after,
            limit=limit,
        ))

    def get_channel_message(self, channel_id, message_id):
        return self.make_request(Endpoints.GET_CHANNEL_MESSAGE, dict(channel=channel_id, message=message_id))

    def create_message(self, channel_id, content=None, nonce=None, tts=False, files=None, embed=None):
        payload = {
            'nonce': nonce,
            'tts': tts
        }

        if content:
            payload['content'] = content

        if embed:
            payload['embed'] = embed

        if files:
            if len(files) == 1:
                attachments = {
                    'file': tuple(files[0]),
                }
            else:
                attachments = {
                    'file{}'.format(index): tuple(file) for index, file in enumerate(files)
                }

            return self.make_request(Endpoints.CREATE_MESSAGE, dict(channel=channel_id), files=attachments,
                                     data={'payload_json': json.dumps(payload)})

        return self.make_request(Endpoints.CREATE_MESSAGE, dict(channel=channel_id), json=payload)

    def create_reaction(self, channel_id, message_id, unicode):
        return self.make_request(Endpoints.CREATE_REACTION, dict(channel=channel_id, message=message_id, emoji=unicode))

    def delete_own_reaction(self, channel_id, message_id, unicode):
        return self.make_request(Endpoints.DELETE_OWN_REACTION, dict(channel=channel_id, message=message_id, emoji=unicode))

    def delete_user_reaction(self, channel_id, message_id, unicode, user_id):
        return self.make_request(Endpoints.DELETE_USER_REACTION, dict(channel=channel_id, message=message_id, emoji=unicode, user=user_id))

    def get_reactions(self, channel_id, message_id, unicode):
        return self.make_request(Endpoints.GET_REACTIONS, dict(channel=channel_id, message=message_id, emoji=unicode))

    def delete_all_reactions(self, channel_id, message_id):
        return self.make_request(Endpoints.DELETE_ALL_REACTIONS, dict(channel=channel_id, message=message_id))

    def edit_message(self, channel_id, message_id, content=None, embed=None):
        return self.http.make_request(Endpoints.EDIT_MESSAGE, dict(channel=channel_id, message=message_id), json=self._optional(
            content=content,
            embed=embed
        ))

    def delete_message(self, channel_id, message_id):
        return self.http.make_request(Endpoints.DELETE_MESSAGE, dict(channel=channel_id, message=message_id))

    def bulk_delete_messages(self, channel_id, messages=None):
        return self.http.make_request(Endpoints.BULK_DELETE_MESSAGES, dict(channel=channel_id), json=self._optional(messages=messages))

    def edit_channel_permissions(self, channel_id, overwrite_id, allow=None, deny=None, permissions_type=None, reason=None):
        return self.http.make_request(Endpoints.EDIT_CHANNEL_PERMISSIONS, dict(channel=channel_id, permissions=overwrite_id),
                                      headers=self._reason_header(reason), json=self._optional(
            allow=allow,
            deny=deny,
            type=permissions_type,
        ))

    def get_channel_invites(self, channel_id):
        return self.make_request(Endpoints.GET_CHANNEL_INVITES, dict(channel=channel_id))

    def create_channel_invite(self, channel_id, max_age=None, max_uses=None, temporary=None, unique=None):
        return self.make_request(Endpoints.CREATE_CHANNEL_INVITE, dict(channel=channel_id), json=self._optional(
            max_age=max_age,
            max_uses=max_uses,
            temporary=temporary,
            unique=unique,
        ))

    def delete_channel_permission(self, channel_id, overwrite_id, reason=None):
        return self.make_request(Endpoints.DELETE_CHANNEL_PERMISSION, dict(channel=channel_id, permission=overwrite_id),
                                 headers=self._reason_header(reason))

    def trigger_typing_indicator(self, channel_id):
        return self.make_request(Endpoints.TRIGGER_TYPING_INDICATOR, dict(channel=channel_id))

    def get_pinned_messages(self, channel_id):
        return self.make_request(Endpoints.GET_PINNED_MESSAGES, dict(channel=channel_id))

    def add_pinned_channel_message(self, channel_id, message_id):
        return self.make_request(Endpoints.ADD_PINNED_CHANNEL_MESSAGE, dict(channel=channel_id, message=message_id))

    def delete_pinned_channel_message(self, channel_id, message_id):
        return self.make_request(Endpoints.DELETE_PINNED_CHANNEL_MESSAGE, dict(channel=channel_id, message=message_id))

    def group_dm_add_recipient(self, channel_id, user_id, access_token, nick=None):
        payload = {'access_token': access_token, }.update(self._optional(nick=nick))

        return self.make_request(Endpoints.GROUP_DM_ADD_RECIPIENT, dict(channel=channel_id, user=user_id), json=payload)

    def group_dm_remove_recipient(self, channel_id, user_id):
        return self.make_request(Endpoints.GROUP_DM_REMOVE_RECIPIENT, dict(channel=channel_id, user=user_id))

    # ----------------------------------- Audit Log ----------------------------------- #

    def get_guild_audit_log(self, guild_id, user_id=None, action_type=None, before=None, limit=None):
        return self.make_request(Endpoints.GET_GUILD_AUDIT_LOG, dict(guild=guild_id), params=self._optional(
            user_id=user_id,
            action_type=action_type,
            before=before,
            limit=limit,
        ))

    # ----------------------------------- Emoji ----------------------------------- #

    def list_guild_emojis(self, guild_id):
        return self.make_request(Endpoints.LIST_GUILD_EMOJIS, dict(guild=guild_id))

    def get_guild_emoji(self, guild_id, emoji_id):
        return self.make_request(Endpoints.GET_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id))

    def create_guild_emoji(self, guild_id, name, image, roles, reason=None):
        payload = {
            'name': name,
            'image': image,
            'roles': roles,
        }

        return self.make_request(Endpoints.CREATE_GUILD_EMOJI, dict(guild=guild_id), headers=self._reason_header(reason), json=payload)

    def modify_guild_emoji(self, guild_id, emoji_id, name, roles, reason=None):
        payload = {
            'name': name,
            'roles': roles,
        }

        return self.make_request(Endpoints.MODIFY_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id),
                                 headers=self._reason_header(reason), json=payload)

    def delete_guild_emoji(self, guild_id, emoji_id, reason=None):
        return self.make_request(Endpoints.DELETE_GUILD_EMOJI, dict(guild=guild_id, emoji=emoji_id), headers=self._reason_header(reason))

    # ----------------------------------- Invite ----------------------------------- #

    def get_invite(self, invite_code, with_counts=None):
        return self.make_request(Endpoints.GET_INVITE, dict(invite=invite_code), params=self._optional(with_counts=with_counts))

    def delete_invite(self, invite_code, reason=None):
        return self.make_request(Endpoints.DELETE_INVITE, dict(invite=invite_code), headers=self._reason_header(reason))

    # ----------------------------------- User ----------------------------------- #

    def get_current_user(self):
        return self.make_request(Endpoints.GET_CURRENT_USER)

    def get_user(self, user_id):
        return self.make_request(Endpoints.GET_USER, dict(user=user_id))

    def modify_current_user(self, username=None, avatar=None):
        return self.make_request(Endpoints.MODIFY_CURRENT_USER, json=self._optional(
            username=username,
            avatar=avatar,
        ))

    def get_current_user_guilds(self):
        return self.make_request(Endpoints.GET_CURRENT_USER_GUILDS)

    def leave_guild(self, guild_id):
        return self.make_request(Endpoints.LEAVE_GUILD, dict(guild=guild_id))

    def get_user_dms(self):
        return self.make_request(Endpoints.GET_USER_DMS)

    def create_dm(self, user_id):
        return self.make_request(Endpoints.CREATE_DM, json={'recipient_id': user_id})

    def create_group_dm(self, access_tokens=None, nicks=None):
        return self.make_request(Endpoints.CREATE_GROUP_DM, json=self._optional(
            access_tokens=access_tokens,
            nicks=nicks,
        ))

    def get_user_connections(self):
        return self.make_request(Endpoints.GET_USER_CONNECTIONS)

    # ----------------------------------- Voice ----------------------------------- #

    def list_voice_regions(self):
        return self.make_request(Endpoints.LIST_VOICE_REGIONS)

    # ----------------------------------- Webhook ----------------------------------- #

    def create_webhook(self, channel_id, name, avatar=None):
        if not 1 < len(name) <= 32:
            raise ValueError('Nigga, choose a fucking username between 2 and 32 characters and nothing else.')

        payload = {'name': name, }.update(self._optional(avatar=avatar))

        return self.make_request(Endpoints.CREATE_WEBHOOK, dict(channel=channel_id), json=payload)

    def get_channel_webhooks(self, channel_id):
        return self.make_request(Endpoints.GET_CHANNEL_WEBHOOKS, dict(channel=channel_id))

    def get_guild_webhooks(self, guild_id):
        return self.make_request(Endpoints.GET_GUILD_WEBHOOKS, dict(guild=guild_id))

    def get_webhook(self, webhook_id):
        return self.make_request(Endpoints.GET_WEBHOOK, dict(webhook=webhook_id))

    def get_webhook_with_token(self, webhook_id, webhook_token):
        return self.make_request(Endpoints.GET_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token))

    def modify_webhook(self, webhook_id, name=None, avatar=None, channel_id=None, reason=None):
        return self.make_request(Endpoints.MODIFY_WEBHOOK, dict(webhook=webhook_id), headers=self._reason_header(reason), json=self._optional(
            name=name,
            avatar=avatar,
            channel_id=channel_id,
        ))

    def modify_webhook_with_token(self, webhook_id, webhook_token, name=None, avatar=None):
        return self.make_request(Endpoints.MODIFY_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token), json=self._optional(
            name=name,
            avatar=avatar,
        ))

    def delete_webhook(self, webhook_id, reason=None):
        return self.make_request(Endpoints.DELETE_WEBHOOK, dict(webhook=webhook_id), headers=self._reason_header(reason))

    def delete_webhook_with_token(self, webhook_id, webhook_token):
        return self.make_request(Endpoints.DELETE_WEBHOOK_WITH_TOKEN, dict(webhook=webhook_id, token=webhook_token))

    def execute_webhook(self, webhook_id, webhook_token, content=None, username=None, avatar_url=None, tts=None, file=None, embeds=None, wait=False):
        params = {'wait': int(wait)}

        return self.make_request(Endpoints.EXECUTE_WEBHOOK, dict(webhook=webhook_id, token=webhook_token), params=params, json=self._optional(
            content=content,
            username=username,
            avatar_url=avatar_url,
            tts=tts,
            file=file,
            embeds=embeds,
        ))

    def execute_slack_compatible_webhook(self, webhook_id, webhook_token):
        return self.make_request(Endpoints.EXECUTE_SLACK_COMPATIBLE_WEBHOOK, dict(webhook=webhook_id, token=webhook_token))

    def execute_github_compatible_webhook(self, webhook_id, webhook_token):
        return self.make_request(Endpoints.EXECUTE_GITHUB_COMPATIBLE_WEBHOOK, dict(webhook=webhook_id, token=webhook_token))

    # ----------------------------------- OAuth2 ----------------------------------- #

    def get_current_application_info(self):
        return self.make_request(Endpoints.GET_CURRENT_APPLICATION_INFO)

    # ----------------------------------- Gateway ----------------------------------- #

    def get_gateway(self):
        resp = self.make_request(Endpoints.GET_GATEWAY)
        logger.debug("Received payload containing Gateway URL {}".format(resp['url']))

        if not hasattr(self._cache, 'gateway'):
            self._cache.gateway = resp['url']

        return resp

    def get_gateway_bot(self):
        return self.make_request(Endpoints.GET_GATEWAY_BOT)
