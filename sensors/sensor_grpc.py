import grpc, time, random, os, iot_pb2, iot_pb2_grpc

def generate_data():
    # ids = os.getenv("SENSOR_ID", "SENSOR_GRPC")
    return iot_pb2.Data(
        id="Sensor grpc",
        heart_rate = random.randint(50,160),
        temperature=round(random.uniform(36.0, 40.0), 1),
        pressure=f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    )

def run():
    channel = grpc.insecure_channel('dns:///gateway:50051')
    stub = iot_pb2_grpc.IotServiceStub(channel)
    while True:
        iotData = generate_data()
        response = stub.SendData(iotData)
        print(f"Sent: {iotData}")
        print(f"Response: {response.status}")
        time.sleep(5)

if __name__ == "__main__":
    run()
