# QRkot_spreadsheets
Сервис благотворительного фонда для закрытых проектов
с возможностью сохранения данных в документах Google


# Запуск

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Amirkhan012/cat_charity_fund
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск

```
uvicorn app.main:app
```

# Примеры
```
POST charity_project
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```

```
POST donation
{
  "full_amount": 0,
  "comment": "string"
}
```


# Cодержимое env-файла
APP_TITLE - Имя приложения (Сервис благотворительного фонда поддержки котиков)

APP_DESCRIPTION - Описание приложения (Приложение для благотворительного фонда поддержки котиков, в которой можно делать пожертвования)

DATABASE_URL - База данных (sqlite+aiosqlite:///./fastapi.db)

SECRET - Пароль (Superparol123)
FIRST_SUPERUSER_EMAIL - Имя суперпользователя (superuser@mail.ru)
FIRST_SUPERUSER_PASSWORD - Пароль суперпользователя (parol12345)

# Миграция
```
alembic revision --autogenerate -m "Описание миграции"
alembic upgrade head
```
