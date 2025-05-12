import paho.mqtt.client as mqtt
import psycopg2, json

# Connect to the Postgres database
conn = psycopg2.connect(dbname="health", user="user", password="pass", host="db")
cur = conn.cursor()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    cur.execute(
      "INSERT INTO sensor_data (sensor, temperature, heart_rate, blood_pressure) VALUES (%s, %s, %s, %s)",
      (data["id"], data["temp"], data["hr"], data["bp"])
    )
    conn.commit()
    print("Saved:", data)

client = mqtt.Client()
client.on_message = on_message
client.connect("broker", 1883)
client.subscribe("health/sensors")
client.loop_forever()
