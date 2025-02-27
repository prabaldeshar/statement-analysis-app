frontend:
	cd statement-analysis-fe && docker compose up --build -d

stop-frontend:
	cd statement-analysis-fe && docker compose down

backend:
	cd statement-analysis-be && docker compose up --build -d

stop-backend:
	cd statement-analysis-be && docker compose down