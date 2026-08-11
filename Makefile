up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

api:
	curl http://localhost:8080/health

demo:
	curl -X POST "http://localhost:8080/api/v1/demo/generate?count=20"

producer:
	docker compose --profile tools run --rm event-producer

dashboard:
	start http://localhost:8501

airflow:
	start http://localhost:8081

clean:
	docker compose down -v
