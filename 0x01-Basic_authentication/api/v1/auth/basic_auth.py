#!/usr/bin/env python3
"""Our custom authentication class that inherits from the
Base Auth class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """Our custom Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base 64 part of the header
        Args:
            authorization_header (str): the header
        Returns:
            str: the extracted text or nothing
        """
        if not ((authorization_header) and
                (isinstance(authorization_header, str)) and
                (authorization_header.startswith('Basic '))):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
       ) -> str:
        """Decodes an encoded header
        Args:
            base64_authorization_header (str): the header
        Returns:
            str: the decoded header
        """
        if not ((base64_authorization_header) and
                (isinstance(base64_authorization_header, str))):
            return None
        try:
            val = base64.b64decode(base64_authorization_header)
            return val.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
         ) -> (str, str):
        """Extracts the user credentials from a decoded header
        """
        if not ((decoded_base64_authorization_header) and
                (isinstance(decoded_base64_authorization_header, str)) and
                (":" in decoded_base64_authorization_header)):
            return (None, None)
        val = decoded_base64_authorization_header.split(":", maxsplit=1)
        return tuple(val)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
         ) -> TypeVar('User'):
        """Returns a user object if one can be found
        based on the credentials or None"""
        if not ((user_email and user_pwd) and
                (isinstance(user_email, str) and
                 isinstance(user_pwd, str))):
            return None
        users = User().search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user at any point in time"""
        header = self.authorization_header(request)
        extracted = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(extracted)
        user_details = self.extract_user_credentials(decoded)
        curr_user = self.user_object_from_credentials(*user_details)
        return curr_user
