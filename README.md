# QRKot - Фонд помощи котикам


Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Ключевые возможности сервиса
- Создание благотворительных проектов
- Создание пожертвований для этих проектов
- Автоматическая система распределения пожертвований между проектами

## Использованные технологии
- Python 3.9
- FastAPI
- Alembic
- Uvicorn
- SQLAlchemy

## Как установить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Apicqq/cat_charity_fund
```

```
cd cat_charity_fund
```

Создать и активировать виртуальное окружение:

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

Создать файл .env:
```
touch .env
```

И наполнить его переменными по примеру из файла `.env.example`

Применить миграции:

```
alembic upgrade head
```

Запустить проект:
```
uvicorn app.main:app
```

Сервис QRKot будет доступен по адресу:  [http://127.0.0.1:8000](http://127.0.0.1:8000)

Документация доступна в файле [openapi.json](https://github.com/Apicqq/cat_charity_fund/blob/master/openapi.json), а также по следующим адресам:


Для документации Swagger:

[https://127.0.0.1:8000/swagger](https://127.0.0.1:8000/swagger)


Для документации ReDoc:

[https://127.0.0.1:8000/redoc](https://127.0.0.1:8000/redoc)


Автор проекта: [Никита Смыков](https://github.com/Apicqq)