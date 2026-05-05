# Recommendation System

## Запуск

docker-compose up -d

## Сервисы

- Event Service: 8001
- Feature Service: 8002
- Recommendation Service: 8003

## Тест

1. POST /events
2. GET /features/{user_id}
3. GET /recommendations/{user_id}
