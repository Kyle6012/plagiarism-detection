from celery import Celery
from app.core.config import settings


app = Celery('plagiarism_detection')

# Configure Celery with explicit settings
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)



# Import tasks
app.autodiscover_tasks(['app.services'])