Архитектура проекта
Project
- feedback-service
- ingredient-service
- subscriptions-service

Каждый сервис включает:

FastAPI приложение
модели SQLAlchemy
подключение к базе данных
seed-скрипты для заполнения данных
API для чтения данных

Во всех сервисах используется единый формат подключения через .env:

DATABASE_URL= connection_string

В базе данных используются отдельные схемы для каждого сервиса:

FeedbackService
IngredientService
SubscriptionService

Схемы были заранее созданы вручную в Azure SQL Database (поэтому в коде отсуствует сосздание схем).

1. Feedback Service
Функционал:
хранение отзывов пользователей
расчёт статистики рейтингов

Эндпоинты:
GET /feedback

Возвращает все отзывы.

GET /feedback/stats

Возвращает:

средний рейтинг по подписке
количество отзывов



2. Ingredient Service
Функционал:
управление ингредиентами
учёт остатков на складе

Эндпоинты:
GET /ingredients

Возвращает список ингредиентов с информацией:

название
описание
цена
доступное количество (рассчитывается динамически)


Subscription Service
Функционал:
управление подписками пользователей
список товаров внутри подписки

Эндпоинты:
GET /subscriptions

Возвращает:

данные подписки
список связанных ингредиентов


Заполнение тестовыми данными (seed data)

В каждом сервисе есть файл seed_data.py, который:

добавляет тестовые записи
заполняет таблицы stub-данными
используется для проверки работы API


1. Установка зависимостей
pip install -r requirements.txt

2. Настройка переменных окружения

Создать файл .env в каждом сервисе:

DATABASE_URL=ваш_connection_string

3. Создание таблиц

В каждом сервисе:
python create_db.py

4. Заполнение базы данных
python seed_data.py

5. Запуск сервиса
uvicorn app.main:app --reload


### Проверка работы очереди сообщений (Subscription → Feedback)

1.Запустить FeedbackService (consumer):
cd feedback-servise
python consumer.py

Ожидаемый результат:
Consumer запущен и слушает очередь...

2.Запустить SubscriptionService:
cd subscriptions-service
uvicorn app.main:app --reload

3.Открыть Swagger:
http://127.0.0.1:8000/doc

4.Выполнить запрос:
POST /subscriptions

body:
{
  "user_id": 1,
  "plan_type": "basic"
}






