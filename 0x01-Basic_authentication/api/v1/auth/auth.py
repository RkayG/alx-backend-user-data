#!/usr/bin/env python3
"""Our base authentication class to inherit from"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Our base Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the url requires authentication
        Args:
            path (str): the path to check
            excluded_paths (List[str]): These don't ned auth
        Returns:
            bool: True or False
        """
        if not path or not excluded_paths:
            return True
        for m in excluded_paths:
            if m.endswith('*'):
                if path.startswith(m[:-1]):
                    return False
        if path[-1] != "/":
            path += '/'
        tocheck = [i + '/' if i[-1] != '/' else i for i in excluded_paths]
        if path in tocheck:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks if a header is authorized
        Args:
            request (request, optional):
                The request to be made. Defaults to None.
        Returns:
            str: the headers or None
        """
        if not request or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Does nothing. Meant to be overidden when inherited
        """
        return None
