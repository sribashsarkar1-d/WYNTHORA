from celery.schedules import crontab
from app.core.celery_app import celery_app
from app.tasks.ml_tasks import retrain_lstm_model

@celery_app.on_after_configure.connect  # type: ignore
def setup_periodic_tasks(sender, **kwargs):
    # Retrain LSTM model every Sunday at midnight
    sender.add_periodic_task(
        crontab(hour=0, minute=0, day_of_week=0),
        retrain_lstm_model.s(),
        name='retrain_lstm_model_weekly'
    )
