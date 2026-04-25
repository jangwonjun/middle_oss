import json
from pathlib import Path
import streamlit as st

# 1. 초기 설정 (가장 먼저 실행)
st.set_page_config(page_title="공구 마스터 퀴즈", page_icon="🛠️", layout="centered")

STUDENT_ID = "2024404085"
STUDENT_NAME = "장원준"
QUESTION_FILE = Path("data/questions.json")

VALID_USERS = {
    "toolmaster": "1234",
    "wonjun": "hammer",
}

# 퀴즈 리셋 함수
def reset_quiz_state():
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.user_answer = None

# 초기 상태 설정
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

# 스타일 정의
def apply_custom_style():
    st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #2f3542 !important; font-family: 'Pretendard', sans-serif; }
    .main .block-container { max-width: 500px; padding-top: 2rem; }
    div[data-testid="stProgress"] > div > div > div > div { background-color: #ff4757; }
    div[data-testid="stTextInput"] input { background-color: #f1f2f6 !important; color: #2f3542 !important; border: 1px solid #dfe4ea !important; border-radius: 10px !important; }
    .quiz-container { background-color: #f7f9fb; border-radius: 20px; padding: 25px; margin-top: 10px; border: 1px solid #edf2f7; }
    .feedback-box { padding: 15px; border-radius: 15px; margin-bottom: 20px; font-weight: 700; text-align: center; border: 2px solid transparent; }
    .correct-box { background-color: #e3f9e5; color: #2ed573 !important; border-color: #2ed573; }
    .wrong-box { background-color: #fff4f4; color: #ff4757 !important; border-color: #ff4757; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: 800; background-color: #747d8c; color: white; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff4757; color: white; }
    .header-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    .header-title { font-weight: 800; color: #2f3542 !important; font-size: 1.1rem; }
    .header-percent { font-weight: 700; color: #ff4757 !important; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    apply_custom_style()
    init_state()

    # --- 로그인 화면 ---
    if not st.session_state.logged_in:
        with st.container():
            st.markdown("""
            <div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
                <h1 style='font-size: 2.5rem;'>🛠️ 공구 마스터</h1>
                <p style='font-size: 1.1rem; color: #747d8c; font-weight: 600;'>당신도 공구 마스터에 도전해보세요!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            user_id = st.text_input("아이디", placeholder="wonjun", key="login_id")
            user_pw = st.text_input("비밀번호", type="password", placeholder="hammer", key="login_pw")
            
            if st.button("게임 시작하기", key="login_btn"):
                if user_id in VALID_USERS and VALID_USERS[user_id] == user_pw:
                    st.session_state.logged_in = True
                    reset_quiz_state()
                    st.rerun()
                else:
                    st.error("로그인 정보가 올바르지 않습니다.")
            
            # 제출자 정보 (컨테이너 내부 하단에 배치)
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            st.caption(f"제출자: {STUDENT_NAME} ({STUDENT_ID})")
        return 

    # --- 퀴즈 화면 ---
    questions = load_questions(QUESTION_FILE)
    total = len(questions)
    
    # 퀴즈 종료 여부 확인
    if st.session_state.current_idx >= total:
        st.balloons()
        st.markdown("<div style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
        st.title("🏆 미션 클리어!")
        st.markdown(f"<h2 style='color: #ff4757; margin-bottom: 30px;'>최종 점수: {st.session_state.score} / {total}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("다시 도전하기", key="retry_btn"):
                reset_quiz_state()
                st.rerun()
        with col2:
            if st.button("로그아웃", key="logout_btn_end"):
                # 모든 세션 초기화 후 강제 리셋
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        return

    # 진행바 및 상단 정보
    percent = int((st.session_state.current_idx / total) * 100)
    st.markdown(f"<div class='header-container'><div class='header-title'>🛠️ 공구 마스터</div><div class='header-percent'>{percent}%</div></div>", unsafe_allow_html=True)
    st.progress(st.session_state.current_idx / total)

    q = questions[st.session_state.current_idx]
    
    # 피드백 영역
    if st.session_state.submitted:
        if st.session_state.user_answer == q['answer']:
            st.markdown(f"<div class='feedback-box correct-box'>✅ 정답입니다!</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-box wrong-box'>❌ 아쉽습니다! 정답은 [{q['answer']}]</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='height: 74px;'></div>", unsafe_allow_html=True)

    # 문제 카드
    st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-top: 0; line-height: 1.5;'>Q{st.session_state.current_idx + 1:02d}. {q['description']}</h3>", unsafe_allow_html=True)
    ans = st.radio("정답 선택", q['options'], index=None, key=f"q_{st.session_state.current_idx}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    
    # 하단 버튼 제어
    if not st.session_state.submitted:
        if st.button("정답 확인하기", key=f"check_{st.session_state.current_idx}"):
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
        btn_txt = "결과 보기 🏆" if is_last else "다음 문제로 👉"
        if st.button(btn_txt, key=f"next_{st.session_state.current_idx}"):
            st.session_state.current_idx += 1
            st.session_state.submitted = False
            st.session_state.user_answer = None
            st.rerun()

if __name__ == "__main__":
    main()
