# Security Audit Report: reviews-s07

## 1. Информация о проекте

- project_code: reviews-s07
- service.name: reviews-svc-s07
- resource: reviews
- port: 8209
- endpoint: /api/reviews
- extra_field: rating

Цель аудита — проверить сервис `reviews-s07` по OWASP Top 10 и выявить уязвимости.

## 2. Чек-лист проверок

- Injection (SQL/Command Injection)
- Broken Access Control
- Authentication
- Token validation (JWT)
- Sensitive Data Exposure
- Cryptographic Failures
- Security Misconfiguration
- CORS
- Rate Limiting
- Logging & Monitoring
- Vulnerable Components
- Container Security

## 3. Анализ уязвимостей

### 3.1 Injection

Проверялись вредоносные входные данные:

' OR '1'='1  
1; DROP TABLE reviews;  
$(whoami)  
; cat /etc/passwd  

Риск: High  
Решение: использовать ORM и параметризованные запросы.

### 3.2 Broken Access Control

Проверка доступа по ID:

GET /api/reviews/1  
GET /api/reviews/2  

Риск: High  
Решение: проверять права доступа на сервере.

### 3.3 Authentication и JWT

Проверялось:

- доступ без токена
- проверка подписи
- срок действия токена

Риск: High  
Решение: валидировать JWT (signature, exp, role).

### 3.4 Input Validation

Поле: rating (int)

Примеры плохих данных:

{"rating": -100}  
{"rating": 999999}  
{"rating": "admin"}  

Риск: Medium  
Решение: ограничить диапазон (1–5).

### 3.5 Sensitive Data Exposure

Проверка:

- API keys
- пароли
- токены

Риск: High  
Решение: использовать переменные окружения.

### 3.6 Security Misconfiguration

Проверка:

- debug mode
- открытые порты
- дефолтные настройки

Риск: Medium  
Решение: отключить debug и закрыть лишние порты.

### 3.7 CORS

Проверка:

Access-Control-Allow-Origin: *

Риск: Medium  
Решение: указать конкретные домены.

### 3.8 Rate Limiting

Проверка:

GET /api/reviews

Риск: Medium  
Решение: добавить ограничение запросов.

### 3.9 Logging & Monitoring

Проверка логирования:

- ошибок
- подозрительных запросов

Риск: Medium  
Решение: добавить логирование.

### 3.10 Components

Проверка зависимостей.

Риск: Medium  
Решение: использовать pip-audit / Dependabot.

### 3.11 Container Security

Проверка:

- запуск от root
- лишние файлы
- секреты в образе

Риск: Medium  
Решение: использовать slim-образы и non-root пользователя.

## 4. Найденные проблемы

### 1. Нет строгой валидации rating

Severity: Medium  

Описание: rating может принимать некорректные значения.  

Пример:  
{"rating": -100}  

Решение: ограничить диапазон (1–5).

### 2. Возможен доступ к чужим данным

Severity: High  

Описание: доступ к чужим review по ID.  

Решение: проверять права доступа.

### 3. Нет rate limiting

Severity: Medium  

Описание: сервис можно перегрузить.  

Решение: добавить ограничение.

### 4. Возможные секреты в коде

Severity: High  

Описание: ключи могут храниться в коде.  

Решение: использовать env variables.

## 5. Итог

Сервис reviews-s07 требует:

- валидации данных
- контроля доступа
- rate limiting
- безопасного хранения секретов

Рекомендации:

1. Валидировать rating  
2. Проверять доступ  
3. Ограничить запросы  
4. Использовать secrets  
5. Обновлять зависимости  
6. Не запускать контейнер от root
