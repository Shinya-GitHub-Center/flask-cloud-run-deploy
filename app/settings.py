import os

basedir = os.path.dirname(os.path.dirname(__file__))
dbdir = basedir + "/db"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(dbdir, "blogpost.sqlite")
SECRET_KEY = os.urandom(10)

USERNAME = "admin"
PASSWORD = "0000"
