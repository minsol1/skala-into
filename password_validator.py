#
# 교육 환경 설정 및 간단한 파이썬 연습 코드
# [실습2] 비밀번호 Regex 검증
# 조건: 최소 하나의 영문 소문자, 영문 대문자, 숫자 및 기호가 포함되어야 함
#
# 작성일 : 2026-07-14
# 작성자 : 김민솔, SKALA
#
# 변경일 : 
#
# All Rights Reserved by SK AX, SKALA
#

import re

rules = [
    (r'[a-z]', "영문 소문자"),
    (r'[A-Z]', "영문 대문자"),
    (r'\d', "숫자"),
    (r'[^A-Za-z0-9]', "기호"),
]

password = input("비밀번호를 입력하세요: ")

missing = [name for regex, name in rules if not re.search(regex, password)]

if not missing:
    print("사용 가능한 비밀번호입니다.")
else:
    print(f"비밀번호에 다음 조건이 빠졌습니다: {', '.join(missing)}")
