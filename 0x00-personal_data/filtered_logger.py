#!/usr/bin/env python3
"""
function called filter_datum
that returns the log message obfuscated:
"""

from typing import List
import re
import logging
from os import environ
import mysql.connector

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    uses regex to redact sensitve
    information from a log message
    """
    for i in fields:
        message = re.sub(f"{i}=.*?{separator}",
                         f"{i}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        initialize arguments
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format records by redacting sensitive info
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object.
    """
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter.format()
    return user_data


def get_db():
    """
    setting up db connection
    """
    db_config = {
        "host": environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        "user": environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        "database": environ.get("PERSONAL_DATA_DB_NAME")
    }
    connection = mysql.connector.connection.MySQLConnection(**db_config)

    return connection


def main():
    """
    retrieve and fromat data in db
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()
