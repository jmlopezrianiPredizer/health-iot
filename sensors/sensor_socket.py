
import os, time, random, json, websocket

GATEWAY_WS_URL = "ws://gateway:5002/ws"

def generate_health_data():
    return {
        "id": "Sensor socket",
        "heart_rate": random.randint(50, 160),
        "temperature": round(random.uniform(36.0, 40.0), 1),
        "pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

def send_data(ws):
    while True:
        data = generate_health_data()
        rsp = json.dumps(data)
        ws.send(rsp)
        print(f"Enviado: {rsp}")
        time.sleep(5)

# if __name__ == "__main__":
#     socket = websocket.WebSocket()
#     try:
#         socket.connect(GATEWAY_WS_URL)
#         send_data(socket)
#     except Exception as e:
#         print("Error de conexión:", e)
if __name__ == "__main__":
    while True:
        ws = websocket.WebSocket()
        try:
            print(f"Conectando a {GATEWAY_WS_URL}…")
            ws.connect(GATEWAY_WS_URL)
            print("¡Conectado! Empezando a enviar datos…")
            send_data(ws)
        except Exception as e:
            print("Error de conexión o envío:", e)
        finally:
            try:
                ws.close()
            except:
                pass
            print("Esperando 2s antes de reconectar…")
            time.sleep(2)