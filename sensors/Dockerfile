FROM python:3.13-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "sensor_rest.py"]
