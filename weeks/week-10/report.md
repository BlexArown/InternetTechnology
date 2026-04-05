# Отчет по Docker

## Что было сделано

Для лабораторной работы был создан сервис `orders-svc-s07` на FastAPI.
Сервис работает с ресурсом `orders` и использует порт `8282` в соответствии с вариантом.

Также был создан `Dockerfile` с использованием multi-stage build:

- на первом этапе (`builder`) устанавливаются зависимости из `requirements.txt`
- на втором этапе создается итоговый runtime-образ только с нужными пакетами и исходным кодом

Был настроен файл `.dockerignore`, чтобы не включать в контекст сборки лишние файлы.

## Слои образа

В Docker каждая инструкция образует отдельный слой.

Основные слои (layers) Dockerfile:

1. `FROM python:3.11-slim AS builder`
2. `WORKDIR /app`
3. `COPY requirements.txt .`
4. `RUN pip install --no-cache-dir --prefix=/install -r requirements.txt`
5. `FROM python:3.11-slim`
6. `WORKDIR /app`
7. `COPY --from=builder /install /usr/local`
8. `COPY main.py .`
9. `EXPOSE 8282`
10. `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8282"]`

Использование multi-stage build уменьшает размер финального образа, потому что в него не попадают лишние промежуточные данные.

## Сборка и запуск

Сборка образа:

```bash
docker build -t week10-app .```

Запуск контейнера:

```bash
docker run -p 8282:8282 week10-app```

## Размер образа

Размер (size) образа можно посмотреть командой:

```bash
docker images```

Мой размер: 161 MB.
