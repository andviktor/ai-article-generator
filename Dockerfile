FROM python:3.11-slim

WORKDIR /app

COPY requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]