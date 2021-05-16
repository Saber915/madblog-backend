from flask import request, jsonify, url_for
import re

from app.api.errors import bad_request
from app.api import bp
from app.models import User
from app import db


@bp.route('/users', methods=['POST'])
def create_user():
    """注册用户"""
    data = request.get_json()
    if not data:
        return bad_request("You must post json data.")
    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
def get_users():
    """返货所有的用户列表"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    """返回一个用户"""

    return jsonify(User.query.get_or_404(uid).to_dict())


@bp.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    """修改一个用户"""


@bp.route('/users/<uid>', methods=['DELETE'])
def delete_user(uid):
    """删除一个用户"""
