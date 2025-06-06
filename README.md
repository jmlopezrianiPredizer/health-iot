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
- Guarda logs y mensajes.

### 🔹 Subscriber

Lee mensajes del broker MQTT y los guarda en una base de datos PostgreSQL.

### 🔹 Base de Datos (PostgreSQL)

- Usuario: `user`
- Contraseña: `12345`
- Base de datos: `iotdata`
- Puerto: `5432`

---
## 🗃️ Esquema de la Base de Datos

La tabla `readings` almacena los registros recibidos desde los sensores IoT. Esta es su estructura:

| Campo         | Tipo de Dato | Descripción                                  |
|---------------|--------------|----------------------------------------------|
| `reading_id`  | SERIAL       | Identificador único, clave primaria          |
| `sensor_id`   | TEXT         | Identificador del sensor que envió el dato   |
| `heart_rate`  | INTEGER      | Ritmo cardíaco en bpm                        |
| `temperature` | REAL         | Temperatura corporal en grados Celsius       |
| `pressure`    | TEXT         | Presión arterial en formato `"120/80"`       |
| `record_time` | TIMESTAMP    | Fecha y hora de registro (por defecto: now)  |

---
## 🚀 Cómo ejecutar el proyecto

1. **Construye el gateway:**

```bash
docker-compose build --no-cache gateway
```
2. **Construye y ejecuta todos los servicios:**

```bash
docker-compose up
```
## ⭕ Cómo parar el proyecto
1. **Detiene todo:**
 ```bash
 cmd + c
 ```
 Repetir para forzar shutdown
2. **Elimina contededores:**
```bash
docker-compose down
```
3. **Elimina volumenes:**
``bash
docker-compose down --volumes
``
Esto asegura que al volver a alzar el proyecto no van a haber conflictos al ser construido.
## 🔎 Algunos comandos extras

**Verifica que el contenedor esté en ejecución:**

```bash
docker ps
```
**Útil si solo quieres inspeccionar la base de datos:**

```bash
docker-compose up -d db
```
---
## 🐘 Cómo acceder a la base de datos con DBeaver

Puedes usar DBeaver para conectarte y visualizar la base de datos PostgreSQL que utiliza el sistema.

### 🔧 Pasos para conectarse

1. Abre **DBeaver**.
2. Ve a **Database > New Database Connection**.
3. Selecciona **PostgreSQL** y haz clic en **Next**.
4. Llena los campos de conexión con la siguiente información:

| Parámetro    | Valor         |
|--------------|---------------|
| **Host**     | `localhost`   |
| **Port**     | `5432`        |
| **Database** | `iotdata`     |
| **Username** | `user`        |
| **Password** | `12345`       |

5. Haz clic en **Test Connection**.
   - Si es la primera vez, DBeaver te pedirá descargar el controlador. Acepta.
6. Si la prueba es exitosa, haz clic en **Finish**.
