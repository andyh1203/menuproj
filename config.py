import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secretlolz'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(basedir,
                                                 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
