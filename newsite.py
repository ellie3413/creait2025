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

st.set_page_config(page_title="M$ney.", layout="wide")


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

lottie_url = "https://lottie.host/21891569-1b6f-44bb-9eda-36b302ebb906/fGMM009Fec.json"
lottie_ani = load_lottie_url(lottie_url)


# ----- 페이지 라우팅 -----

# ----- 랜딩 페이지 -----
if st.session_state.page == "landing":
    # 배경색 및 스타일 적용
    st.markdown("""
    <style>
                
    @font-face {
    font-family: 'MaruBuriBold';
    src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot);
    src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot?#iefix) format("embedded-opentype"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff2) format("woff2"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff) format("woff"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.ttf) format("truetype");
}
                
    @font-face {
    font-family: 'MaruBuri';
    src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.eot);
    src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.eot?#iefix) format("embedded-opentype"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.woff2) format("woff2"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.woff) format("woff"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Regular.ttf) format("truetype");
}

html, body, div, span, input, label, textarea, button, section, article, aside, header, footer, p, * {
            font-family: 'MaruBuri', sans-serif !important;
        }
.mango-title {
    font-family: 'MaruBuriBold' !important;
    font-size: 52px;
    color: #4285F4;
    text-align: center;
    margin-bottom: 20px;
    line-height: 1.4;
}
                
    .mango-title .dot {
    color: #FF9BD2; 
}
                
    html, body, .stApp, .main, .block-container {
        background-color: #FFF !important;
    }
    
   
    .subtitle {
        font-family: 'MaruBuri' !important;
        font-size: 20px;
        font-weight: 500;
        color: #111;
        text-align: center
    }
    div.stButton > button {
    font-family: 'MaruBuri' !important;
    background-color:#3D3B40;
    color: white;
    padding: 20px 30px;
    font-size: 30px;
    font-weight: bold;
    border-radius: 4px;
    border: none;
    margin-bottom: 10px;
    width: 80%;
}
div.stButton > button:hover {
    font-family: 'MaruBuri' !important;
    background-color: #FF9BD2;
    color: #3D3B40;            
    opacity: 0.8;
}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<hr style="border: 3px solid #000; margin: 20px 0;">
""", unsafe_allow_html=True)
    
    # 두 개의 컬럼 구성 (좌: 소개 / 우: 버튼)
    left, right = st.columns([3, 2])
    
    # 왼쪽 소개
    with left:
        st_lottie(lottie_ani, height=200, key="landing_lottie")
        st.markdown('<h1 class="mango-title">  M$ney<span class="dot">.</span></h1>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Miney와 함께 떠나는 내 보증금 되찾기 여정</div>', unsafe_allow_html=True)
    
    # 오른쪽 버튼 - HTML 버튼 태그 사용
    with right:
        st.markdown("""
        <div style="border: 2px solid #FFF; padding: 50px; border-radius: 10px;">
        </div>
        """, unsafe_allow_html=True)
        if st.button("튜토리얼 보기"):
            st.session_state.page = "tutorial"
            st.rerun()
        if st.button("내 돈 돌려받기"):
            st.session_state.page = "ai"
            st.rerun()


# ----- 튜토리얼 페이지 -----
elif st.session_state.page == "tutorial":
    st.markdown("""
        <style>
        
        @font-face {
        font-family: 'MaruBuriBold';
        src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot);
        src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot?#iefix) format("embedded-opentype"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff2) format("woff2"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff) format("woff"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.ttf) format("truetype");
    }
                
        html, body, div, span, input, label, textarea, button, section, article, aside, header, footer, p, h1, h2, h3, h4, h5, h6, * {
            font-family: 'MaruBuri', sans-serif !important;
        }
        
        html, body, .stApp, .main, .block-container {
        background-color: #FAE7F3 !important;
    }
                
        .orange-header {
            font-family:'MaruBuriBold',sans-serif !important;
            font-size:35px;
            color: #3D3B40;
            margin-bottom: 10px;
        }
        
        .orange-header .dot {
        color: #FF9BD2; 
    }

        div.stButton > button {
            font-family: 'MaruBuri', sans-serif !important;
            background-color:#3D3B40;
            color: white;
            border: none;
            padding: 0.6em 1.3em;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            font-size: 16px;
            display: flex; 
            justify-content: center;
        }

        div.stButton > button:hover {
            font-family: 'MaruBuri', sans-serif !important;
            background-color: #FF9BD2;
            color: #3D3B40;            
            opacity: 0.8;
        }
                
        .sentence {
            font-family:'MaruBuriBold',sans-serif !important;
            font-size:16px;
            color: #3D3B40;
            margin-bottom: 10px;
        }

        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="orange-header">M$ney<span class="dot">.</span> 사용설명서</div>', unsafe_allow_html=True)
        st.markdown("이미지")
    
    with col2:    
        st.markdown("""
        </br></br></br></br>
        <div class="sentence" style="background-color:#fff; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px;">
            1. 임대차 계약서 파일을 업로드하세요 (PDF 파일을 준비해주세요!)
        </div>
        <div class="sentence" style="background-color:#fff; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px;">
            2. 임대차계약전문가 돌려내봇이 계약서 주요 조항을 분석합니다
        </div>
        <div class="sentence" style="background-color:#fff; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px;">
            3. 아래에 궁금한 질문을 입력하시면 계약서를 바탕으로 답변을 제공합니다
        </div>
        </br></br></br>
        """, unsafe_allow_html=True)

        col_left, col_center, col_right = st.columns([1, 1, 1])

        with col_center:
            if st.button("M$ney 사용하기"):
                st.session_state.page = "ai"
                st.rerun()

# ----- AI 분석 페이지 -----
elif st.session_state.page == "ai":
    st.markdown("""
        <style>
        
        @font-face {
        font-family: 'MaruBuriBold';
        src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot);
        src: url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.eot?#iefix) format("embedded-opentype"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff2) format("woff2"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.woff) format("woff"), url(https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-Bold.ttf) format("truetype");
    }
                
        html, body, div, span, input, label, button, section, article, aside, header, footer, p, h1, h2, h3, h4, h5, h6, * {
            font-family: 'MaruBuri', sans-serif !important;
        }
                
        textarea {
            background-color: #FAE7F3 !important;  /* 연분홍 배경 */
            color: #3D3B40 !important;             /* 텍스트 색상 */
            font-family: 'MaruBuri', sans-serif !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }
               
        .orange-header {
            font-family:'MaruBuriBold',sans-serif !important;
            font-size:35px;
            color: #3D3B40;
            margin-bottom: 10px;
        }
        
        .orange-header .dot {
        color: #FF9BD2; 
    }

        div.stButton > button {
            font-family: 'MaruBuri', sans-serif !important;
            background-color:#3D3B40;
            color: white;
            border: none;
            padding: 0.6em 1.3em;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            font-size: 16px;
        }

        div.stButton > button:hover {
            font-family: 'MaruBuri', sans-serif !important;
            background-color: #FF9BD2;
            color: #3D3B40;            
            opacity: 0.8;
        }
        
         .subheader {
            font-family:'MaruBuriBold',sans-serif !important;
            font-size:20px;
            color: #3D3B40;
            margin-bottom: 10px;
        }
                
        .sentences {
            font-family:'MaruBuriBold',sans-serif !important;
            font-size:16px;
            color: #3D3B40;
            margin-bottom: 10px;
        }

        details.guide-box {
            background-color:#FAE7F3;
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

    col1, col2 = st.columns([5, 1])  

    with col1:
        st.markdown('<h1 class="orange-header">M$ney<span class="dot">.</span></h1>', unsafe_allow_html=True)

    with col2:
        st.markdown(" ")
        if st.button("튜토리얼로 돌아가기"): 
            st.session_state.page = "tutorial"
            st.rerun()


    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="subheader">계약서를 업로드해 주세요</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(label="계약서를 AI가 분석해드리며, 불리한 조항이 있는지 확인합니다.", type=["pdf"])

        if uploaded_file:
            file_bytes = uploaded_file.read()
            file_stream = BytesIO(file_bytes)

            st.markdown("**내 계약서**")
            show_pdf(file_bytes)

    with col2:
        st.markdown('<div class="subheader">M$ney의 계약서 주요 정보 요약</div>', unsafe_allow_html=True)
        if uploaded_file:
            with st.spinner("계약서를 분석 중입니다..."):
                reader = PdfReader(file_stream)
                text = "".join([page.extract_text() for page in reader.pages])

                st.success("계약서 분석 완료!")
                st.text("여기에 이제 분석 내용이 들어갑니다 (아래는 예시입니다)")
                st.write(text[:500])

    st.markdown("---")
    st.markdown('<div class="subheader">어떤 문제가 있으신가요?</div>', unsafe_allow_html=True)
    user_prompt = st.text_area("여러분의 든든한 법률 파트너가 되어 드릴게요! 궁금한 사항을 입력해 주세요.", placeholder="예: 제가 계약기간을 채우지 못했어요... 보증금을 아예 못 돌려받는 경우도 있나요?")

    ai_prompt= "여기 ai 출력"

    _, _, col_btn = st.columns([8, 1, 1]) 

    with col_btn:
        if st.button("질문하기"):
            if not uploaded_file:
                st.warning("먼저 계약서를 업로드해 주세요.")
            elif not user_prompt.strip():
                st.warning("질문을 입력해 주세요.")
            else:
                st.success("분석 결과입니다!")
                st.markdown('<div class="subtle-box">', unsafe_allow_html=True)
                st.markdown(f""" 
                {ai_prompt}
                """)
                st.markdown('</div>', unsafe_allow_html=True)
