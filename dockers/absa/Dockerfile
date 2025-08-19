
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip wheel -w /wheels -r /app/requirements.txt

FROM python:3.11-slim
WORKDIR /app

#  para confluent-kafka
RUN apt-get update \
 && apt-get install -y --no-install-recommends librdkafka-dev ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install /wheels/* && rm -rf /wheels

COPY main.py /app/main.py

COPY src/04_aspect_*_clf.joblib /app/models/

ENV KAFKA_BROKERS=kafka:9092 \
    TOPIC_IN=ml.absa.in \
    TOPIC_OUT=ml.absa.out \
    GROUP_ID=absa-v1 \
    MODELS_DIR=/app/models

CMD ["python", "main.py"]


