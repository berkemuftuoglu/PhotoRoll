import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'|\xb8R\xa5\x9fu\x14W\x8f\xb4\x14\xdd\xc8\xb6\x1c\xa3'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///photoroll.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    '''MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@gmail.com'  # Replace with your Gmail address
    MAIL_PASSWORD = 'your_password'  # Replace with your Gmail password'''
