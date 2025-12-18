import os

class Config(object):

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Azure SQL - Get values from environment
    SQL_SERVER = os.environ.get("SQL_SERVER", "")
    SQL_DATABASE = os.environ.get("SQL_DATABASE", "")
    SQL_USER_NAME = os.environ.get("SQL_USER_NAME", "")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD", "")

    # Build Azure SQL connection string properly
    if all([SQL_SERVER, SQL_DATABASE, SQL_USER_NAME, SQL_PASSWORD]):
        # For Azure SQL Database, ensure server includes .database.windows.net
        if not SQL_SERVER.endswith('.database.windows.net'):
            SQL_SERVER = f"{SQL_SERVER}.database.windows.net"
        
        # Build connection string with Azure-specific parameters
        SQLALCHEMY_DATABASE_URI = (
            "mssql+pyodbc://"
            + SQL_USER_NAME
            + ":"
            + SQL_PASSWORD
            + "@"
            + SQL_SERVER
            + ":1433/"
            + SQL_DATABASE
            + "?driver=ODBC+Driver+17+for+SQL+Server"
            + "&Encrypt=yes"               # Required for Azure SQL
            + "&TrustServerCertificate=no" # Don't trust self-signed certs
            + "&Connection+Timeout=30"     # Timeout after 30 seconds
            + "&authentication=ActiveDirectoryPassword"  # If using AAD auth
        )
    else:
        # Fallback to SQLite for local development
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
        print("⚠️  Using SQLite fallback. Azure SQL connection not configured.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Azure Blob Storage
    BLOB_ACCOUNT = os.environ.get("BLOB_ACCOUNT", "")
    BLOB_STORAGE_KEY = os.environ.get("BLOB_STORAGE_KEY", "")
    BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER", "default-container")

    # Microsoft OAuth
    CLIENT_ID = os.environ.get("CLIENT_ID", "")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "")
    AUTHORITY = "https://login.microsoftonline.com/common"
    REDIRECT_PATH = "/getAToken"
    SCOPE = ["User.Read"]

    # Flask Session
    SESSION_TYPE = "filesystem"
