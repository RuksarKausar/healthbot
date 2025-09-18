# Use lighter Python image (saves 300MB+)
FROM python:3.9-slim

# Don't create .pyc files (saves space)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install only essential packages and clean up
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn && \
    rm -rf /root/.cache

# Copy your code
COPY . .

# Use port that Railway expects
EXPOSE $PORT

# Simple start command (no multiple processes)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 webhook_server:app
