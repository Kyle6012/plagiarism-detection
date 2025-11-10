from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.services.batch_processing"],
)

celery_app.conf.update(
    task_track_started=True,
)
