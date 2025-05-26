import streamlit as st
from datetime import date
import re
import pymysql

if 'page' not in st.session_state:
    st.session_state.page = 'register'
# st.session_state : 사용자 상태(세션)를 저장할 수 있는 딕셔너리
# 세션 상태에 page라는 키가 아직 없다면, 기본 페이지를 'register'로 설정

def go_to_login():
    st.session_state.page = 'login'

def go_to_main():
    st.session_state.page = 'main'

# register 페이지 설정
def show_register(login_success):
    st.title("환자 등록")
    name = st.text_input("성함")
    gender = st.selectbox("성별",["여성", "남성"])
    birth = st.date_input("생년월일",
                          value = date(2025, 1,1),
                          min_value = date(1900,1,1),
                          max_value = date.today())   
    password = st.text_input("비밀번호", type="password")
    # type="password" : 입력값을 가려주는 옵션

    if password:
        # 비밀번호 조건
        password_rule = r'^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$'
        if not re.match(password_rule, password):
            st.error("❌비밀번호는 숫자와 영문자를 포함한 8자리 이상이어야 합니다.")
        else:
            st.success("✅사용 가능한 비밀번호입니다!")
            if st.button("다음 단계로"):
                st.session_state.page = "phq9"

if st.session_state.page == 'register':
    show_register(go_to_login)

# phq9 페이지 설정
def show_phq9():
    st.title("PHQ-9 진단")

    st.markdown("<h4>📝 지난 2주일 동안 당신은 다음의 문제들로 인해서 얼마나 자주 방해를 받았는지 체크해주세요.</h4>",
                unsafe_allow_html = True)
    questions = [
        "1. 일 또는 여가 활동을 하는 데 흥미나 즐거움을 느끼지 못함."
        "2. 기분이 가라앉거나, 우울하거나, 희망이 없음."
        "3. 잠이 들거나 계속 잠을 자는 것이 어려움, 또는 잠을 너무 많이 잠."
        "4. 피곤하다고 느끼거나 기운이 거의 없음."
        "5. 입맛이 없거나 괗식을 함."
        "6. 자신을 부정적으로 봄, 혹은 자신이 실패자라고 느끼거나 자신 또는 가족을 실망시킴."
        "7. 신문을 읽거나 텔레비전 보는 것과 같은 일에 집중하는 것이 어려움."
        "8. 다른 사람들이 주목할 정도로 너무 느리게 움직이거나 말을 함,"
        "또는 반대로 평상시보다 많이 움직여서, 너무 안절부절못하거나 들떠 있음."
        "9. 자신이 죽는 것이 더 낫다고 생각하거나 어떤 식으로든 자신을 해칠 것이라고 생각함."]
    
    label_score = {
        "전혀 아니다 (0점)" : 0,
        "며칠 동안 (1점)" : 1, 
        "일주일 이상 (2점)" : 2,
        "거의 매일 (3점)" : 3}
    
    score_labels = list(label_score.keys())
    scores = []


# i는 몇 번 반복했는지, q는 요소(list 안에 실제 값)
# enumerate()는 i와 q(번호도, 값도) 모두 동시에 꺼내주는 함수
    for i, q in enumerate(questions):
        choice = st.radio(q, score_labels, key=f"phq9_q{i}")
        scores.append(label_score[choice])

    if "confirm" not in st.session_state:
        st.session_state.confirm = False

    if st.button("완료"):
        st.session_state.confirm = True

    if st.session_state.confirm:
        if st.warning("입력한 정보로 등록하시겠습니까?")

        col1, col2 = st.columns(2)

    with col1: 
        if st.button("등록"):
            total = sum(scores)
            insert_phq9(patient_id, date.today(), scores, total)
            st.success("등록이 완료되었습니다!")
            st.session_state.confirm = False