import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import UserInformation
from models import db_session
import uuid
import datetime

bp = Blueprint('auth', __name__, url_prefix='/v1/user')


@bp.route('/create', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_uuid = uuid.uuid4()
        username = request.json['username']
        password = request.json['password']
        fullname = request.json['fullname']
        role = request.json['role']
        age = request.json['age']
        sex = request.json['sex']
        UI = UserInformation()
        UI.user_uid = user_uuid
        UI.username = username
        UI.password = generate_password_hash(password)
        UI.fullname = fullname
        UI.role = role
        UI.age = age
        UI.sex = sex

        error = None

        if len(username) == 0:
            error = 'Username is required.'
        else:
            count = 0
            for s in username:
                if s.isspace():
                    count += 1
            if count > 0:
                error = 'Username must not contain spaces.'
            elif count == 0:
                check_user_exsit = db_session.query(UserInformation).filter(
                    UserInformation.username == username).first()
                if check_user_exsit is not None:
                    error = f"User {username} is already registered."
                else:
                    error = None
        if len(password) == 0:
            error = 'Password is required.'
        else:
            count = 0
            for s in password:
                if s.isspace():
                    count += 1
            if count > 0:
                error = 'Password must not contain spaces.'
        if len(fullname) == 0:
            error = 'Fullname is required.'
        if len(role) == 0:
            error = 'Role is required.'
        if len(age) == 0:
            error = 'Age is required.'
        if len(sex) == 0:
            error = 'Sex is required.'

        if error is None:
            try:
                db_session.add(UI)
                db_session.commit()
            except:
                error = f"User {username} is already registered."
            else:
                return {
                    "message": "success",
                    "data": {
                        "userInfo": {
                            "_id": user_uuid,
                            "username": username,
                            "created_at": UI.created_at,
                            "updated_at": UI.updated_at
                        }
                    }
                }
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/hash', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        error = None
        user = db_session.query(UserInformation).filter(
            UserInformation.username == username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.user_uid
            session['role'] = user.role
            return 'Login successful.'

        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(UserInformation).filter(
            UserInformation.user_uid == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    # print(session)
    return 'Logout successful.'

@bp.route('/checkSession')
def who_is_in_session():
    print(session)
    return 'Check log.'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return 'Sign in required.'

        return view(**kwargs)

    return wrapped_view


@bp.route('/password', methods=('GET', 'POST'))
@login_required
def change_pass():
    if request.method == 'POST':
        uid = request.json['uuid']
        password = request.json['password']
        error = None
        if uid == str(session['user_id']):
            user = db_session.query(UserInformation).filter(
                UserInformation.user_uid == uid).first()
            user.password = generate_password_hash(password)
            db_session.commit()
            return 'Password changed.'
        else:
            error = 'uuid does not match.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/info', methods=('GET', 'POST'))
@login_required
def check_exsit():
    if request.method == 'GET':
        if session['role'] != 'admin':
            return 'Permisson denied.'
        uid = request.json['id']
        try:
            user = db_session.query(UserInformation).filter(
                UserInformation.user_uid == uid).first()
            if user is not None:
                return {
                    "message": "success",
                    "data": {
                        "userInfo": {
                            "_id": uid,
                            # "username": user.username,
                            "fullname": user.fullname,
                            "role": user.role,
                            "age": user.age,
                            "sex": user.sex,
                            "created_at": user.created_at,
                            "updated_at": user.updated_at
                        }
                    }
                }
            else:
                return {
                    "message": "User not found.",
                }
        except:
            return 'Wrong id format.'

    return 'Wrong HTTP request methods!'

@bp.route('/editPersonalInformation', methods=('GET', 'POST'))
@login_required
def edit_personal_information():
    if request.method == 'POST':
        user = db_session.query(UserInformation).filter(
            UserInformation.user_uid == session['user_id']).first()
        if user is None:
            return "Bro, Somehow you get here but you won't be able to do anything more. Please sign up again"
        else:
            user.username = request.json['username']
            user.fullname = request.json['fullname']
            user.role = request.json['role']
            user.age = request.json['age']
            user.sex = request.json['sex']
            user.updated_at = datetime.datetime.utcnow()
            error = None

            if len(user.username) == 0:
                error = 'Username is required.'
            if len(user.fullname) == 0:
                error = 'Fullname is required.'
            if len(user.role) == 0:
                error = 'Role level is required.'
            if len(user.age) == 0:
                error = 'Age is required.'
            if len(user.sex) == 0:
                error = 'Sex is required.'

            if error is None:
                try:
                    db_session.commit()
                    return 'Edit personal information successful. Sign in again to apple change!'
                except:
                    return 'Failed to edit personal information.'
        return error

    return 'Wrong HTTP request methods!'