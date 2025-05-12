import os, time, requests, random, json

url = "http://gateway:5000/data"

def generate_data():
    # ids = os.getenv("SENSOR_ID", "SENSOR_REST")
    return {
        "id": "Sensor rest",
        "heart_rate": random.randint(50, 160),
        "temperature": round(random.uniform(36.0, 40.0), 1),
        "pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

def run():
    while True:
        data = generate_data()
        try:
            response = requests.post(url, json=data)
            print(f"Sent: {data}")
            print(f"Response: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar datos: {e}")
        time.sleep(5)

if __name__ == "__main__":
    run()