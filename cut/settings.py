import os
import string


USER_SHORT_LINK_LENGTH = 16
DEFAULT_SHORT_LINK_LENGTH = 6
REG_PATTERN = '^[A-Za-z0-9]*$'
LETTERS_AND_DIGITS = string.ascii_letters + string.digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY',
                           default='1234test4321')
