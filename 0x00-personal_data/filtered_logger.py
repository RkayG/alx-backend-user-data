#!/usr/bin/env python3
"""A custom logger"""
import logging
import re
import mysql.connector
from typing import List
from os import environ

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter data and obfuscate necessary fields"""
    for x in fields:
        message = re.sub(f'{x}=.*?{separator}',
                         f"{x}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the formatter
        Args:
            fields (List[str]): the list of fields to be obsfucated
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Custom formatter for our custom logger"""
        log_msg = super().format(record)
        formatted = filter_datum(self.fields,
                                 self.REDACTION, log_msg, self.SEPARATOR)
        return formatted


def get_logger() -> logging.Logger:
    """Returns a logger object with uses out custom
    formatter and logs to standard output
    Returns:
        logging.Logger: the logger output
    """
    formatter = RedactingFormatter(list(PII_FIELDS))
    logger = logging.getLogger('user_data')
    handler = logging.StreamHandler()
    logger.propagate = False
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.MySQLConnection:
    """This establishes a connection to a specified database
    Returns:
        mysql.connector.connection: A connection
    """
    host = environ.get('PERSONAL_DATA_DB_HOST', "localhost")
    user = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db = environ.get('PERSONAL_DATA_DB_NAME', "")
    connection = mysql.connector.connection.MySQLConnection(
        host=host,
        user=user,
        password=pwd,
        database=db
    )
    return connection


def main() -> None:
    """This function reads from a database and logs it
    to the standard output
    """
    conn = get_db()
    logger = get_logger()
    cursor = conn.cursor()
    query = 'SELECT * FROM users;'
    cursor.execute(query)
    results = cursor.fetchall()
    fields = ['name', 'email', 'phone', 'ssn', 'password',
              'ip', 'last_login', 'user_agent']
    for x in results:
        message = "; ".join(f'{key}={val}' for key, val in zip(fields, x))
        logger.info(message)


if __name__ == '__main__':
    main()
