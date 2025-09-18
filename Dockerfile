FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

# Use uvicorn instead of gunicorn (fixes the error)
CMD uvicorn webhook_server:app --host 0.0.0.0 --port $PORT
