import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'moments.db')

# WTF forms
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Bcrypt
BCRYPT_LOG_ROUNDS = 12
