from FlaskWebProject import app

# Azure App Service + Gunicorn needs this
if __name__ != "__main__":
    application = app
