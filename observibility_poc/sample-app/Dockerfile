# Dockerfile for sample-app

FROM python:3.9

WORKDIR /app
COPY . /app

# Install necessary OpenTelemetry packages
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-api \
    opentelemetry-exporter-otlp

CMD ["python", "app.py"]
