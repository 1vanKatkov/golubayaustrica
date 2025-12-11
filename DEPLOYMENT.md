# Развертывание сайта в интернете

## Варианты хостинга

### 1. Railway (Рекомендуется для новичков) ⭐
- **Бесплатный тариф**: 512MB RAM, 1GB диск
- **URL**: railway.app
- **Плюсы**: Простая настройка, автоматический деплой из GitHub

### 2. Render
- **Бесплатный тариф**: 750 часов в месяц, спящий режим
- **URL**: render.com
- **Плюсы**: PostgreSQL база данных включена

### 3. Heroku
- **Бесплатный тариф**: Ограниченное время работы
- **URL**: heroku.com
- **Плюсы**: Хорошо документирован

## Подготовка проекта

### Шаг 1: Установите зависимости
```bash
pip install -r requirements.txt
```

### Шаг 2: Создайте секретный ключ
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Шаг 3: Соберите static файлы
```bash
python manage.py collectstatic --noinput
```

## Развертывание на Railway

### Шаг 1: Зарегистрируйтесь на railway.app
- Создайте аккаунт
- Подключите GitHub

### Шаг 2: Создайте новый проект
- Нажмите "New Project"
- Выберите "Deploy from GitHub repo"
- Выберите ваш репозиторий

### Шаг 3: Настройте переменные окружения
В разделе Variables добавьте:
```
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.railway.app
```

### Шаг 4: Импортируйте данные (опционально)
После первого деплоя:
```bash
python scripts/import_production_data.py
```

## Развертывание на Render

### Шаг 1: Зарегистрируйтесь на render.com

### Шаг 2: Создайте Web Service
- Нажмите "New" → "Web Service"
- Подключите GitHub репозиторий

### Шаг 3: Настройте сервис
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput --clear`
- **Start Command**: `gunicorn poker_site.wsgi`

### Шаг 4: Добавьте переменные окружения
```
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.onrender.com
```

## Локальное тестирование продакшена

### Шаг 1: Создайте .env файл
```bash
cp env-example.txt .env
```

### Шаг 2: Запустите с продакшен настройками
```bash
DEBUG=False SECRET_KEY=test-key ALLOWED_HOSTS=localhost,127.0.0.1 python manage.py runserver
```

## Структура файлов для деплоя

```
├── poker_site/
├── home/
├── static/
├── media/
├── scripts/
│   └── import_production_data.py
├── requirements.txt
├── Procfile
├── manage.py
├── data.csv (опционально)
└── DEPLOYMENT.md
```

## Важные моменты

1. **База данных**: В продакшене используйте PostgreSQL вместо SQLite
2. **Static файлы**: Автоматически собираются через Whitenoise
3. **Безопасность**: Никогда не коммитьте SECRET_KEY в код
4. **ALLOWED_HOSTS**: Добавьте домен вашего хостинга

## Команды для обслуживания

```bash
# Создание суперпользователя
python manage.py createsuperuser

# Резервное копирование данных
python manage.py dumpdata > backup.json

# Восстановление данных
python manage.py loaddata backup.json
```
