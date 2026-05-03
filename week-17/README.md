# Финальный проект shipments-s07

## Описание

`shipments-s07` — микросервисная система для управления доставками.

Сервисы:

- shipments-svc-s07 — основной REST API для отправлений
- tracking-service — сервис отслеживания tracking-кодов
- notification-service — сервис уведомлений
- gateway — Nginx API Gateway

## Запуск

```bash
docker compose up --build```
---

## Проверка

Основной сервис:

```bash
curl http://localhost:8230/
curl http://localhost:8230/shipments```

Через gateway:

```bash
curl http://localhost:8080/api/shipments```

Создание shipment:

```bash
curl -X POST http://localhost:8080/api/shipments \
  -H "Content-Type: application/json" \
  -d '{"recipient":"Bob","address":"Berlin","tracking":"TRK-002"}'```

Проверка tracking:

```bash
curl http://localhost:8230/shipments/1/tracking```

