#!/usr/bin/env python3
"""Our clas for the User Session engine"""
from models.base import Base


class UserSession(Base):
    """UserSession class to handle storage of crucial
    session data"""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User Session
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
