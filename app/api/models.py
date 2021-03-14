from app import db
from app import bcrypt
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(30),  nullable=False)
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

    def set_password(self, pwd):
        self.password = bcrypt.generate_password_hash(pwd)

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(180), nullable=False)
    publication_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    content = db.Column(db.String(80), nullable=False)
    publication_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
