FROM python:3.14-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY project/ project/

CMD gunicorn -w 2 -b 0.0.0.0:${PORT:-8000} "project.app:app"