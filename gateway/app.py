import threading
import time
import json
import asyncio
import requests
import websockets
import grpc
import paho.mqtt.client as mqtt

# Estos dos archivos deben estar en el mismo directorio:
#  - iot_pb2.py
#  - iot_pb2_grpc.py
import iot_pb2, iot_pb2_grpc

# ---------- Configuración MQTT ----------
MQTT_BROKER = "mosquitto"      # nombre del servicio en docker-compose
MQTT_PORT   = 1883
MQTT_TOPIC  = "health/data"

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, MQTT_PORT)


# ---------- Loop REST ----------
def rest_loop():
    """
    Cada 5 s hace GET al sensor REST y publica el JSON
    """
    url = "http://sensors_rest:5000/data"
    while True:
        try:
            resp = requests.get(url, timeout=3)
            resp.raise_for_status()
            data = resp.json()
            mqttc.publish(MQTT_TOPIC, json.dumps(data))
            print("[REST] Publicado:", data)
        except Exception as e:
            print("[REST] Error:", e)
        time.sleep(5)


# ---------- Loop WebSocket ----------
async def ws_loop():
    """
    Se conecta al sensor WebSocket y publica cada mensaje que llega
    """
    uri = "ws://sensors_ws:6789"
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("[WS] Conectado a", uri)
                async for message in ws:
                    mqttc.publish(MQTT_TOPIC, message)
                    print("[WS] Publicado:", message)
        except Exception as e:
            print("[WS] Error:", e)
            # si se desconecta, reintentar en 5 s
            await asyncio.sleep(5)


# ---------- Loop gRPC ----------
def grpc_loop():
    """
    Crea un canal al servidor gRPC y, cada 5 s, envía un Data
    y publica la respuesta (Response) en MQTT.
    """
    # 1) Canal al servicio gRPC
    channel = grpc.insecure_channel("sensors_grpc:50051")
    # 2) Stub que genera protoc: IotServiceStub
    stub   = iot_pb2_grpc.IotServiceStub(channel)

    while True:
        try:
            # 3) Prepara tu mensaje Data según el proto
            req = iot_pb2.Data(
                id="sensor-1",
                heart_rate=80,
                temperature=36.5,
                pressure="120/80"
            )
            # 4) Llamada remota SendData, que devuelve un Response
            resp = stub.SendData(req)

            # 5) Publica el status y los valores en MQTT
            payload = {
                "id":           req.id,
                "heart_rate":   req.heart_rate,
                "temperature":  req.temperature,
                "pressure":     req.pressure,
                "status":       resp.status
            }
            mqttc.publish(MQTT_TOPIC, json.dumps(payload))
            print("[gRPC] Publicado:", payload)

        except Exception as e:
            print("[gRPC] Error:", e)

        # 6) Espera antes de la siguiente llamada
        time.sleep(5)


# ---------- Arranque de hilos y corutina principal ----------
if __name__ == "__main__":
    # 1) REST en hilo aparte
    threading.Thread(target=rest_loop, daemon=True).start()
    # 2) gRPC en hilo aparte
    threading.Thread(target=grpc_loop, daemon=True).start()
    # 3) WebSocket en el hilo principal (asyncio)
    asyncio.run(ws_loop())
