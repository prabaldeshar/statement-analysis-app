from celery import Celery

from api.config.settings import settings

app = Celery(
    "api",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include="api.tasks.transaction_tasks",
)


if __name__ == "__main__":
    app.start()
