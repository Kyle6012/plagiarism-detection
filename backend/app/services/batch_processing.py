from celery import Celery

celery = Celery(__name__)
celery.config_from_object("app.core.celery")

@celery.task
def process_batch(batch_id: str):
    # This is a placeholder for the actual batch processing logic.
    # In a real implementation, this would trigger the plagiarism check.
    print(f"Processing batch: {batch_id}")
