import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import urllib.parse
import ssl
import time
from typing import Optional, Tuple, Dict, Any

# 1. 환경 변수 불러오기 (.env 파일에서)
load_dotenv()

# 2. API 키 세팅
openai.api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

if not openai.api_key or not weather_api_key:
    raise Exception("API 키가 .env에서 정상적으로 로드되지 않았습니다!")

# URL 인코딩된 API 키를 디코딩
weather_api_key = urllib.parse.unquote(weather_api_key)

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
def get_current_date() -> str:
    return datetime.now().strftime("%Y%m%d")

def get_current_hour() -> str:
    now = datetime.now()
    hour = now.hour
    # API는 매시각 45분에 생성되어 지원됨
    if now.minute < 45:
        hour = (hour - 1) if hour > 0 else 23
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

def validate_api_response(data: Dict[str, Any]) -> bool:
    """API 응답의 구조를 검증합니다."""
    try:
        return (
            isinstance(data, dict) and
            'response' in data and
            'body' in data['response'] and
            'items' in data['response']['body'] and
            'item' in data['response']['body']['items']
        )
    except Exception:
        return False

def extract_weather_data(items: list) -> Tuple[Optional[str], Optional[str]]:
    """날씨 데이터를 추출합니다."""
    temp, sky_code = None, None
    for item in items:
        if not isinstance(item, dict) or 'category' not in item or 'obsrValue' not in item:
            continue
        if item['category'] == 'T1H':
            temp = item['obsrValue']
        if item['category'] == 'PTY':
            sky_code = str(item['obsrValue'])
    return temp, sky_code

# 6. 기상청 API 호출 함수
def forecast(nx: int, ny: int, max_retries: int = 3) -> Tuple[Optional[str], Optional[str]]:
    """날씨 정보를 가져오는 함수입니다."""
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    base_date = get_current_date()
    base_time = get_current_hour()

    # API 요청 파라미터 설정
    params = {
        'serviceKey': weather_api_key,  # 이미 인코딩된 API 키
        'numOfRows': '10',
        'pageNo': '1',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': str(nx),
        'ny': str(ny)
    }

    # 초단기실황 조회 URL
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    
    print(f"\n[API 요청 정보]")
    print(f"- 날짜: {base_date}")
    print(f"- 시각: {base_time}")
    print(f"- 위치: nx={nx}, ny={ny}")
    
    for attempt in range(max_retries):
        try:
            # requests.get()을 직접 사용하여 세션 관리 단순화
            res = requests.get(
                url, 
                params=params,
                headers=headers,
                timeout=10,
                verify=True
            )
            
            if attempt == 0:
                print(f"- 요청 URL: {res.url}\n")
            
            # 응답 확인
            print(f"시도 {attempt + 1}: 상태 코드 {res.status_code}")
            
            if res.status_code != 200:
                print(f"API 오류: {res.text}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None, None

            # JSON 응답 파싱
            try:
                data = res.json()
            except ValueError as e:
                print(f"JSON 파싱 오류: {res.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None, None

            # 응답 구조 검증
            if not validate_api_response(data):
                print("잘못된 API 응답 구조")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None, None

            # 데이터 추출
            items = data['response']['body']['items']['item']
            temp, sky_code = extract_weather_data(items)

            if temp is None or sky_code is None:
                print("날씨 데이터 누락")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None, None

            sky = int_to_weather.get(sky_code, "정보 없음")
            return temp, sky

        except requests.exceptions.RequestException as e:
            print(f"요청 오류: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None, None
        except Exception as e:
            print(f"예상치 못한 오류: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None, None

    return None, None

# 7. 사용자 입력 및 실행
def main():
    location = input("어느 지역 날씨가 궁금해? (예: 서울, 부산 등): ").strip()

    if location not in location_to_coords:
        print("❌ 지원하지 않는 지역입니다. (서울, 부산, 대전, 광주, 대구, 제주 중 선택)")
        return

    nx, ny = location_to_coords[location]
    temp, sky = forecast(nx, ny)

    if temp is None or sky is None:
        print("❌ 날씨 정보를 가져오지 못했습니다.")
    else:
        print(f"\n🌤️ {location}의 현재 날씨 정보:")
        print(f"- 기온: {temp}°C")
        print(f"- 강수형태: {sky}")

if __name__ == "__main__":
    main()
