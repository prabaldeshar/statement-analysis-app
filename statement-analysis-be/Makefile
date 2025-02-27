install:
	python3 -m pip install -r requirements.txt

dev:
	uvicorn api.main:app --port 8001 --reload

worker:
	celery -A api.worker.celery worker -l INFO