import websocket
import json
import threading

# WebSocket 메시지 수신 시 호출되는 함수
def on_message(ws, message):
    try:
        data = json.loads(message)
        protocol = data.get("protocol")

        if protocol == "loadCoin":
            print("✅ 코인 정보 수신:")
            for coin in data.get("coinList", []):
                print(f" - {coin['name']} | 현재가: {coin['close']} | 거래금액: {coin['tradePrice']}")

        elif protocol == "loadOrderbook":
            print("✅ 오더북 정보 수신:")
            buy_orders = data.get("buyOrders", [])
            sell_orders = data.get("sellOrders", [])
            print(f"📈 매수 호가 개수: {len(buy_orders)} | 📉 매도 호가 개수: {len(sell_orders)}")

        elif protocol == "candle":
            print("✅ 차트 데이터 수신 (최근 5개):")
            for candle in data.get("candlesticks", [])[-5:]:
                print(f" - 시간: {candle['_time']} | 시가: {candle['_open']} | 종가: {candle['_close']} | 고가: {candle['_high']} | 저가: {candle['_low']}")

        else:
            print(f"ℹ️ 다른 메시지 수신: {json.dumps(data, indent=2, ensure_ascii=False)}")

    except json.JSONDecodeError:
        print("⚠️ JSON 디코딩 실패. 메시지:", message)

# WebSocket 연결 시 호출되는 함수
def on_open(ws):
    print("🔗 WebSocket 연결 성공! 요청 전송 중...")

    # 서버에 요청 메시지 전송
    ws.send(json.dumps({"protocol": "connect", "idx": -1, "token": -1, "login": False, "cidx": "8"}))
    ws.send(json.dumps({"protocol": "loadCoin"}))      # 코인 정보 요청
    ws.send(json.dumps({"protocol": "loadOrderbook", "cidx": "8"}))  # 오더북 정보 요청
    ws.send(json.dumps({"protocol": "candle", "cidx": "8"}))         # 차트 데이터 요청

# WebSocket 연결 종료 시 호출되는 함수
def on_close(ws, close_status_code, close_msg):
    print("❌ WebSocket 연결 종료!")
    print(f"🔍 상태 코드: {close_status_code}, 메시지: {close_msg}")

# WebSocket 오류 발생 시 호출되는 함수
def on_error(ws, error):
    print(f"🚫 WebSocket 오류 발생: {error}")

# WebSocket 실행 함수
def run_websocket():
    ws_url = "wss://stip.global/ws/connect"  # 실제 WebSocket URL 

    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )

    # WebSocket 연결 시작
    ws.run_forever()

if __name__ == "__main__":
    print("🚀 WebSocket 연결 시도 중...")

    # WebSocket 실행을 별도 스레드에서 실행 (메인 스레드 차단 방지)
    ws_thread = threading.Thread(target=run_websocket)
    ws_thread.start()
