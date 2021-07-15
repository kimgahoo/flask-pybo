# 회원가입 뷰

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
                # generate_password_hash는 암호화하여 저장 >> 복호화 안됨
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')    # flash는 피드 자체 오류가 아닌 프로그램 논리 오류를 발생시킨다.
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request      # before_app_request :  라우트 함수보다 먼저 실행됨
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None       
            # g는 플라스크가 제공하는 컨텍스트 변수
            # g 변수는 , 요청 => 응답 과정에서 유효하다
    else:
        g.user = User.query.get(user_id)
            # session 변수에 user_id 값이 있으면, db에서 이를 조회 하여 g.user 에 저장한다
            # 그럼 이후 사용자 로그인 검사를 할때, session 조사할 필요가 없다
            # g.user 값이 있는지만 알아내면 된다.
            # g.user에는 User 객체가 저장되어 있어, 여러가지 다른 사용자 정보를 얻어내는 이점있다.

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
