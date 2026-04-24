import json
from pathlib import Path
import streamlit as st

# 기본 설정
st.set_page_config(page_title="공구 마스터 퀴즈", page_icon="🛠️", layout="centered")

STUDENT_ID = "2024404085"
STUDENT_NAME = "장원준"
QUESTION_FILE = Path("data/questions.json")

VALID_USERS = {
    "toolmaster": "1234",
    "wonjun": "hammer",
}

# 스타일 정의
def apply_custom_style():
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 텍스트 기본 색상 */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #2f3542 !important;
        font-family: 'Pretendard', sans-serif;
    }

    /* 핸드폰 비율 레이아웃 */
    .main .block-container {
        max-width: 500px;
        padding-top: 2rem;
    }

    /* 진행바 색상 - 레드 포인트 */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #ff4757; 
    }
    
    /* 입력창 스타일링 - 검은색 제거 */
    div[data-testid="stTextInput"] input {
        background-color: #f1f2f6 !important;
        color: #2f3542 !important;
        border: 1px solid #dfe4ea !important;
        border-radius: 10px !important;
    }
    
    /* 문제 카드 스타일 */
    .quiz-container {
        background-color: #f7f9fb;
        border-radius: 20px;
        padding: 25px;
        margin-top: 10px;
        border: 1px solid #edf2f7;
    }

    /* 정답/오답 상단 피드백 박스 */
    .feedback-box {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        font-weight: 700;
        text-align: center;
        border: 2px solid transparent;
    }
    .correct-box {
        background-color: #e3f9e5;
        color: #2ed573 !important;
        border-color: #2ed573;
    }
    .wrong-box {
        background-color: #fff4f4;
        color: #ff4757 !important;
        border-color: #ff4757;
    }

    /* 버튼 스타일 - 검은색 제거 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 800;
        background-color: #747d8c; /* 부드러운 그레이 */
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff4757;
        color: white;
    }

    /* 상단 정보 배지 레이아웃 */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    .header-title {
        font-weight: 800;
        color: #2f3542 !important;
        font-size: 1.1rem;
    }
    .header-percent {
        font-weight: 700;
        color: #ff4757 !important;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def reset_quiz():
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.user_answer = None

def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_idx" not in st.session_state:
        st.session_state.current_idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = None

def main():
    apply_custom_style()
    init_state()

    if not st.session_state.logged_in:
        # 로그인 페이지 진입 시 quiz 상태 항상 초기화
        reset_quiz()

        st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
            <h1 style='font-size: 2.5rem;'>🛠️ 공구 마스터</h1>
            <p style='font-size: 1.1rem; color: #747d8c; font-weight: 600;'>당신도 공구 마스터에 도전해보세요!</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        user_id = st.text_input("아이디", placeholder="wonjun")
        user_pw = st.text_input("비밀번호", type="password", placeholder="hammer")

        if st.button("게임 시작하기", key="btn_login"):
            if user_id in VALID_USERS and VALID_USERS[user_id] == user_pw:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("로그인 정보가 올바르지 않습니다.")

        st.write("")
        st.caption(f"제출자: {STUDENT_NAME} ({STUDENT_ID})")
        return

    # 퀴즈 로직
    questions = load_questions(QUESTION_FILE)
    total = len(questions)
    
    # 1. 상단 정보 (🛠️ 공구 마스터 + 진행율)
    percent = int((st.session_state.current_idx / total) * 100)
    if st.session_state.current_idx >= total: percent = 100
    
    st.markdown(f"""
    <div class='header-container'>
        <div class='header-title'>🛠️ 공구 마스터</div>
        <div class='header-percent'>{percent}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    progress_val = min(st.session_state.current_idx / total, 1.0)
    st.progress(progress_val)

    if st.session_state.current_idx < total:
        q = questions[st.session_state.current_idx]
        
        # 2. 피드백 영역
        if st.session_state.submitted:
            if st.session_state.user_answer == q['answer']:
                st.markdown(f"<div class='feedback-box correct-box'>✅ 정답입니다!</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-box wrong-box'>❌ 아쉽습니다! 정답은 [{q['answer']}]</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='height: 74px;'></div>", unsafe_allow_html=True)

        # 3. 문제 박스
        st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: 0; line-height: 1.5;'>Q{st.session_state.current_idx + 1:02d}. {q['description']}</h3>", unsafe_allow_html=True)
        
        ans = st.radio("정답 선택", q['options'], index=None, key=f"q_{st.session_state.current_idx}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("") # 간격

        # 4. 버튼 영역
        if not st.session_state.submitted:
            if st.button("정답 확인하기", key=f"btn_check_{st.session_state.current_idx}"):
                if ans:
                    st.session_state.user_answer = ans
                    st.session_state.submitted = True
                    if ans == q['answer']:
                        st.session_state.score += 1
                    st.rerun()
                else:
                    st.warning("먼저 정답을 선택해 주세요!")
        else:
            is_last = st.session_state.current_idx == total - 1
            btn_text = "결과 보기 🏆" if is_last else "다음 문제로 👉"
            if st.button(btn_text, key=f"btn_next_{st.session_state.current_idx}"):
                st.session_state.current_idx += 1
                st.session_state.submitted = False
                st.session_state.user_answer = None
                st.rerun()

    else:
        # 5. 결과 화면
        st.balloons()
        st.markdown("<div style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
        st.title("🏆 미션 클리어!")
        st.markdown(f"<h2 style='color: #ff4757; margin-bottom: 30px;'>최종 점수: {st.session_state.score} / {total}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 버튼 수평 배치
        col1, col2 = st.columns(2)
        with col1:
            if st.button("다시 도전하기", key="btn_retry"):
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("로그아웃", key="btn_logout"):
                reset_quiz()
                st.session_state.logged_in = False
                st.rerun()

if __name__ == "__main__":
    main()
