from pybo import db

# db == SQLAlchemy() >> db.Model 이라는 걸 제공함

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)
    # 테이블 객체(question_voter)란 , 다대다 관계를 정의하려고, db.Table 클래스로 정의되는 객체를 말한다
    # question_voter는 , user_id와 question_id 둘다 기본키이므로, 다대다 관계가 성립됨

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):   # 질문 모델
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user.id 는 User의 id야
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    # secondary 설정은 > voter가 다대다 관계이며
    # question_voter 테이블 참조함
    # 만약 어떤 계정이 a_user라는 객체로 참조되면 > a_user.question_voter_set 으로 , 해당 계정이 "추천한 질문 리스트" 구할수있게해줌
    # backhref 설정에 사용하는 이름 중복 사용하면 안됨


class Answer(db.Model):     # 답변 모델
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # db.ForeignKey(연결할 모델의 속성명, ondelete 삭제 연동설정)
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    # db.relationship('참조할 모델명', 역참조설정)
    # 역참조 : 예를 들어 어떤 질문에 해당하는 객체가 a_question이라면 a_question.answer_set와 같은 코드로 해당 질문에 달린 답변을 참조할 수 있다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class User(db.Model):       # 회원가입 모델 db
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)   # 댓글 작성자
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)      # 댓글 내용
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    # 댓글의 질문 (Question 모델과 관계를 가짐)
    # 질문에 댓글을 작성하면 question_id 필드에 값이 저장되고
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))
    # 댓글의 답변(Answer 모델과 관계를 가짐)
    # 답변에 댓글이 작성되면 answer_id 필드에 값이 저장



'''
    db모델을 수정하면, 
    리비전 파일을 새로 생성 >> flask db migrate
    리비전 파일을 데이터베이스로 변경 >> flask db upgrade
'''

