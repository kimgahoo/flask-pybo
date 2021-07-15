from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
    # flash 함수는 , 강제로 오류 발송시키는 함수 : 로직에 오류가 있을경우 사용
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db

from ..forms import QuestionForm, AnswerForm   # 뭐지, .. 만하면 한 스텝 위로 올라간것 뿐인데?? 아냐 이건쉬워 당연하잖아.
from pybo.views.auth_views import login_required
# from pybo.models import Question, Answer, User    아래코드와 똑같음
from ..models import Question, Answer, User, question_voter

bp = Blueprint("question", __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
        # 페이지 번호를 가져오는 놈이네 page
        # localhost:5000/question/list/?page=5 >> page 5를 보여주나봐
        # localhost:5000/question/list  >> page 값이 없으면 >> default=1을 적용

    # 조회
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    #페이징
    question_list = question_list.paginate(page, per_page=10)
        # 페저네이트 paginate
        # page : 페이지를 조회할 번호
        # per_page=10 : 페이지 마다 보여줄 게시물이 10건임
        ### paginate 함수는 , 조회할 데이터를 감싸 Pagination 객체로 반환한다
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required     # 로그인 된사용자인지 확인하는 데코레이터
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
            # form.validate_on_submit() >> 전송된 데이터의 정합성을 점검한다>> 즉, 폼을 생성할때 각필드에 지정한
            # DataRequired() 같은 점검 항목에 이상이 없는지 확인한다.
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)    # form은 , 질문을 넘겨준거지.

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':    ### POST방식으로 요청되는경우 >> 데이터를 수정한다음 <저장하기> 버튼 누를때.
        form = QuestionForm()   # 실제 저장데이터 방식폼
        if form.validate_on_submit():   # 검증하고 이상없으면 변경된 데이터 저장
            form.populate_obj(question)
                # form 변수에 들어있는데이터 == (화면에 입력되어있는 데이터를 ) >> question 객체에 적용해줌
                # 그래서 db.session.add를 안하는구나. 여기서 적용해주니.
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)   ### get 방식으로 요청되는 경우는  >> <질문수정>버튼을 눌렀을때..
        # 질문수정을 눌렀을때, 질문제목, 질문 내용이 보여야하는데, 가장 간단한 방법은
        # QuestionForm: 폼모델이잖아
        ### QuestionForm(obj=question) 과 같이 >> obj 매개변수에 전달하여, 폼을 생성하는것이다
        # 그럼 QuestionForm의 subject, content 필드에  | question 객체의 subject, content의 값이 전달된다
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for("question.detail.html", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question_list'))