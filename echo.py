#
# 교육 환경 설정 및 간단한 파이썬 연습 코드
# [실습1] Echo 프로그램 (1/2)
# 사용자가 입력하는 문장을 그대로 출력하는 프로그램
#
# 작성일 : 2026-07-14
# 작성자 : 김민솔, SKALA
#
# 변경일 : 
#
# All Rights Reserved by SK AX, SKALA
#

while True:
    sentence = input("문장을 입력하세요 (!quit 입력 시 종료): ")
    if sentence == "!quit":
        print("프로그램을 종료합니다. 안녕히 가세요!")
        break
    print(sentence)
