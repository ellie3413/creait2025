import streamlit as st
import base64
from io import BytesIO
from PyPDF2 import PdfReader
from streamlit_lottie import st_lottie
import requests

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "rental_type" not in st.session_state:
    st.session_state.rental_type = None

st.set_page_config(page_title="💸 돌려내", layout="wide")

# ----- CSS -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poor+Story&display=swap');

    html, body, div, span, input, label, textarea, button, section, article, aside, header, footer, p, h1, h2, h3, h4, h5, h6, * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    button, textarea, input, label {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    .orange-header {
        font-family:'Poor Story', serif !important;
        font-size:52px;
        color: #FF7F50;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .subtle-box {
        background-color: #FF7F50;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }

    div.stButton > button {
        background-color: #FF7F50;
        color: white;
        border: none;
        padding: 0.6em 1.3em;
        border-radius: 5px;
        transition: background-color 0.3s ease;
        font-size: 16px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #FF6347;
    }

    details.guide-box {
        background-color: #FFE0B2;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #FFB74D;
        margin-bottom: 20px;
        width: 80%;
        margin-left: auto;
        margin-right: auto;
        font-size: 16px;
    }
    summary {
        font-weight: bold;
        cursor: pointer;
        color: #E65100;
    }
    </style>
""", unsafe_allow_html=True)

# ----- PDF 뷰어 함수 -----
def show_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie_url = "https://lottie.host/b70a930f-8d8f-4a3b-8e65-96616752c917/ULOhh1m010.json"
lottie_ani = load_lottie_url(lottie_url)


# ----- 페이지 라우팅 -----

# ----- 랜딩 페이지 -----
if st.session_state.page == "landing":
    # 배경색 및 스타일 적용
    st.markdown("""
    <style>
    html, body, .stApp, .main, .block-container {
        background-color: #FFF !important;
    }
    
    .title {
        font-size: 50px;
        font-weight: 800;
        color: #4285F4;
        margin-bottom: 20px;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        font-weight: 500;
        color: #111;
        text-align: center
    }
    div.stButton > button {
    background-color:#4285F4;
    color: white;
    padding: 20px 30px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 4px;
    border: none;
    margin-bottom: 10px;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #4285F4;
    color: white;            
    opacity: 0.8;
}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<hr style="border: 3px solid #4285F4; margin: 20px 0;">
""", unsafe_allow_html=True)
    
    # 두 개의 컬럼 구성 (좌: 소개 / 우: 버튼)
    left, right = st.columns([3, 2])
    
    # 왼쪽 소개
    with left:
        st_lottie(lottie_ani, height=200, key="landing_lottie")
        st.markdown('<div class="title">돌려내</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">돌려내가 여러분의 든든한 법률 파트너가 되어 드릴게요!</div>', unsafe_allow_html=True)
    
    # 오른쪽 버튼 - HTML 버튼 태그 사용
    with right:
        st.markdown("""
        <div style="border: 2px solid #FFF; padding: 50px; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)
        if st.button("📘 튜토리얼 가기"):
            st.session_state.page = "tutorial"
            st.rerun()
        if st.button("💸 내 돈 돌려받기"):
            st.session_state.page = "ai"
            st.rerun()

    st.markdown("""
<hr style="border: 3px solid #4285F4; margin: 20px 0;">
""", unsafe_allow_html=True)

# ----- 튜토리얼 페이지 -----
elif st.session_state.page == "tutorial":
    st.markdown('<div class="orange-header">📘 돌려내 어떻게 사용하나요?</div>', unsafe_allow_html=True)
    st.markdown("""
   1.  임대차 계약서 파일을 업로드하세요 (PDF 파일을 준비해주세요!)
    2. 임대차계약전문가 돌려내봇이 계약서 주요 조항을 분석합니다
    3. 아래에 궁금한 질문을 입력하시면 계약서를 바탕으로 답변을 제공합니다
    """)
    if st.button("돌려내 사용하기"):
        st.session_state.page = "ai"
        st.rerun()

# ----- AI 분석 페이지 -----
elif st.session_state.page == "ai":
    st.markdown('<div class="orange-header"> 💸 돌려내!</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📄 계약서를 업로드해 주세요**")
        uploaded_file = st.file_uploader(label="계약서를 AI가 분석해드리며, 불리한 조항이 있는지 확인합니다.", type=["pdf"])

        if uploaded_file:
            file_bytes = uploaded_file.read()
            file_stream = BytesIO(file_bytes)

            st.markdown("**📄 내 계약서**")
            show_pdf(file_bytes)

    with col2:
        st.markdown("**🔎 계약서 주요 정보 요약**")
        if uploaded_file:
            with st.spinner("계약서를 분석 중입니다..."):
                reader = PdfReader(file_stream)
                text = "".join([page.extract_text() for page in reader.pages])

                st.success("계약서 분석 완료!")
                st.text("여기에 이제 분석 내용이 들어갑니다 (아래는 예시입니다)")
                st.write(text[:500])
        else:
            st.info("계약서를 업로드하면 요약 분석 결과가 여기에 표시됩니다.")

    st.markdown("---")
    st.subheader("어떤 점이 궁금하신가요?")
    user_prompt = st.text_area("🤖 돌려내봇이 여러분의 든든한 법률 파트너가 되어 드릴게요! 궁금한 사항을 입력해 주세요:", placeholder="예: 제가 계약기간을 채우지 못했어요... 보증금을 아예 못 돌려받는 경우도 있나요?")

    ai_prompt= "여기 ai 출력"

    if st.button("질문하기"):
        if not uploaded_file:
            st.warning("먼저 계약서를 업로드해 주세요.")
        elif not user_prompt.strip():
            st.warning("질문을 입력해 주세요.")
        else:
            st.success("분석 결과입니다!")
            st.markdown('<div class="subtle-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **내 질문**: {user_prompt}  
            **돌려내의 분석 결과**: {ai_prompt}
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(" ")
    if st.button("🔙 튜토리얼로 돌아가기"): 
        st.session_state.page = "tutorial"
        st.rerun()
