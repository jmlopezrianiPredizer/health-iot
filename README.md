# 🏥 Health IoT Project

Este proyecto simula un sistema de monitoreo de salud utilizando sensores simulados, un gateway IoT, un broker MQTT, un suscriptor y una base de datos PostgreSQL. Todo está manejado con Docker y Docker Compose para una ejecución automatizada.

---

## 📁 Estructura del Proyecto
```
health-iot/
├── gateway/ # Procesa datos y publica en MQTT
│ ├── app.py
│ ├── Dockerfile
│ ├── iot_pb2.py
│ ├── iot_pb2_grpc.py
│ └── requirements.txt
├── sensors/ # Simuladores de sensores de salud
│ ├── sensor_rest.py
│ ├── sensor_grpc.py
│ ├── sensor_socket.py
│ ├── iot.proto
│ ├── Dockerfile
│ └── requirements.txt
├── subscriber/ # Suscriptor MQTT que escribe en PostgreSQL
│ ├── sub.py
│ └── Dockerfile
├── docker-compose.yml # Manejo de todos los servicios
└── README.md # Documentación del proyecto
```

---

## 🔌 Componentes

### 🔹 Sensores Simulados

Cada sensor genera datos aleatorios (temperatura, ritmo cardíaco, presión arterial) y los envía cada 5 segundos al gateway usando distintos protocolos.

| Archivo             | Protocolo   | Destino                        |
|---------------------|-------------|--------------------------------|
| `sensor_rest.py`    | REST        | `http://gateway:5000/data`     |
| `sensor_grpc.py`    | gRPC        | `gateway:50051`                |
| `sensor_socket.py`  | WebSocket   | `ws://gateway:5002/ws`         |

### 🔹 Gateway

Recibe datos desde los sensores a través de múltiples protocolos y los publica en el broker MQTT (`mqtt-broker`).

- Protocolo: REST, gRPC, WebSocket
- Puerto REST: `5000`
- Puerto gRPC: `50051`
- WebSocket: `5002`

### 🔹 MQTT Broker

- Imagen: `eclipse-mosquitto:2.0`
- Puerto: `1883`
- Guarda logs y mensajes en volúmenes persistentes.

### 🔹 Subscriber

Lee mensajes del broker MQTT y los guarda en una base de datos PostgreSQL.

### 🔹 Base de Datos (PostgreSQL)

- Usuario: `user`
- Contraseña: `12345`
- Base de datos: `iotdata`
- Puerto: `5432`

---

## 🚀 Cómo ejecutar el proyecto

1. **Construye los servicios (sin usar cache):**

```bash
docker-compose build --no-cache
