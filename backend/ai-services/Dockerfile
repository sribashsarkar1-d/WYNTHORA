FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
ENV PYTHONPATH=/app

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi prometheus-client celery aioredis

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Create non-root user for security
RUN useradd -m -r appuser && chown -R appuser:appuser $APP_HOME
USER appuser

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
