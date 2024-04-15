#!/usr/bin/env python3
"""A session authentication that expires"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiry Authentication class"""
    def __init__(self):
        """Initializes the session"""
        super().__init__()
        try:
            self.session_duration = int(os.environ.get('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Overloads the parent method to create a
        session and store it to the database"""
        ses_id = super().create_session(user_id)
        if not ses_id:
            return None
        data = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[ses_id] = data
        return ses_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Overloads the parent method to check if the
        session has expired"""
        if not session_id:
            return None
        data = self.user_id_by_session_id.get(session_id)
        if not data:
            return None
        if self.session_duration <= 0:
            return data.get('user_id')
        if 'created_at' not in data:
            return None
        curr = datetime.now()
        expiry = data['created_at'] + timedelta(seconds=self.session_duration)
        if expiry < curr:
            return None
        return data.get('user_id')
