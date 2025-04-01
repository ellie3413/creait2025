import streamlit as st
from io import StringIO
from PyPDF2 import PdfReader

st.set_page_config(page_title="돌려내", layout="wide")

st.title("🏠 돌려내: 주택 임대차 계약 분석 도우미")

st.markdown("법적으로 불리한 조항, 사용자 맞춤 질문에 대해 AI가 도와드립니다!")

# --- Sidebar (계약 정보 입력)
st.sidebar.header("1️⃣ 계약 정보 입력")
rental_type = st.sidebar.radio("계약 유형을 선택하세요:", ["전세", "월세"])
uploaded_file = st.sidebar.file_uploader("📄 계약서 업로드", type=["pdf", "txt"])

# --- 사용자 질문 입력
st.sidebar.header("2️⃣ 질문 입력")
user_prompt = st.sidebar.text_area("궁금한 점이나 상황을 자유롭게 입력해 주세요:", placeholder="예: 중도 해지 시 위약금이 발생하나요?")

if st.sidebar.button("분석 시작하기 🚀"):
    if uploaded_file is None:
        st.warning("계약서를 업로드해 주세요.")
    elif not user_prompt:
        st.warning("궁금한 점을 입력해 주세요.")
    else:
        # --- 계약서 내용 읽기
        with st.spinner("계약서를 분석 중입니다..."):
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            else:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                text = stringio.read()

            # --- 여기에 OpenAI API 호출 or RAG 연결 ---
            # 예시 출력 (임시)
            st.success("분석이 완료되었습니다!")
            st.markdown("#### 💡 AI 분석 결과")
            st.markdown(f"""
            **계약 유형**: {rental_type}  
            **사용자 질문**: {user_prompt}

            ---  
            📌 **예상 분석 내용 (예시)**  
            - 계약서 상 중도 해지 시 위약금이 발생할 수 있는 조항이 있습니다.  
            - '계약 해제 시 임차인이 임대인에게 2개월치 월세를 지급한다'는 조항은 일반적이지 않으며, 분쟁의 소지가 있습니다.  
            - 주택임대차보호법 제6조에 따라 불공정한 조항은 무효가 될 수 있습니다.
            """)

# --- 챗GPT 스타일 대화창 (데모용)
st.markdown("---")
st.subheader("🗨️ 대화 시뮬레이션 (Demo)")
chat_input = st.text_input("무엇이 궁금하신가요?", key="chat_input")

if chat_input:
    st.markdown("**USER:** " + chat_input)
    # 예시 응답
    st.markdown("**돌려내봇:** 해당 조항은 임대차보호법 제4조에 의해 보호받지 못할 수 있습니다. 좀 더 자세한 설명을 원하시나요?")
