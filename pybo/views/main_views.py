from flask import Blueprint, url_for    ## render_template 화면구성인데, url_for를 쓰면서 삭제하네????
from werkzeug.utils import redirect     ## werkzeug 대체 뭐하는놈?

bp = Blueprint('main', __name__, url_prefix='/')
    # (블루프린트 객체의)이름, 모듈명, url프리픽스 값을 전달해야함
    # main은 , > 함수명으로 url을 찾아주는 > url_for 함수에서 사용예정
    # ulr_prefix 는 접두어 url을 정할때 사용

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
        # url_for 함수는 > 라우트가 설정된 함수명으로 url을 역으로 찾아주고
        # redirect 입력받은 url로 리다이렉트 해둔다.
        # question._list 순서대로 해석되어 > question 찾고(블루프린트) > _list 함수 찾고
        ### question._list 에서 >> question 은 >> 블루프린트 이름이야 !!!!!!!!!!!!
        ### url_for('question._list')는 bp의 접두어인 /question/과 /list/가 더해진 /question/list/ URL을 반환









