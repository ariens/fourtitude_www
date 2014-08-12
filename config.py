import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(25)
SECRET_KEY = os.urandom(25)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'mail.layerzero.ca'
MAIL_PORT = 587 
MAIL_USERNAME = 'debug@ariens.ca'
MAIL_PASSWORD = os.environ['DEBUG_MAIL_PASSWORD']
MAIL_USE_SSL = False
MAIL_USE_TLS = True

# administrator list
ADMINS = ['dave@ariens.ca']

# email activation settings
ACTIVATION_CODE_VALID_FOR_SECONDS = 86400
