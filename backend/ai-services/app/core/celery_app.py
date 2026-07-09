from celery import Celery
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "world_sim_worker",
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/1"
)

# Enterprise Celery Configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Worker pools and scaling
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
    
    # Dead Letter Queues / Task Retries
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Default routing
    task_default_queue="default",
    task_routes={
        "app.tasks.ml_tasks.*": {"queue": "ml_queue"},
        "app.tasks.simulation_tasks.*": {"queue": "sim_queue"}
    }
)

# Optional: Periodic Tasks (Celery Beat) configuration can go here
