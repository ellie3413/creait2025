import openai
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
import os

# 1. 환경 변수 불러오기 (.env 파일에서)
load_dotenv()

# 2. API 키 세팅
openai.api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

if not openai.api_key or not weather_api_key:
    raise Exception("API 키가 .env에서 정상적으로 로드되지 않았습니다!")

# 3. 지역 → 위경도 매핑
location_to_coords = {
    "서울": (60, 127),
    "부산": (98, 76),
    "대전": (67, 100),
    "광주": (58, 74),
    "대구": (89, 90),
    "제주": (52, 38)
}

# 4. 현재 날짜/시간 처리 함수
def get_current_date():
    return datetime.now().strftime("%Y%m%d")

def get_current_hour():
    now = datetime.now()
    hour = now.hour
    if now.minute < 45:
        hour -= 1
    return f"{hour:02}00"

# 5. 강수형태 해석
int_to_weather = {
    "0": "맑음 (강수 없음)",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}
import urllib.parse

# API 키를 디코드한 후 사용
def forecast(nx, ny):
    # API 키가 이미 인코딩되어 있을 경우 디코드
    decoded_key = urllib.parse.unquote(weather_api_key)
    
    params = {
        'serviceKey': decoded_key,
        'numOfRows': '100',
        'pageNo': '1',
        'dataType': 'XML',
        'base_date': get_current_date(),
        'base_time': get_current_hour(),
        'nx': str(nx),
        'ny': str(ny)
    }

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    
    try:
        print(f"요청 URL: {url}")
        print(f"요청 파라미터: {params}")
        
        res = requests.get(url, params=params)
        
        # 상태 코드와 응답 내용 출력
        print(f"응답 상태 코드: {res.status_code}")
        print(f"응답 텍스트 (일부): {res.text[:200]}")  # 처음 200자만 출력
        
        # 상태 코드 검사
        res.raise_for_status()
        
        # XML 파싱
        root = ET.fromstring(res.text)
        
        # 응답 상태 확인
        result_code = root.find(".//resultCode")
        if result_code is not None and result_code.text != "00":
            result_msg = root.find(".//resultMsg")
            error_msg = result_msg.text if result_msg is not None else "Unknown error"
            print(f"API 오류: {error_msg} (코드: {result_code.text})")
            return None, None
        
        temp, sky_code = None, None
        
        # 아이템 목록 찾기
        items = root.findall(".//item")
        for item in items:
            category = item.find("category")
            if category is not None:
                if category.text == "T1H":  # 기온
                    temp = item.find("obsrValue").text
                elif category.text == "PTY":  # 강수형태
                    sky_code = item.find("obsrValue").text
        
        sky = int_to_weather.get(sky_code, "정보 없음")
        return temp, sky
    
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None, None
    except ET.ParseError as e:  # XML 파싱 오류
        print(f"XML 파싱 오류: {e}")
        print(f"응답 원문: {res.text}")  # 전체 응답 내용 확인
        return None, None
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}")
        return None, None

# 7. 사용자 입력 및 실행
location = input("어느 지역 날씨가 궁금해? (예: 서울, 부산 등): ").strip()

if location in location_to_coords:
    nx, ny = location_to_coords[location]
    print(f"날씨 정보를 조회 중입니다...")
    temp, sky = forecast(nx, ny)
    
    if temp is None or sky is None:
        print("❌ 날씨 정보를 가져오지 못했습니다.")
    else:
        print(f"\n🌤️ {location}의 현재 날씨 정보:")
        print(f"- 기온: {temp}°C")
        print(f"- 강수형태: {sky}")
else:
    print(f"❌ '{location}'은(는) 지원하지 않는 지역입니다. 서울, 부산, 대전, 광주, 대구, 제주 중에서 선택해주세요.")