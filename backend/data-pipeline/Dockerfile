FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt apache-airflow

COPY . .

ENV PYTHONPATH=/app/scripts
ENV AIRFLOW_HOME=/app/airflow

# Initialize airflow db on startup and run the scheduler
CMD airflow db init && airflow scheduler & airflow webserver -p 8080
