#!/usr/bin/env python3
"""A session auth that saves to DB"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Our db session authentication"""
    def create_session(self, user_id=None) -> str:
        """Creates a new session and saves it to
        the database"""
        if not user_id:
            return None
        ses_id = super().create_session(user_id)
        session = UserSession(user_id=user_id, session_id=ses_id)
        session.save()
        return ses_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Overloads the parent class method to search for
        the session in the database"""
        # sess = super().user_id_for_session_id(session_id)
        if not session_id:
            return None
        session = UserSession().search(
            {'session_id': session_id})
        if not session:
            return None
        return session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Overloads the parent class method to
        destroy the class in the database"""
        # val = super().destroy_session(request)
        # if val:
        #     return val
        if not request:
            return False
        session = self.session_cookie(request)
        if not session:
            return False
        curr = UserSession().search(
            {'session_id': session})
        if not curr or curr == []:
            return False
        curr[0].remove()
        return True
