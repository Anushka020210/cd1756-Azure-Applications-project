from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from azure.storage.blob import BlobServiceClient
import string, random
from werkzeug.utils import secure_filename
from flask import flash

# ===============================
# Azure Blob Setup
# ===============================
blob_container = app.config.get("BLOB_CONTAINER")
connection_string = app.config.get("BLOB_CONNECTION_STRING")

if not connection_string or not blob_container:
    raise RuntimeError("Azure Blob Storage is not configured properly")

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(blob_container)


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_changes(self, form, file, userId, new=False):
        self.title = form.title.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = userId

        if file:
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1]
            filename = f"{id_generator()}.{extension}"

            try:
                blob_client = container_client.get_blob_client(filename)
                blob_client.upload_blob(file, overwrite=True)

                if self.image_path:
                    container_client.delete_blob(self.image_path)

                self.image_path = filename

            except Exception as e:
                flash(str(e))

        if new:
            db.session.add(self)

        db.session.commit()
