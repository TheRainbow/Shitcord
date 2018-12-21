# -*- coding: utf-8 -*-

import base64
import enum

__all__ = ['PlebAvatar', '_get_image_mime_type', '_create_avatar_uri_scheme', '_valid_icon_size']


class PlebAvatar(enum.IntEnum):
    # The Discord standard avatars for people without real profile pictures.
    BLURPLE = 0
    GREY    = 1
    GRAY    = 1
    GREEN   = 2
    ORANGE  = 3
    RED     = 4

    def __str__(self):
        return self.name.lower()


def _get_image_mime_type(image_data: bytes):
    """Determines the header type for an image given its byte representation."""

    if image_data.startswith(b'\xFF\xD8') and image_data.rstrip(b'\0').endswith(b'\xFF\xD9'):
        return 'image/jpeg'
    elif image_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif image_data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif image_data.startswith(b'RIFF') and image_data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise TypeError('Unsupported image type provided.')


def _create_avatar_uri_scheme(image_data: bytes):
    """Creates the Data URI Scheme for an avatar given its byte representation."""

    mime = _get_image_mime_type(image_data)
    b64 = base64.b64encode(image_data).decode('ascii')

    fmt = 'data:{mime};base64,{data}'
    return fmt.format(mime=mime, data=b64)


def _valid_icon_size(size: int):
    """Validates whether the icon is in a range between 16 and 2048."""

    return not size & (size - 1) and size in range(16, 2049)
