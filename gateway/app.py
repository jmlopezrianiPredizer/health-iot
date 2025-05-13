from multiprocessing import Process
import asyncio
from concurrent import futures
import grpc
import json
import iot_pb2
import iot_pb2_grpc
import paho.mqtt.client as mqtt
from flask import Flask, request
import time
from websockets import serve


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/entries"

mqtt_client = mqtt.Client()

mqtt_ws_client = mqtt.Client()


class iotService(iot_pb2_grpc.IotServiceServicer):
    def SendData(self, request, context):
        data = {
            "sensor_id":     request.id,
            "heart_rate":    request.heart_rate,
            "temperature":   request.temperature,
            "pressure": request.pressure
        }
        print("grpc", data)
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
        return iot_pb2.Response(status="OK")

def run_grpc():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    servicer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_pb2_grpc.add_IotServiceServicer_to_server(iotService(), servicer)
    servicer.add_insecure_port('[::]:50051')
    print("Servidor gRPC iniciado en el puerto 50051")
    servicer.start()
    servicer.wait_for_termination()

app = Flask(__name__)
client_rest = mqtt.Client()
client_rest.connect(MQTT_BROKER, MQTT_PORT, 60)

@app.route('/data', methods=['POST'])
def receive_data():
    body = request.json
    data = {
        "sensor_id":     body.get("id"),
        "heart_rate":    body["heart_rate"],
        "temperature":   body["temperature"],
        "pressure":      body["pressure"]
    }
    print("Recibido:", data)
    client_rest.publish(MQTT_TOPIC, json.dumps(data))
    return '', 200

def run_rest():
    print("Servidor Rest iniciado en el puerto 5000")
    app.run(host="0.0.0.0", port=5000)

async def ws_handler(websocket):
    async for message in websocket:
        payload = json.loads(message)
        data = {
            "sensor_id":   payload.get("id"),
            "heart_rate":  payload["heart_rate"],
            "temperature": payload["temperature"],
            "pressure":    payload["pressure"]
        }
        print("Recibido WS:", data)
        mqtt_ws_client.publish(MQTT_TOPIC, json.dumps(data))
        
async def run_ws():
    mqtt_ws_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_ws_client.loop_start()
    print("Servidor WebSocket iniciado en el puerto 5002")
    async with serve(
        ws_handler,
        "0.0.0.0",               # escucha en todas las interfaces
        5002,                    # puerto del WebSocket
        ping_interval=None       # desactiva los pings automáticos
    ):
        await asyncio.Future()   # mantiene el servidor vivo indefinidamente


if __name__ == "__main__":
    Process(target=run_grpc, daemon=True).start()
    Process(target=run_rest, daemon=True).start()
    Process(target=lambda: asyncio.run(run_ws()), daemon=True).start()

    while True:
        time.sleep(60)