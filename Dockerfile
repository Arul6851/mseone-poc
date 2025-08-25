# Use official lightweight Python image
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
