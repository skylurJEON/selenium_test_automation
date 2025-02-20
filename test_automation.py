from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 필요 시 주석 해제
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)  # 대기 시간 

try:
    # 웹 페이지 열기
    url = "https://stip.global/user/trade?cidx=8"
    driver.get(url)
    time.sleep(3)

    # ✅ 테스트 시나리오 1: 페이지 타이틀 확인
    current_title = driver.title.strip()
    print(f"현재 페이지 타이틀: {current_title}")
    assert any(keyword in current_title for keyword in ["Trade", "거래", "STIP"]), "페이지 타이틀 검증 실패!"
    print("✅ 페이지 타이틀 확인 완료.")

    # ✅ 테스트 시나리오 2: 가격 정보 확인
    try:
        price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_closePrice")))
        price = price_element.text.strip()
        print(f"✅ 현재 가격: {price} USDT")
    except Exception as e:
        print(f"⚠️ 가격 정보를 찾을 수 없습니다: {e}")

     # ✅ 테스트 시나리오 3: 차트 로딩 확인
    print("🔎 차트 로딩 확인 중...")

      # 1️⃣ iframe 내부 탐색 시도 (iframe 존재 여부 확인)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    chart_found = False

    if iframes:
        print(f"🔍 {len(iframes)}개의 iframe 발견. 차트 탐색 시도 중...")

        for idx, iframe in enumerate(iframes):
            driver.switch_to.frame(iframe)
            try:
                # iframe 내 모든 div 요소 가져오기 (차트 요소 확인용)
                div_elements = driver.find_elements(By.TAG_NAME, "div")
                for div in div_elements:
                    class_name = div.get_attribute("class")
                    if class_name and any(keyword in class_name for keyword in [
                        "tradingview", "chart", "tv-lightweight-charts", "tv-chart-container",
                        "chart-container", "chartArea"]):
                        print(f"✅ 차트 로딩 확인 완료 (iframe #{idx}에서 발견). 클래스명: {class_name}")
                        chart_found = True
                        break

                driver.switch_to.default_content()
                if chart_found:
                    break

            except Exception as e:
                driver.switch_to.default_content()  # 다음 iframe 탐색 위해 초기화
                print(f"⚠️ iframe #{idx} 탐색 중 오류 발생: {e}")

    # 2️⃣ iframe에서 찾지 못한 경우, 메인 페이지 탐색 시도
    if not chart_found:
        print("🔍 메인 페이지에서 차트 탐색 시도 중...")
        try:
            div_elements = driver.find_elements(By.TAG_NAME, "div")
            for div in div_elements:
                class_name = div.get_attribute("class")
                if class_name and any(keyword in class_name for keyword in [
                    "tradingview", "chart", "tv-lightweight-charts", "tv-chart-container",
                    "chart-container", "chartArea"]):
                    print(f"✅ 차트 로딩 확인 완료 (메인 페이지에서 발견). 클래스명: {class_name}")
                    chart_found = True
                    break
            
            if not chart_found:
                print("⚠️ 메인 페이지에서 차트 요소 탐색 실패: 관련 클래스명 div 요소 미발견.")

        except Exception as e:
            print(f"⚠️ 메인 페이지 탐색 중 오류 발생: {e}")

    # 3️⃣ 최종 결과 출력
    if not chart_found:
        print("❌ 차트 로딩 실패: 차트 요소를 찾을 수 없습니다.")

except Exception as e:
    print(f"❌ 예외 발생: {e}")

finally:
    driver.quit()

