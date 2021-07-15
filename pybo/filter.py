# 템플릿 필터 만들기

# format_datetime 함수 실행시, UnicodeEncoderError 발생한다면..
import locale
locale.setlocale(locale.LC_ALL, '')
# 위 두줄을 추가


def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)