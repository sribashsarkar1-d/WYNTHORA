from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from prometheus_client import make_asgi_app
import logging

logger = logging.getLogger(__name__)

def setup_telemetry(app):
    """
    Sets up OpenTelemetry tracing and Prometheus metrics.
    """
    try:
        # 1. OpenTelemetry Tracing
        # Check if TracerProvider is already set to prevent "Overriding of current TracerProvider" warning
        if type(trace.get_tracer_provider()).__name__ == 'ProxyTracerProvider':
            provider = TracerProvider()
            processor = BatchSpanProcessor(ConsoleSpanExporter())
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            
            FastAPIInstrumentor.instrument_app(app)
            logger.info("OpenTelemetry Tracing initialized successfully.")
        else:
            logger.info("OpenTelemetry Tracing already initialized.")
        
        # 2. Prometheus Metrics Endpoint
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)
        logger.info("Prometheus metrics endpoint mounted at /metrics.")
        
    except Exception as e:
        logger.error(f"Failed to initialize telemetry: {e}")
