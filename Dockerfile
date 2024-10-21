FROM python:3.12-slim

WORKDIR /app

COPY .env .env
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

EXPOSE 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "your_django_app.wsgi:application"]
