from time import sleep
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Set up OpenTelemetry metrics
exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317")
reader = PeriodicExportingMetricReader(exporter)
meter_provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Create a counter metric
counter = meter.create_counter(
    "requests_count",
    description="Count of requests",
)

# Simulate metrics recording
while True:
    counter.add(1)
    print("Recorded a metric")
    sleep(5)
