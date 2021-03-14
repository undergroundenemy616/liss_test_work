import marshmallow_sqlalchemy as ma
from .models import User, Post, Comment


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
    author = ma.auto_field(dump_only=True)


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True
    author = ma.auto_field(dump_only=True)
