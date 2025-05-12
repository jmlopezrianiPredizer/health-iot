import os, json
import paho.mqtt.client as mqtt
import psycopg2

PG_HOST     = os.getenv("PG_HOST","postgres-db")
PG_PORT     = os.getenv("PG_PORT",5432)
PG_DB       = os.getenv("PG_DATABASE","iotdata")
PG_USER     = os.getenv("PG_USER","user")
PG_PASS     = os.getenv("PG_PASS","12345")
MQTT_BROKER = os.getenv("MQTT_BROKER","mqtt")
MQTT_PORT   = int(os.getenv("MQTT_PORT",1883))
MQTT_TOPIC  = os.getenv("MQTT_TOPIC","iot/entries")

connection = psycopg2.connect(host=PG_HOST,port=PG_PORT,dbname=PG_DB,user=PG_USER,password=PG_PASS)
connection.autocommit=True
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings(
    reading_id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    heart_rate INTEGER NOT NULL,
    temperature NUMBER NOT NULL,
    pressure TEXT NOT NULL,
    record_time TIMESTAMP NOT NULL DEFAULT now()
);
""")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    print("Conectado a ", MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    cursor.execute(
      "INSERT INTO readings(sensor_id, heart_rate, temperature, pressure) VALUES(%s,%s,%s,%s)",
      (payload["sensor_id"], payload["heart_rate"], payload["temperature"], payload["pressure"])
    )
    print("Exitoso registro:", payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()