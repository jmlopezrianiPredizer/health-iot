FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt app.py iot_pb2.py iot_pb2_grpc.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
