## API для благотворительного фонда поддержки котиков - QRKot

### 1. Вы можете:
- Администратор может создавать благотворительные проекты
- Администратор может редактировть проекты, которые не внесены средства
- Зарегистрированые пользователи могут создавать пожертвования, которые автоматически распределяются по проектам

### 2. Как запустить проект:

   Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/sdvkam/cat_charity_fund.git
```
```
cd cat_charity_fund
```
Cоздать и активировать виртуальное окружение (рекомендация - на Python 3.9):
```
python3.9 -m venv venv
```
* Если у вас Linux/MacOS
    ```
    source venv/bin/activate
    ```
* Если у вас Windows
    ```
    source venv/scripts/activate
    ```
Обновить pip:
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Создать базу для сохранения данных
```
alembic upgrade head
```
Запустит проект
```
uvicorn app.main:app --reload
```
При первом запуске будет создан суперпользователь с данными указанными в .env файле в корневой папке.
```
Пример файла .env приведен в файле env_example.txt.
```
### 3. Документация по API
```
http://..../docs - в формате Swagger
```
```
http://..../redoc - в формате ReDoc
```

### 4. Технологии
- Python 3.9
- FastAPI 0.78.0
- SQLAlchemy 1.4.36
- SQLite

Language: ![https://img.shields.io/badge/Python-3.9-blue](https://img.shields.io/badge/Python-3.9-blue)
