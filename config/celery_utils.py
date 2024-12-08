from celery import current_app as current_celery_app
from celery.result import AsyncResult
from .celery_config import settings


def create_celery():
    """
    Create and configure a new Celery instance
    """
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    # Update multiple configurations in a single call for better readability
    celery_app.conf.update(
        {
            "task_track_started": True,
            "task_serializer": "json",
            "result_serializer": "json",
            "accept_content": [
                "json",
            ],
            "result_persistent": True,
            "worker_send_task_events": False,
            "worker_prefetch_multiplier": 1,
        }
    )

    return celery_app


def get_task_info(task_id):
    """
    Returns task info for the given task_id, including status and result.
    """
    task = AsyncResult(task_id)
    if task.ready():
        result = {
            "id": task_id,
            "status": task.status,
            "result": task.result,
            "error": task.traceback
            if task.failed()
            else None,  # Include traceback if failed
        }
    else:
        result = {
            "id": task_id,
            "status": task.status,
            "result": None,
        }

    return result
