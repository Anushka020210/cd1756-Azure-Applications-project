from FlaskWebProject import app

# Azure App Service looks for "app" object
application = app

if __name__ == "__main__":
    application.run()
