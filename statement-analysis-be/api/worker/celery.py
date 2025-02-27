from celery import Celery

from api.config.settings import settings

app = Celery(
    "api",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include="api.tasks.transaction_tasks",
)


if __name__ == "__main__":
    app.start()
