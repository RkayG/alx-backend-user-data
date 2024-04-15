#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB, User, NoResultFound, InvalidRequestError
import uuid


def _hash_password(password: str) -> str:
    """This hashes a password using bcrypt
    Args:
        password (str): the password to be hashed
    Returns:
        bytes: the hashed password in bytes
    """
    pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return pwd


def _generate_uuid() -> str:
    """Generate a uuid"""
    _id = str(uuid.uuid4())
    return _id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a login"""
        try:
            pwd = password.encode()
            user = self._db.find_user_by(email=email)
            val = bcrypt.checkpw(pwd, user.hashed_password)
            return val
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Finds a user by session"""
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Creates a new reset_token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a password and resets it"""
        if not (reset_token or password):
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        pwd = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=pwd, reset_token=None
        )
