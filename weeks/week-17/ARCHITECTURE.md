# Архитектура финального проекта shipments-s07

## 1. Обзор проекта

`shipments-s07` — финальный проект по предмету ИТиСПО.

Система предназначена для управления доставками и отслеживания отправлений.

Основной вариант:

- project_code: `shipments-s07`
- resource: `shipments`
- singular: `shipment`
- extra_field: `tracking`
- main service: `shipments-svc-s07`
- port: `8230`

---

## 2. Состав системы

Система состоит из нескольких сервисов:

1. `shipments-svc-s07` — основной сервис для работы с отправлениями.
2. `tracking-service` — сервис отслеживания tracking-кодов.
3. `notification-service` — сервис уведомлений.
4. `gateway` — Nginx API Gateway для внешних запросов.

---

## 3. Shipments Service

`shipments-svc-s07` — основной REST API.

Функции:

- создание отправления;
- получение списка отправлений;
- получение отправления по ID;
- хранение tracking-кода;
- запрос статуса доставки у Tracking Service;
- отправка события в Notification Service.

Endpoint-ы:

- `GET /`
- `GET /health`
- `GET /shipments`
- `GET /shipments/{id}`
- `POST /shipments`
- `GET /shipments/{id}/tracking`

---

## 4. Tracking Service

`tracking-service` отвечает за получение информации по tracking-коду.

Функции:

- принимает tracking-код;
- возвращает статус доставки;
- возвращает текущее местоположение отправления.

Endpoint-ы:

- `GET /`
- `GET /health`
- `GET /tracking/{tracking_code}`

---

## 5. Notification Service

`notification-service` отвечает за уведомления.

Функции:

- принимает событие о создании отправления;
- сохраняет уведомления;
- возвращает список уведомлений.

Endpoint-ы:

- `GET /`
- `GET /health`
- `POST /notifications`
- `GET /notifications`

Падение Notification Service не должно полностью ломать создание shipment, поэтому в основном сервисе ошибка отправки уведомления обрабатывается безопасно.

---

## 6. API Gateway

В качестве Gateway используется Nginx.

Он принимает внешние HTTP-запросы и проксирует их на основной сервис.

Маршрут из варианта:

`/api/shipments -> shipments-svc-s07`

Gateway нужен для:

- единой точки входа;
- маршрутизации запросов;
- возможности добавить rate limiting;
- логирования внешних запросов.

---

## 7. Диаграмма взаимодействия

[Client]
   |
   v
[Gateway / Nginx]
   |
   v
[shipments-svc-s07]
   |              \
   |               \
   v                v
[tracking-service] [notification-service]

Основной поток:

1. Клиент отправляет запрос на Gateway.
2. Gateway перенаправляет запрос в `shipments-svc-s07`.
3. Shipments Service при необходимости обращается к Tracking Service.
4. При создании отправления Shipments Service отправляет событие в Notification Service.


---

## 8. Протоколы взаимодействия

Для внешнего API используется REST, потому что он удобен для клиентов, браузеров, curl и Postman.

Для внутреннего взаимодействия в текущей реализации используется HTTP между контейнерами внутри Docker Compose сети.

В проектной архитектуре возможно заменить внутреннее HTTP-взаимодействие на gRPC:

- `shipments-svc-s07 -> tracking-service`
- `shipments-svc-s07 -> notification-service`

gRPC подходит для межсервисного общения, потому что использует строгие контракты и эффективную сериализацию.


---

## 9. Хранение данных

В текущей учебной реализации данные хранятся в памяти приложения.

Для production-версии предполагается использовать PostgreSQL.

Пример таблицы `shipments`:

| Поле | Тип | Описание |
|---|---|---|
| id | integer | Идентификатор отправления |
| recipient | string | Получатель |
| address | string | Адрес доставки |
| tracking | string | Tracking-код |
| status | string | Статус доставки |

---

## 10. Docker

Каждый сервис упакован в отдельный Docker-образ.

Используются отдельные Dockerfile:

- `shipments-service/Dockerfile`
- `tracking-service/Dockerfile`
- `notification-service/Dockerfile`

Docker нужен для:

- изоляции сервисов;
- одинакового окружения на разных машинах;
- воспроизводимого запуска;
- удобной упаковки приложения.

---

## 11. Docker Compose

Для локального запуска используется `docker-compose.yml`.

Состав compose-проекта:

- `shipments-svc-s07`
- `tracking-service`
- `notification-service`
- `gateway`
- пользовательская сеть `final-net`

Запуск проекта:

```bash
docker compose up --build```

Проверка:

```bash
curl http://localhost:8230/
curl http://localhost:8230/shipments
curl http://localhost:8080/api/shipments```

---

## 12. Healthcheck

Для сервисов настроены health endpoint-ы:

- `GET /health` в Shipments Service
- `GET /health` в Tracking Service
- `GET /health` в Notification Service

В Docker Compose используется `depends_on` с `condition: service_healthy`.

Это позволяет запускать основной сервис только после готовности зависимых сервисов.

---

## 13. Kubernetes

Для Kubernetes используется приложение:

- k8s.app: `shipments-app`
- container: `shipments-container`

Возможная структура Kubernetes-манифестов:

- Deployment для запуска нескольких реплик приложения;
- Service для стабильного доступа к Pod-ам;
- probes для проверки готовности и живости контейнера;
- resources для ограничения CPU и памяти.

---

## 14. Helm

Helm chart может использоваться для шаблонизации Kubernetes YAML.

Через values-файлы можно задавать разные параметры для окружений:

- dev — 1 реплика, минимальные ресурсы;
- stage — 2 реплики;
- prod — 3 реплики и увеличенные limits.

Это позволяет не копировать Kubernetes YAML вручную для каждого окружения.

---

## 15. CI/CD

CI/CD pipeline должен выполнять следующие шаги:

1. Checkout кода.
2. Установка зависимостей.
3. Lint.
4. Запуск тестов.
5. Сборка Docker-образов.
6. Сохранение Docker-образов как artifact или публикация в registry.
7. Опциональный deploy через Helm или kubectl.

CI/CD уменьшает количество ручных ошибок и делает сборку воспроизводимой.

---

## 16. Наблюдаемость

Для наблюдаемости используются:

- health endpoint-ы;
- structured logs;
- логи Docker Compose;
- HTTP-коды ошибок;
- потенциально метрики RPS и latency.

Команды для просмотра логов:

```bash
docker compose logs shipments-svc-s07
docker compose logs tracking-service
docker compose logs notification-service```

---

## 17. Безопасность

Основные меры безопасности:

- валидация входных данных;
- проверка прав доступа;
- хранение секретов в переменных окружения;
- использование `.dockerignore`;
- ограничение CORS;
- rate limiting на Gateway;
- запуск контейнеров от non-root пользователя в production;
- проверка зависимостей через security audit.

---

## 18. Масштабирование

Сервисы можно масштабировать независимо.

Например:

- `shipments-svc-s07` масштабируется при росте количества API-запросов;
- `tracking-service` масштабируется при большом количестве запросов tracking;
- `notification-service` масштабируется при большом количестве событий.

Падение Notification Service не должно полностью останавливать создание shipment.

---

## 19. Инструкция по запуску

Перейти в папку проекта:

```bash
cd /home/weeks/week-17```

Запустить проект:

```bash
docker compose up --build```

Проверить основной сервис:

```bash
curl http://localhost:8230/```

Проверить список отправлений:

```bash
curl http://localhost:8230/shipments```

Проверить Gateway:

```bash
curl http://localhost:8080/api/shipments```

Создать отправление:

```bash
curl -X POST http://localhost:8080/api/shipments \
  -H "Content-Type: application/json" \
  -d '{"recipient":"Bob","address":"Berlin","tracking":"TRK-002"}'```

Проверить tracking:

```bash
curl http://localhost:8230/shipments/1/tracking```

---

## 20. Итог

Проект `shipments-s07` объединяет темы курса:

- REST API;
- межсервисное взаимодействие;
- Docker;
- Docker Compose;
- API Gateway;
- Kubernetes;
- Helm;
- CI/CD;
- Security Audit;
- Performance Analysis.

В результате получилась микросервисная система, которая запускается одной командой и имеет документацию по архитектуре.

