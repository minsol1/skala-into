#
# 교육 환경 설정 및 간단한 파이썬 연습 코드
# [실습2] echo 프로그램으로 비밀번호 검증하기
# 조건: 최소 하나의 영문 소문자, 영문 대문자, 숫자 및 기호가 포함되어야 함
# !quit 입력 시 프로그램 종료
#
# 작성일 : 2026-07-14
# 작성자 : 김민솔, SKALA
#
# 변경일 :
#
# All Rights Reserved by SK AX, SKALA
#

import re

RULES = [
    (r'[a-z]', "영문 소문자"),
    (r'[A-Z]', "영문 대문자"),
    (r'\d', "숫자"),
    (r'[^A-Za-z0-9]', "기호"),
]


def check_password(password):
    missing = [name for regex, name in RULES if not re.search(regex, password)]
    return len(missing) == 0, missing


while True:
    password = input("비밀번호를 입력하세요 (!quit 입력 시 종료): ")

    if password == "!quit":
        print("프로그램을 종료합니다. 안녕히 가세요!")
        break

    is_valid, missing = check_password(password)

    if is_valid:
        print("사용 가능한 비밀번호입니다.")
    else:
        print(f"비밀번호에 다음 조건이 빠졌습니다: {', '.join(missing)}")
