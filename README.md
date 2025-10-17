# MOOCLMS — Система управления обучением

## Технологический стек
- **Backend:** Python 3.13+, FastAPI, Flask
- **База данных:** SQLite (aiosqlite)
- **Аутентификация:** JWT
- **Инструменты:** Poetry, Git

---

## Предварительные требования

### Необходимое ПО:
- **Visual Studio Code** (рекомендуется)
- **Python 3.13** или выше
- **Git**

### Рекомендуемые расширения VSCode:
- Python
- Pylance
- SQLite
---

## Быстрый старт

### 1. Клонирование и настройка
```bash git clone <repository-url>``` 
```cd MOOCLMS```

2. Создание виртуального окружения
```bashpython -m venv env```

3. Активация виртуального окружения
Windows:

```bash .\env\Scripts\activate```
или - открываем меню конфигурации vsc и пишем Python: Select interpreter 

macOS/Linux:
```bash source env/bin/activate```

4. Установка зависимостей
```bash pip install poetry```
```poetry install```

Конфигурация
Создание файла окружения
Создайте файл .env в корне проекта:

DB_URL=sqlite+aiosqlite:///mooc.db
TEST_DB_URL=sqlite+aiosqlite:///test.db
JWT_SECRET=123_test_456_user
ACCESS_EXPIRE=1
REFRESH_EXPIRE=7
ALGORITHM=HS256

Запуск приложения
Запуск в разных терминалах:
Терминал 1 — База данных:

```bash python run_db.py```
Терминал 2 — Клиент (Flask):

```bashpython run_client.py```
Терминал 3 — Сервер (FastAPI):

```bash uvicorn run_server:app --reload```
Доступ к приложению
После запуска всех сервисов откройте в браузере:

Flask клиент: http://localhost:5000

FastAPI сервер: http://localhost:8000

Документация API
После запуска доступна автоматическая документация:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Структура проекта
text
MOOCLMS/
├── run_db.py          # Скрипт работы с БД
├── run_client.py      # Flask клиент
├── run_server.py      # FastAPI сервер
├── .env              # Конфигурация окружения
├── poetry.toml       # Конфигурация зависимостей
└── requirements.txt  # Список зависимостей
Проверка установки
Если все шаги выполнены правильно, вы сможете:

Создавать курсы и уроки

Регистрировать пользователей

Работать с системой через web-интерфейс

Использовать REST API для интеграций