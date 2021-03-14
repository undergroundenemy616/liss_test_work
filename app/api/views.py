from . import api
from functools import wraps
from flask_restful import Api, Resource
from flask import request, make_response, jsonify
from app.api.models import User, Post, Comment
from app.api.schemas import UserSchema, PostSchema, CommentSchema
from marshmallow import ValidationError
from .. import db


api = Api(api)


def auth_requeired(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        user = User.query.filter_by(username=auth.username).first()
        if auth and user and user.verify_password(auth.password):
            return f(*args, **kwargs)
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return wrapper


class SignIn(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        if User.query.filter_by(email=data['email']).first() is not None or User.query.filter_by(username=data['email']).first() is not None:
            return make_response('User with this username or email already exists', 409)
        user = User(email=data['email'], username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201


class PostList(Resource):
    method_decorators = {'post': [auth_requeired]}

    def get(self):
        posts = Post.query.all()
        json_posts = PostSchema().dump(posts, many=True)
        return json_posts, 200

    def post(self):
        json_data = request.get_json()
        try:
            data = PostSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        author = User.query.filter_by(username=request.authorization.username).first()
        post = Post(title=data['title'], content=data['content'], author=author.id)

        db.session.add(post)
        db.session.commit()
        return PostSchema().dump(post), 201


class PostDetail(Resource):
    method_decorators = {'put': [auth_requeired], 'delete': [auth_requeired]}

    def get(self, id):
        post = Post.query.get_or_404(id)
        json_post = jsonify(PostSchema().dump(post))
        return make_response(json_post, 200)

    def put(self, id):
        post = Post.query.get_or_404(id)
        json_data = request.get_json()
        if post.user.username != request.authorization.username:
            return 'Forbidden', 403
        try:
            update_post = PostSchema().load(json_data, partial=True)
            if 'title' in update_post:
                post.title = update_post['title']
            if 'content' in update_post:
                post.content = update_post['content']
        except ValidationError as err:
            return err.messages, 422
        db.session.commit()
        return 'Successfully updated', 200

    def delete(self, id):
        post = Post.query.get_or_404(id)
        if post.user.username != request.authorization.username:
            return 'Forbidden', 403
        db.session.delete(post)
        db.session.commit()
        return 'Deleted', 204


class CommentList(Resource):
    method_decorators = {'post': [auth_requeired]}

    def get(self):
        comments = Comment.query.all()
        json_comments = CommentSchema().dump(comments, many=True)
        return json_comments, 200

    def post(self):
        json_data = request.get_json()
        try:
            data = CommentSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        author = User.query.filter_by(username=request.authorization.username).first()
        comment = Comment(title=data['title'], content=data['content'], author=author.id, post=data['post'])
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment), 201


class CommentDetail(Resource):
    method_decorators = {'put': [auth_requeired], 'delete': [auth_requeired]}

    def get(self, id):
        comment = Comment.query.get_or_404(id)
        json_comment = PostSchema().dump(comment)
        return json_comment, 200

    def put(self, id):
        comment = Comment.query.get_or_404(id)
        if comment.user.username != request.authorization.username:
            return 'Forbidden', 403
        json_data = request.get_json()
        try:
            update_comment = CommentSchema().load(json_data, partial=True)
            if 'title' in update_comment:
                comment.title = update_comment['title']
            if 'content' in update_comment:
                comment.content = update_comment['content']
        except ValidationError as err:
            return err.messages, 422
        db.session.commit()
        return 'Successfully updated', 200

    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        if comment.user.username != request.authorization.username:
            return 'Forbidden', 403
        db.session.delete(comment)
        db.session.commit()
        return 'Deleted', 204


api.add_resource(SignIn, '/sign-in')
api.add_resource(PostList, '/posts')
api.add_resource(PostDetail, '/post/<int:id>')
api.add_resource(CommentList, '/comments')
api.add_resource(CommentDetail, '/comment/<int:id>')
