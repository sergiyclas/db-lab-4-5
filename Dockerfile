FROM python:3.11-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Скопіювати requirements
COPY requirements.txt /app/

# Встановити залежності
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати увесь код у контейнер
COPY . /app

# Запускаємо gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1