import streamlit as st
import base64
from io import BytesIO
from PyPDF2 import PdfReader

# 세션 상태 초기화: 계약 유형 선택
if "rental_type" not in st.session_state:
    st.session_state.rental_type = None

st.set_page_config(page_title="💸 돌려내", layout="wide")

# CSS
st.markdown("""
    <style>
   @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Poor+Story&display=swap');
   
    html, body, div, span, input, label, textarea, button, section, article, aside, header, footer, p, h1, h2, h3, h4, h5, h6, * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    /* 버튼과 입력창에도 폰트 적용 */
    button, textarea, input, label {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    /* 기본 헤더 스타일 (주황색) */
    .orange-header {
        font-family:'Poor Story', serif !important;
        font-size:52px;
        color: #FF7F50;
        font-weight: 700;
        margin-bottom: 10px;
    }
    /* 깔끔한 박스 스타일 */
    .subtle-box {
        background-color: #FF7F50;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    /* Streamlit 버튼 스타일 재정의 */
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
    /* 선택된 버튼 스타일 (강조) */
    .selected-btn {
        background-color: #FF4500 !important;
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


def show_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# 페이지 타이틀
st.markdown('<div class="orange-header"> 💸 돌려내!</div>', unsafe_allow_html=True)

st.markdown("""
<details class="guide-box">
  <summary><strong>💡 돌려내! 어떻게 사용하나요? (클릭해서 보기)</strong></summary>
  <br>
  1. 전세, 월세 선택 후 임대차 계약서 파일을 업로드하세요 (PDF 또는 텍스트 파일만 가능합니다)<br>
  2. 임대차계약전문가 돌려내봇이 계약서 주요 조항을 분석합니다<br>
  3. 아래에 궁금한 질문을 입력하시면 계약서를 바탕으로 답변을 제공합니다
</details>
""", unsafe_allow_html=True)

# --- 레이아웃 분할: 왼쪽(업로드 및 계약 유형 버튼), 오른쪽(계약서 요약)
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📄 계약서를 업로드해 주세요**")
    uploaded_file = st.file_uploader(label="계약서를 AI가 분석해드리며, 불리한 조항이 있는지 확인합니다.",type=["pdf"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_stream = BytesIO(file_bytes)

        # PDF 미리보기
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

# --- 하단: 질문 입력 영역
st.markdown("---")
st.subheader("어떤 점이 궁금하신가요?")
user_prompt = st.text_area("🤖 돌려내봇이 여러분의 든든한 법률 파트너가 되어 드릴게요! 궁금한 사항을 입력해 주세요:", placeholder="예: 제가 계약기간을 채우지 못했어요... 보증금을 아예 못 돌려받는 경우도 있나요?")

if st.button("질문하기"):
    if not uploaded_file:
        st.warning("먼저 계약서를 업로드해 주세요.")
    elif not user_prompt.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        # 여기에 실제 질문 분석 로직 (예: OpenAI API 호출)이 들어갈 자리
        st.success("분석 결과입니다!")
        st.markdown('<div class="subtle-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **질문**: {user_prompt}  
        **AI 응답**: 계약서 제6조에 따르면 중도 해지 시 임차인에게 불리한 조항이 적용될 수 있으니, 변호사 상담을 권장드립니다.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
