FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libc6-dev libpq-dev python3-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

RUN chmod +x /app/entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh

# Открываем порт для Gunicorn
EXPOSE 8000

# Запуск Gunicorn
CMD ["/app/entrypoint.sh"]

