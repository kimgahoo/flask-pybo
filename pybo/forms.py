# 질문등록 폼 클래스
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    ''' 질문 폼 클래스 > 모델 클래스의 속성은 비슷'''
        # Flask-WTF 모듈의 FlaskForm 클래스를 상속 받음
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
        # 제목은 폼 라벨로 사용
        # 템플릿에서 이 값으로 라벨을 출력할수 있다. 라벨이 뭔데????
        # validators >> 필드값 검증
        # 필수 항목인지 검증하는 >> DataRequired
        # 이메일인지 검증하는 Eamil
        # 길이를 점검하는 Length 등이 있다.
        ### 필수값이면서, 이메일 이어야 한다면 >> validators=[DataRequired(), Email()]
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    # 회원가입 폼
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])   # EqualTo 검증을 추가
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    ''' 로그인 폼 '''
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])
    
        







'''
    이메일 검증 설치 해야한다
    email-validator 설치하기
    pip install email_validator
'''