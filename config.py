import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # -------------------------
    # Flask
    # -------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # -------------------------
    # Azure Blob Storage
    # -------------------------
    BLOB_ACCOUNT = os.environ.get("BLOB_ACCOUNT")
    BLOB_STORAGE_KEY = os.environ.get("BLOB_STORAGE_KEY")
    BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")

    # -------------------------
    # Azure SQL Database
    # -------------------------
    SQL_SERVER = os.environ.get("SQL_SERVER")
    SQL_DATABASE = os.environ.get("SQL_DATABASE")
    SQL_USER_NAME = os.environ.get("SQL_USER_NAME")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://"
        + SQL_USER_NAME
        + "@"
        + SQL_SERVER
        + ":"
        + SQL_PASSWORD
        + "@"
        + SQL_SERVER
        + ":1433/"
        + SQL_DATABASE
        + "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------
    # Microsoft Entra ID (OAuth)
    # -------------------------
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    AUTHORITY = "https://login.microsoftonline.com/common"
    REDIRECT_PATH = "/getAToken"

    SCOPE = ["User.Read"]

    # -------------------------
    # Session
    # -------------------------
    SESSION_TYPE = "filesystem"
